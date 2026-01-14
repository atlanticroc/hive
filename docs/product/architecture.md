# System Architecture: LPMA Weather Disruption Predictor

**Last Updated**: 2026-01-08
**Architecture Status**: Pre-MVP Design
**Team**: Solo Developer
**Deployment Target**: Cloud (AWS/GCP)

---

## Architecture Overview

The LPMA Weather Disruption Predictor follows a **cloud-native, monolithic MVP architecture** optimized for solo development, with clear paths to scale horizontally as user adoption grows. The system combines time-series data engineering, machine learning inference, and real-time web services into a cohesive prediction platform.

### Design Principles

1. **Start Simple, Scale Smart**: Monolith for MVP, microservices decomposition only when proven necessary
2. **Data-First Architecture**: Time-series database optimized for weather data queries powers all features
3. **ML Pipeline Separation**: Model training offline (batch), inference online (real-time)
4. **Caching-First Performance**: Redis sits between API and expensive predictions
5. **Observability Built-In**: Monitoring, logging, error tracking from day 1

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        USERS (Web Browser)                       │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FastAPI Web Application                      │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐       │
│  │  Static UI   │   │ REST API     │   │ Background   │       │
│  │  (React/JS)  │   │ /forecast    │   │ Tasks        │       │
│  └──────────────┘   └──────┬───────┘   └──────────────┘       │
└─────────────────────────────┼────────────────────────────────────┘
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
  ┌──────────────────┐  ┌──────────┐  ┌─────────────────┐
  │  Redis Cache     │  │ XGBoost  │  │  PostgreSQL +   │
  │  (Predictions)   │  │  Model   │  │  TimescaleDB    │
  └──────────────────┘  └──────────┘  └─────────────────┘
                                              │
                                              │ Time-series data
                                              ▼
                                    ┌──────────────────────┐
                                    │  METAR Observations  │
                                    │    (Hypertables)     │
                                    └──────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      Celery Background Workers                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Periodic Task (every 30-60min):                          │  │
│  │  1. Fetch latest METAR/TAF from Aviation Weather Center   │  │
│  │  2. Parse and validate weather data                       │  │
│  │  3. Store in TimescaleDB                                  │  │
│  │  4. Trigger prediction update                             │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

All technology choices backed by Context7 documentation research and production ML system best practices.

### Backend: Python 3.12+

**Rationale**: Unified ecosystem for data engineering, ML, and web services. Mature libraries for METAR parsing, time-series analysis, and ML inference.

**Key Libraries**:
- `pandas` (2.x): METAR data processing, feature engineering
- `numpy` (1.26+): Numerical computations, array operations
- `scikit-learn` (1.7+): Feature preprocessing, model evaluation metrics
- `python-metar` / `metar`: METAR/TAF parsing

### Web Framework: FastAPI

**Context7 Reference**: `/websites/fastapi_tiangolo` (12,067 snippets, Benchmark Score: 94.6)

**Why FastAPI**:
- **High Performance**: Async/await for non-blocking I/O, comparable to Node.js/Go
- **Automatic OpenAPI Docs**: Built-in Swagger UI for API testing (critical for future B2B partnerships)
- **Background Tasks**: Native support for post-response processing without blocking user requests
- **Type Safety**: Pydantic models with automatic validation
- **Production Ready**: Used by Microsoft, Uber, Netflix for ML inference APIs

**Key FastAPI Patterns** (from Context7 research):

```python
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

app = FastAPI()

class ForecastResponse(BaseModel):
    status: str  # "green" | "yellow" | "red"
    disruption_probability: float  # 0-1
    confidence: float  # 0-1
    last_updated: str  # ISO 8601 timestamp

@app.get("/api/v1/forecast", response_model=ForecastResponse)
async def get_forecast(background_tasks: BackgroundTasks):
    # Check Redis cache first (< 5ms)
    cached = redis_client.get("latest_forecast")
    if cached:
        background_tasks.add_task(log_api_call, "cache_hit")
        return ForecastResponse.parse_raw(cached)

    # Cache miss: Generate prediction (~ 50-100ms)
    forecast = generate_prediction()
    redis_client.setex("latest_forecast", 1800, forecast.json())  # 30min TTL
    background_tasks.add_task(log_api_call, "cache_miss")
    return forecast
```

**Reference**: [FastAPI BackgroundTasks](https://fastapi.tiangolo.com/reference/background) - Post-response async operations

### Task Scheduling: Celery

**Context7 Reference**: `/websites/celeryq_dev_en_stable` (6,062 snippets, Benchmark Score: 87.1)

**Why Celery**:
- **Periodic Tasks**: Cron-like scheduling for METAR data fetching every 30-60min
- **Distributed Workers**: Scale horizontally by adding worker processes
- **Retry Logic**: Automatic retry with exponential backoff for failed API calls
- **Monitoring**: Flower dashboard for task tracking

**Celery Task Pattern** (from Context7 research):

```python
from celery import Celery
from celery.schedules import crontab

celery_app = Celery('lpma_predictor', broker='redis://localhost:6379/0')

@celery_app.task(bind=True, max_retries=3)
def fetch_metar_data(self):
    try:
        # Fetch from Aviation Weather Center
        response = requests.get("https://aviationweather.gov/api/data/metar?ids=LPMA")
        metar_data = parse_metar(response.text)

        # Store in TimescaleDB
        store_observation(metar_data)

        # Invalidate Redis cache to trigger fresh prediction
        redis_client.delete("latest_forecast")

    except Exception as exc:
        raise self.retry(exc=exc, countdown=300)  # Retry after 5min

# Schedule every 30 minutes
celery_app.conf.beat_schedule = {
    'fetch-metar-every-30min': {
        'task': 'tasks.fetch_metar_data',
        'schedule': crontab(minute='*/30'),
    },
}
```

**Reference**: [Celery Periodic Tasks](https://docs.celeryq.dev/en/stable/faq) - Custom schedule intervals for dynamic task execution

### Database: PostgreSQL 15+ with TimescaleDB Extension

**Research Citation**: [TimescaleDB for Time-Series Weather Data](https://maddevs.io/writeups/time-series-data-management-with-timescaledb/)

**Why PostgreSQL + TimescaleDB**:
- **Time-Series Optimization**: Hypertables with automatic time-based partitioning (10-100x faster time-range queries vs vanilla PostgreSQL)
- **Compression**: Native compression (90%+ storage savings on historical data older than 7 days)
- **Continuous Aggregates**: Pre-compute hourly/daily weather statistics for fast dashboard queries
- **SQL Compatibility**: Standard PostgreSQL, no new query language to learn
- **Scalability**: Proven for millions of rows/second ingestion (weather data is write-heavy)

**Schema Design**:

```sql
-- Main time-series table for METAR observations
CREATE TABLE metar_observations (
    time TIMESTAMPTZ NOT NULL,
    airport_code TEXT NOT NULL DEFAULT 'LPMA',
    wind_speed_kt INT,
    wind_direction_deg INT,
    wind_gust_kt INT,
    wind_sector TEXT,  -- '120-190', '200-230', '300-015', '015-040'
    visibility_m INT,
    temperature_c FLOAT,
    dewpoint_c FLOAT,
    pressure_hpa FLOAT,
    runway_in_use TEXT,  -- 'RW05' or 'RW23'
    raw_metar TEXT
);

-- Convert to TimescaleDB hypertable (automatic partitioning by time)
SELECT create_hypertable('metar_observations', 'time');

-- Continuous aggregate for hourly stats (pre-computed for dashboards)
CREATE MATERIALIZED VIEW metar_hourly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) AS hour,
    AVG(wind_speed_kt) AS avg_wind_speed,
    MAX(wind_gust_kt) AS max_gust,
    COUNT(*) AS observation_count
FROM metar_observations
GROUP BY hour;

-- Predictions table (model outputs)
CREATE TABLE disruption_predictions (
    time TIMESTAMPTZ NOT NULL,
    forecast_hour INT,  -- 0 (now), 1, 2, ..., 48
    disruption_probability FLOAT,  -- 0-1
    model_confidence FLOAT,  -- 0-1
    model_version TEXT,  -- 'xgboost_v1.0.2'
    features JSONB  -- Store input features for debugging
);

SELECT create_hypertable('disruption_predictions', 'time');

-- Data retention policy (drop old data automatically)
SELECT add_retention_policy('metar_observations', INTERVAL '3 years');
SELECT add_retention_policy('disruption_predictions', INTERVAL '1 year');
```

**Performance Optimizations**:
- **Indexes**: `CREATE INDEX ON metar_observations (time DESC, wind_sector);`
- **Compression Policy**: `SELECT add_compression_policy('metar_observations', INTERVAL '7 days');` (compress data older than 7 days)
- **Tiered Storage**: Hot data (last 30 days) on SSD, cold data (>30 days) on S3 via [tablespaces](https://www.tigerdata.com/blog/guide-to-postgres-data-management)

### Machine Learning: XGBoost (Primary), Prophet (v2), PyTorch (v3)

#### XGBoost (MVP Model)

**Context7 Reference**: `/dmlc/xgboost` (1,618 snippets, Benchmark Score: 85.8)

**Why XGBoost**:
- **Industry Standard**: Wins 80%+ of Kaggle competitions for structured/tabular data
- **Probability Output**: `objective='binary:logistic'` provides calibrated 0-1 probabilities
- **Feature Importance**: Built-in SHAP values for model interpretability
- **Fast Inference**: <10ms prediction latency for single sample
- **Handles Imbalance**: `scale_pos_weight` parameter for class weighting (disruptions are ~10-20% of data)

**Training Pipeline** (from Context7 best practices):

```python
from xgboost import XGBClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import roc_auc_score, classification_report

# Load labeled data from TimescaleDB
X_train, y_train = load_training_data(start='2004-01-01', end='2020-12-31')
X_val, y_val = load_training_data(start='2021-01-01', end='2022-12-31')
X_test, y_test = load_training_data(start='2023-01-01', end='2024-12-31')

# Initialize XGBoost with optimized hyperparameters
model = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.05,
    objective='binary:logistic',
    scale_pos_weight=5,  # Weight for class imbalance (90% non-disruption, 10% disruption)
    gamma=1.0,  # Regularization
    min_child_weight=3,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

# Train model
model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    early_stopping_rounds=20,
    verbose=10
)

# Evaluate
y_pred_proba = model.predict_proba(X_test)[:, 1]
print(f"ROC-AUC: {roc_auc_score(y_test, y_pred_proba):.3f}")
print(classification_report(y_test, (y_pred_proba > 0.5).astype(int)))

# Save model
import pickle
with open('models/xgboost_v1.0.0.pkl', 'wb') as f:
    pickle.dump(model, f)
```

**Reference**: [XGBoost Binary Classification](https://github.com/dmlc/xgboost/blob/master/doc/get_started.rst) - Probability prediction with logloss metric

#### Prophet (v2 - Uncertainty Intervals)

**Context7 Reference**: `/facebook/prophet` (584 snippets, Benchmark Score: 85.9)

**Why Prophet** (for v2 feature expansion):
- **Uncertainty Intervals**: MCMC sampling provides confidence bands (e.g., "70% confidence: 50-80% disruption risk")
- **Seasonality Handling**: Automatically detects daily, weekly, yearly patterns in wind disruptions
- **Interpretable Components**: Decompose forecast into trend + seasonality + holidays
- **Missing Data Robust**: Handles gaps in METAR observations gracefully

**Prophet Pattern** (from Context7 research):

```python
from prophet import Prophet

# Prepare data for Prophet (requires 'ds' and 'y' columns)
df = pd.DataFrame({
    'ds': timestamps,
    'y': disruption_binary_labels  # 0 or 1
})

# Initialize with MCMC for uncertainty
model = Prophet(
    interval_width=0.95,  # 95% confidence intervals
    mcmc_samples=300  # Full Bayesian sampling
)

# Train
model.fit(df)

# Forecast 48 hours ahead
future = model.make_future_dataframe(periods=48, freq='H')
forecast = model.predict(future)

# Extract uncertainty bounds
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
```

**Reference**: [Prophet Uncertainty Intervals](https://github.com/facebook/prophet/blob/main/docs/_docs/uncertainty_intervals.md) - MCMC sampling for seasonality uncertainty

#### PyTorch LSTM (v3 - Advanced Time-Series)

**Context7 Reference**: `/pytorch/pytorch` (3,920 snippets, Benchmark Score: 91)

**Why PyTorch LSTM** (experimental, v3+):
- **Sequence Modeling**: Captures long-term temporal dependencies (e.g., wind patterns over 6-12 hours)
- **Multi-Variate Input**: Handle multiple weather variables simultaneously (wind speed, direction, pressure, temp)
- **Attention Mechanisms**: Identify which past time steps most predictive of disruptions

**LSTM Architecture** (from Context7 research):

```python
import torch
import torch.nn as nn

class WeatherLSTM(nn.Module):
    def __init__(self, input_dim=10, hidden_dim=64, output_dim=1):
        super(WeatherLSTM, self).__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers=2, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # x: [batch, seq_len, input_dim]
        lstm_out, _ = self.lstm(x)
        # Take last time step output
        last_output = lstm_out[:, -1, :]
        output = self.fc(last_output)
        return self.sigmoid(output)  # Probability 0-1

# Input: 12-hour window of weather observations (12 timesteps × 10 features)
model = WeatherLSTM(input_dim=10, hidden_dim=64, output_dim=1)
```

**Reference**: [PyTorch LSTM Sequence Models](https://context7.com/pytorch/pytorch/llms.txt) - Sequence-to-sequence architectures

### Caching: Redis 7+

**Why Redis**:
- **Sub-5ms Latency**: In-memory cache for prediction results
- **TTL Support**: Auto-expire cached predictions after 30min (match METAR update frequency)
- **Distributed**: Multiple FastAPI instances can share cache
- **Simple**: Key-value store, no complex query language

**Caching Strategy**:
```python
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

def get_cached_forecast():
    cached = redis_client.get("forecast:latest")
    if cached:
        return json.loads(cached)
    return None

def cache_forecast(forecast_data, ttl=1800):  # 30min TTL
    redis_client.setex(
        "forecast:latest",
        ttl,
        json.dumps(forecast_data)
    )
```

**Performance Impact** (from scaling research):
- Without cache: 50-100ms per prediction (model inference + DB query)
- With cache: < 5ms (Redis lookup)
- **80-90% cache hit rate expected** (most users check same "current forecast" multiple times/day)

**Reference**: [FastAPI + Redis ML Serving](https://www.analyticsvidhya.com/blog/2025/06/ml-model-serving/) - Sub-100ms response times with caching

---

## Data Flow Architecture

### 1. Historical Data Acquisition (One-Time Setup)

```
Iowa State METAR Archive
         │
         │ HTTP API / Bulk Download
         ▼
 Python ETL Script
 (pandas + requests)
         │
         │ Batch Insert (175K records)
         ▼
PostgreSQL + TimescaleDB
  (metar_observations)
         │
         │ SQL Query
         ▼
  Feature Engineering
 (wind sectors, lagged features)
         │
         │ Labeled Dataset (CSV)
         ▼
   XGBoost Training
         │
         ▼
  Trained Model (.pkl)
```

### 2. Real-Time Prediction Flow

```
Aviation Weather Center API
         │
         │ Celery Task (every 30min)
         ▼
METAR Parser (python-metar)
         │
         │ Validated Weather Data
         ▼
 TimescaleDB Insert
  (metar_observations)
         │
         │ Invalidate Cache
         ▼
   Redis DELETE("forecast:latest")

─── User Request ───────────────

     User Browser
         │
         │ GET /api/v1/forecast
         ▼
    FastAPI Handler
         │
         │ Check Cache
         ▼
     Redis GET
         │
         ├─ Cache Hit (80%) → Return (< 5ms)
         │
         └─ Cache Miss (20%)
                │
                │ Load Model
                ▼
           XGBoost Inference
                │
                │ Features: Latest METAR + lagged
                ▼
        Disruption Probability (0-1)
                │
                │ Cache Result (30min TTL)
                ▼
           Return to User
```

---

## API Design

### Endpoints

#### `GET /api/v1/forecast`

**Description**: Get current disruption forecast + 24-48h timeline

**Response** (200 OK):
```json
{
  "status": "yellow",
  "disruption_probability": 0.68,
  "confidence": 0.85,
  "last_updated": "2026-01-08T14:30:00Z",
  "forecast_timeline": [
    {"hour": 0, "probability": 0.68, "status": "yellow"},
    {"hour": 1, "probability": 0.72, "status": "yellow"},
    {"hour": 6, "probability": 0.85, "status": "red"},
    {"hour": 12, "probability": 0.52, "status": "yellow"},
    {"hour": 24, "probability": 0.23, "status": "green"}
  ],
  "model_version": "xgboost_v1.0.2"
}
```

#### `GET /api/v1/status`

**Description**: Health check, model version, last METAR update

**Response** (200 OK):
```json
{
  "status": "healthy",
  "model_version": "xgboost_v1.0.2",
  "last_metar_update": "2026-01-08T14:00:00Z",
  "cache_hit_rate": 0.87,
  "uptime_seconds": 8640000
}
```

---

## Deployment Architecture

### MVP Deployment (Single Instance)

**Platform**: AWS Lightsail / GCP Cloud Run (low-cost, managed)

**Container Stack** (Docker Compose):
```yaml
version: '3.8'

services:
  web:
    image: lpma-predictor:latest
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/lpma
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  celery-worker:
    image: lpma-predictor:latest
    command: celery -A tasks worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/lpma
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  celery-beat:
    image: lpma-predictor:latest
    command: celery -A tasks beat --loglevel=info
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis

  db:
    image: timescale/timescaledb:latest-pg15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=secure_password

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

**Cost Estimate** (MVP Phase, 10-100 users):
- AWS Lightsail 2GB / GCP Cloud Run: $10-20/month
- Managed PostgreSQL (AWS RDS / GCP Cloud SQL): $30-50/month
- Domain + SSL: $15/year
- **Total**: ~$50-70/month

### Scaling Path (1,000+ DAU)

```
         ┌─────────────────┐
         │   CloudFlare    │  (CDN + DDoS protection)
         │   Load Balancer │
         └────────┬────────┘
                  │
      ┌───────────┼───────────┐
      │           │           │
      ▼           ▼           ▼
 ┌────────┐  ┌────────┐  ┌────────┐
 │FastAPI │  │FastAPI │  │FastAPI │  (Horizontal scaling)
 │  Pod 1 │  │  Pod 2 │  │  Pod 3 │
 └────┬───┘  └────┬───┘  └────┬───┘
      │           │           │
      └───────────┼───────────┘
                  │
         ┌────────┴────────┐
         │                 │
         ▼                 ▼
    ┌────────┐      ┌──────────────┐
    │ Redis  │      │ PostgreSQL + │
    │Cluster │      │ TimescaleDB  │
    └────────┘      └──────────────┘
```

**Horizontal Scaling**:
- Add FastAPI pods/instances (stateless, scale to 10-100+ pods)
- Redis cluster mode for distributed caching
- PostgreSQL read replicas for query load distribution
- Celery workers scale independently (add more for faster METAR ingestion)

---

## Security Architecture

### GDPR Compliance

**Data Protection Measures**:
- No user accounts required for MVP (anonymous usage, no PII collected)
- Google Analytics with IP anonymization
- Cookie consent banner (EU visitors)
- Privacy policy: Data retention, user rights (access, deletion)

**Reference**: [Aviation Data Protection Laws](https://www.numberanalytics.com/blog/aviation-data-protection-laws-guide) - GDPR requirements for aviation data

### API Security

- **HTTPS Only**: TLS 1.3, Let's Encrypt certificates
- **Rate Limiting**: 100 requests/IP/minute (prevent abuse)
- **CORS**: Restrict origins to production domain
- **Input Validation**: Pydantic models validate all API inputs

### Infrastructure Security

- **Secrets Management**: Environment variables, AWS Secrets Manager (no hardcoded credentials)
- **Database**: Private subnet, firewall rules (only app can access)
- **Monitoring**: Sentry for error tracking, UptimeRobot for uptime alerts

---

## Observability & Monitoring

### Logging

- **Structured Logs**: JSON format with correlation IDs
- **Log Levels**: INFO (API calls), WARNING (cache misses), ERROR (prediction failures)
- **Storage**: CloudWatch Logs (AWS) / Cloud Logging (GCP), 30-day retention

### Metrics

- **API Performance**: Request latency (p50, p95, p99), error rate, throughput
- **Model Performance**: Prediction latency, cache hit rate, model version
- **Data Freshness**: Last METAR update timestamp, data lag

### Alerts

- **Critical**: API downtime >5min, database connection failures
- **Warning**: Cache hit rate <70%, METAR data stale >2 hours
- **Email/Slack**: Notify founder immediately

---

## Research Citations (Architecture)

All technology choices backed by Context7 documentation and production ML system research.

### Context7 Technology Documentation

- **FastAPI**: `/websites/fastapi_tiangolo` (12,067 snippets, Benchmark: 94.6) - BackgroundTasks, async operations, production ML APIs
- **scikit-learn**: `/websites/scikit-learn_stable` (18,168 snippets, Benchmark: 85.1) - Time-series lagged features, model evaluation
- **Celery**: `/websites/celeryq_dev_en_stable` (6,062 snippets, Benchmark: 87.1) - Periodic task scheduling, retry logic
- **XGBoost**: `/dmlc/xgboost` (1,618 snippets, Benchmark: 85.8) - Binary classification, probability prediction, class imbalance
- **Prophet**: `/facebook/prophet` (584 snippets, Benchmark: 85.9) - Time-series forecasting, uncertainty intervals, MCMC sampling
- **PyTorch**: `/pytorch/pytorch` (3,920 snippets, Benchmark: 91) - LSTM sequence models, attention mechanisms

### Architecture & Scaling Research

- **TimescaleDB for weather data**: [Time-Series Data Management](https://maddevs.io/writeups/time-series-data-management-with-timescaledb/) - Hypertables, compression, continuous aggregates
- **FastAPI + Redis scaling**: [ML Model Serving](https://www.analyticsvidhya.com/blog/2025/06/ml-model-serving/) - Sub-100ms latency with caching
- **1M predictions/hour**: [Scaling FastAPI ML Inference](https://medium.com/@connect.hashblock/how-i-scaled-a-fastapi-ml-inference-server-to-handle-1m-predictions-per-hour-6c2424aa4faf) - Async queuing, micro-batching, GPU orchestration
- **METAR data pipeline**: [METAR Data Engineering Project](https://github.com/MarieeCzy/METAR-Data-Engineering-and-Machine-Learning-Project) - Real-world batch + real-time processing

### Security & Compliance

- **GDPR aviation**: [Aviation Data Protection](https://www.numberanalytics.com/blog/aviation-data-protection-laws-guide) - Compliance requirements, breach notification
- **Data retention policies**: [Data Protection Strategies 2026](https://hyperproof.io/resource/data-protection-strategies-for-2026/) - AI transparency, cross-border controls

---

**Architecture Version**: 1.0
**Next Review**: After MVP deployment (Month 4)
**Contact**: Architecture questions → founder@lpmaweather.com
