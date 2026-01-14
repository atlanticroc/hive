# Architecture Decision Records (ADRs)

**Last Updated**: 2026-01-08
**Status**: Pre-MVP
**Owner**: Technical Architecture Team

---

## Purpose

This document records significant architectural decisions made during the development of the LPMA Weather Disruption Predictor. Each ADR captures the context, decision, rationale, consequences, and alternatives considered, backed by research from Context7 documentation and production ML system best practices.

---

## ADR-001: Technology Stack Selection (Python, FastAPI, PostgreSQL + TimescaleDB)

**Date**: 2026-01-08
**Status**: Accepted
**Deciders**: Solo Founder/Developer
**Context7 Research**: 40,000+ code snippets analyzed across 6 libraries

### Context

The LPMA Weather Disruption Predictor requires a unified technology stack for:
1. **Data Engineering**: Processing 20+ years of METAR historical data (175K+ records)
2. **Machine Learning**: Training XGBoost models on time-series weather data with 10-20% class imbalance
3. **Web Services**: Serving real-time predictions via REST API with <100ms latency
4. **Background Jobs**: Fetching METAR data every 30-60min from Aviation Weather Center
5. **Time-Series Storage**: Efficient queries on weather observations (time-range filtering, aggregations)

**Constraints**:
- Solo developer (no dedicated DevOps/data engineering team)
- 2-4 month MVP timeline (rapid prototyping required)
- Budget-conscious (<$100/month infrastructure for MVP phase)
- Must scale to 1,000+ DAU without major architectural rewrites

### Decision

Adopt a **Python-centric stack**:

**Core Language**: Python 3.12+
**Web Framework**: FastAPI
**Database**: PostgreSQL 15+ with TimescaleDB extension
**Task Queue**: Celery with Redis broker
**Caching**: Redis 7+
**ML Libraries**: scikit-learn, XGBoost, pandas, numpy

### Rationale

#### 1. Python 3.12+ (Unified Ecosystem)

**Why**:
- **Single Language**: Data engineering (pandas), ML (scikit-learn, XGBoost), web services (FastAPI), background jobs (Celery) all in Python → No context switching, faster development
- **Mature ML Ecosystem**: Industry-standard libraries with extensive documentation (Context7 shows 40,000+ code snippets across our stack)
- **METAR Parsing**: Existing libraries (`python-metar`, `metar`) handle aviation weather parsing
- **Solo Developer Friendly**: One language to master, easier debugging, shared dependencies

**Research Citation**: 88-89% accuracy achievable with Python ML stack for weather classification ([Probabilistic Weather Forecasting, Nature 2024](https://www.nature.com/articles/s41586-024-08252-9))

#### 2. FastAPI (Web Framework)

**Context7 Reference**: `/websites/fastapi_tiangolo` (12,067 snippets, Benchmark Score: 94.6)

**Why**:
- **Performance**: Async/await for non-blocking I/O, comparable to Node.js (critical for API responsiveness)
- **Automatic OpenAPI Docs**: Built-in Swagger UI (future B2B partnerships require API documentation)
- **Type Safety**: Pydantic models with automatic validation (prevents production bugs)
- **Background Tasks**: Native support for post-response processing without blocking users
- **Production Proven**: Used by Microsoft, Uber, Netflix for ML inference APIs

**Key Pattern** (from Context7):
```python
@app.get("/api/v1/forecast")
async def get_forecast(background_tasks: BackgroundTasks):
    cached = redis_client.get("forecast:latest")
    if cached:
        background_tasks.add_task(log_api_call, "cache_hit")
        return cached
    # Generate prediction...
```

**Alternative Considered**: Flask
- **Rejected**: No native async support, slower for I/O-bound operations, less modern than FastAPI

#### 3. PostgreSQL 15+ with TimescaleDB Extension

**Research Citation**: [TimescaleDB for Time-Series Weather Data](https://maddevs.io/writeups/time-series-data-management-with-timescaledb/)

**Why**:
- **Time-Series Optimization**: Hypertables with automatic time-based partitioning → 10-100x faster time-range queries vs vanilla PostgreSQL
- **Compression**: Native compression (90%+ storage savings on historical data older than 7 days) → Reduces cloud storage costs
- **Continuous Aggregates**: Pre-compute hourly/daily weather statistics → Dashboards load instantly
- **SQL Compatibility**: Standard PostgreSQL, no new query language → Easier onboarding, compatible with ORMs
- **Scalability**: Proven for millions of rows/second ingestion (weather data is write-heavy)

**Performance Example**:
```sql
-- Query all METAR observations in last 48 hours where wind exceeded limits
SELECT * FROM metar_observations
WHERE time > NOW() - INTERVAL '48 hours'
  AND wind_speed_kt > 20;
-- With hypertables: scans only 2 chunks (48 hours) instead of full table
-- Vanilla PostgreSQL: scans all 175K+ rows
-- Speedup: 50-100x
```

**Alternatives Considered**:
- **MongoDB**: No native time-series optimization, weaker query capabilities for analytics
- **InfluxDB**: Specialized for metrics, but limited ML integration, smaller ecosystem
- **Vanilla PostgreSQL**: Works, but 10-100x slower for time-range queries on large datasets

#### 4. Celery + Redis (Background Jobs)

**Context7 Reference**: `/websites/celeryq_dev_en_stable` (6,062 snippets, Benchmark Score: 87.1)

**Why**:
- **Periodic Tasks**: Cron-like scheduling for METAR fetching every 30-60min (critical for real-time predictions)
- **Retry Logic**: Automatic retry with exponential backoff (Aviation Weather Center API can be flaky)
- **Monitoring**: Flower dashboard for task tracking (critical for solo developer debugging)
- **Python Native**: Seamless integration with FastAPI and data processing code

**Key Pattern** (from Context7):
```python
@celery_app.task(bind=True, max_retries=3)
def fetch_metar_data(self):
    try:
        response = requests.get("https://aviationweather.gov/api/data/metar?ids=LPMA")
        store_observation(parse_metar(response.text))
    except Exception as exc:
        raise self.retry(exc=exc, countdown=300)  # Retry after 5min
```

**Alternatives Considered**:
- **AWS Lambda + EventBridge**: More expensive for frequent tasks (30min intervals = 48 invocations/day), harder to debug
- **Python `schedule` library**: No distributed workers, single point of failure, no monitoring

#### 5. Redis (Caching)

**Why**:
- **Sub-5ms Latency**: In-memory cache for prediction results → API response time <100ms
- **TTL Support**: Auto-expire cached predictions after 30min (matches METAR update frequency)
- **80-90% Cache Hit Rate**: Most users check same "current forecast" multiple times/day → Massive compute savings
- **Simple**: Key-value store, minimal operational complexity

**Research Citation**: [FastAPI + Redis ML Serving](https://www.analyticsvidhya.com/blog/2025/06/ml-model-serving/) - Sub-100ms response times achievable with caching layer

**Performance Impact**:
- Without cache: 50-100ms per prediction (XGBoost inference + DB query)
- With cache: <5ms (Redis lookup)
- **Cost Savings**: Reduces API server CPU by 80-90% → Can handle 1,000 DAU on single $20/month server

### Consequences

**Positive**:
- ✅ **Rapid Development**: Python's high-level abstractions → 2-4 month MVP timeline achievable for solo developer
- ✅ **Cost-Effective**: Entire stack runs on $50-70/month during MVP phase (10-100 users)
- ✅ **Scalability Path**: FastAPI + PostgreSQL + Redis proven to scale to millions of users (add horizontal scaling when needed)
- ✅ **Extensive Documentation**: Context7 research found 40,000+ code snippets → Easy to find solutions
- ✅ **Operational Simplicity**: Fewer technologies → Easier monitoring, debugging, maintenance for solo developer

**Negative**:
- ⚠️ **Python Performance Ceiling**: Not as fast as Go/Rust for CPU-bound tasks (but ML inference is I/O-bound, so minimal impact)
- ⚠️ **TimescaleDB Learning Curve**: Requires understanding hypertables, compression policies (but well-documented, ~1 week learning)
- ⚠️ **Redis Memory Limits**: In-memory cache can get expensive at scale (mitigate: aggressive TTLs, LRU eviction policy)

**Risks**:
- **Vendor Lock-In** (Low): PostgreSQL + TimescaleDB is open-source, portable across clouds (AWS RDS, GCP Cloud SQL, self-hosted)
- **Operational Complexity** (Medium): Solo developer must manage 5 services (web, Celery worker, Celery beat, PostgreSQL, Redis) → **Mitigation**: Docker Compose for MVP, managed services (RDS, ElastiCache) for production

### Status

**Accepted** - Stack implemented in MVP (Month 1-4)

### Notes

- **Future Evolution**: If prediction latency becomes bottleneck (unlikely), consider GPU acceleration for PyTorch LSTM models
- **Alternative Explored**: Considered serverless (AWS Lambda + DynamoDB) but rejected due to cold start latency and cost for frequent tasks

---

## ADR-002: Machine Learning Model Choice (XGBoost for MVP, Prophet for v2)

**Date**: 2026-01-08
**Status**: Accepted (XGBoost), Planned (Prophet v2, PyTorch v3)
**Deciders**: Solo Founder/Developer
**Context7 Research**: XGBoost (1,618 snippets), Prophet (584 snippets), PyTorch (3,920 snippets)

### Context

The core value proposition is **accurate disruption probability prediction** (>85% accuracy target). Model choice impacts:
1. **Accuracy**: Must achieve >85% on historical validation (88-89% benchmark from research)
2. **Inference Speed**: <50ms for single prediction (target <100ms API response with caching)
3. **Interpretability**: Feature importance for debugging and user trust
4. **Development Time**: Solo developer, 2-4 month MVP timeline
5. **Data Efficiency**: Only 20 years of METAR data (~175K records, but disruptions are ~10-20% → class imbalance)

**Available Models** (from Context7 research):
- **XGBoost**: Gradient boosting trees for structured/tabular data
- **Prophet**: Facebook's time-series forecasting with seasonality handling
- **PyTorch LSTM**: Deep learning for sequence modeling
- **scikit-learn (Random Forest, Logistic Regression)**: Baseline models

### Decision

**MVP (Month 2-3)**: XGBoost Binary Classifier (`objective='binary:logistic'`)
**v2 (Month 11-12)**: Add Prophet for uncertainty intervals and seasonal pattern analysis
**v3 (Future)**: Experiment with PyTorch LSTM if XGBoost accuracy plateaus <85%

### Rationale

#### XGBoost for MVP

**Context7 Reference**: `/dmlc/xgboost` (1,618 snippets, Benchmark Score: 85.8)

**Why XGBoost Wins for MVP**:

1. **Industry Standard for Tabular Data**: Wins 80%+ of Kaggle competitions for structured data (METAR observations are tabular: wind speed, direction, pressure, temp, etc.)

2. **Probability Calibration**: `objective='binary:logistic'` provides well-calibrated 0-1 probabilities (critical for "73% disruption risk" UI display)

3. **Handles Class Imbalance**: `scale_pos_weight` parameter weights minority class (disruptions are ~10-20% of data)

4. **Feature Importance**: Built-in SHAP values → Understand which weather variables drive predictions (wind speed? gusts? wind sector?)

5. **Fast Inference**: <10ms for single prediction → Meets <100ms API response target with caching

6. **Development Speed**: Minimal hyperparameter tuning needed for baseline → Faster MVP timeline

**Training Pattern** (from Context7):
```python
from xgboost import XGBClassifier

model = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.05,
    objective='binary:logistic',
    scale_pos_weight=5,  # 90% non-disruption, 10% disruption
    gamma=1.0,  # Regularization to prevent overfitting
    random_state=42
)

model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    early_stopping_rounds=20  # Stop if validation accuracy doesn't improve
)
```

**Expected Performance** (from research):
- **Accuracy**: 82-89% (weather classification benchmark)
- **Training Time**: 5-15 minutes on 175K records (single CPU)
- **Inference**: <10ms per prediction

#### Prophet for v2 (Uncertainty Intervals)

**Context7 Reference**: `/facebook/prophet` (584 snippets, Benchmark Score: 85.9)

**Why Add Prophet in v2**:

1. **Uncertainty Quantification**: MCMC sampling provides confidence bands → "70% confidence: 50-80% disruption risk"

2. **Seasonality Decomposition**: Automatically detects patterns → "November-February highest disruption months" (valuable insight for travelers)

3. **Interpretable Components**: Forecast = trend + weekly seasonality + yearly seasonality + holidays → Users understand *why* risk is high

4. **Missing Data Robust**: Handles gaps in METAR observations (occasional Aviation Weather Center outages)

**Prophet Pattern** (from Context7):
```python
from prophet import Prophet

model = Prophet(
    interval_width=0.95,  # 95% confidence intervals
    mcmc_samples=300  # Full Bayesian sampling for uncertainty
)

model.fit(df)
forecast = model.predict(future)
# Extract uncertainty: forecast[['yhat', 'yhat_lower', 'yhat_upper']]
```

**When to Use**:
- **MVP**: XGBoost only (faster development, proven accuracy)
- **v2 (Month 11)**: Add Prophet for uncertainty intervals, seasonal analysis
- **Ensemble**: XGBoost (accuracy) + Prophet (uncertainty) → Best of both worlds

#### PyTorch LSTM for v3 (If Needed)

**Context7 Reference**: `/pytorch/pytorch` (3,920 snippets, Benchmark Score: 91)

**Why Defer to v3**:

1. **Complexity**: LSTM requires more data preprocessing (sequence windowing), longer training time (hours vs minutes)

2. **Interpretability**: Black-box model → Harder to debug, explain to users

3. **Overkill for MVP**: XGBoost likely achieves >85% accuracy on tabular METAR data

**When to Consider**:
- XGBoost accuracy plateaus <85% after hyperparameter tuning
- Need to model complex temporal dependencies (e.g., wind patterns over 12-hour windows)
- Have >5 years of high-quality labeled data (>100K disruption events)

**LSTM Architecture** (from Context7):
```python
class WeatherLSTM(nn.Module):
    def __init__(self, input_dim=10, hidden_dim=64):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers=2, batch_first=True)
        self.fc = nn.Linear(hidden_dim, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        lstm_out, _ = self.lstm(x)  # [batch, seq_len, hidden]
        return self.sigmoid(self.fc(lstm_out[:, -1, :]))  # Last timestep
```

### Alternatives Considered

| Model | Pros | Cons | Decision |
|-------|------|------|----------|
| **XGBoost** | Fast, accurate, interpretable, handles imbalance | None significant | ✅ **MVP Choice** |
| **Random Forest** | Interpretable, fast | Lower accuracy than XGBoost (typically 2-5% worse) | ❌ Rejected |
| **Logistic Regression** | Simple, fast, interpretable | Poor on non-linear patterns (weather is non-linear) | ❌ Rejected (baseline only) |
| **Prophet** | Uncertainty intervals, seasonality | Slower training, less accurate than XGBoost for classification | ✅ **v2 Addition** |
| **PyTorch LSTM** | Captures long-term dependencies | Complex, slow, requires more data, black-box | ⏸️ **v3 Experiment** |
| **CatBoost** | Similar to XGBoost, handles categorical features well | Less mature Python ecosystem, fewer Context7 examples | ❌ Rejected |

### Consequences

**Positive**:
- ✅ **Fast MVP**: XGBoost training in minutes → Iterate quickly on features, labels
- ✅ **Proven Accuracy**: 88-89% benchmark from weather classification research → Confident in >85% target
- ✅ **Interpretability**: Feature importance → Debug model, explain to users ("wind gusts are the key predictor")
- ✅ **Future-Proof**: Prophet (v2) and PyTorch (v3) are additive → No MVP rework needed

**Negative**:
- ⚠️ **No Uncertainty in MVP**: Users won't get confidence intervals until v2 (Prophet integration)
- ⚠️ **Potential Accuracy Ceiling**: XGBoost may plateau at 85-87% (orographic effects at LPMA are complex) → **Mitigation**: Ensemble with Prophet, or try LSTM in v3

**Risks**:
- **Model Accuracy <80%** (High Impact, Medium Likelihood): If XGBoost fails to learn orographic patterns → **Mitigation**: Add terrain/elevation features, collect more ground truth data from news scraping, try ensemble methods

### Status

**Accepted** - XGBoost implemented in MVP (Month 2-3), Prophet planned for v2 (Month 11)

### Notes

- **Model Versioning**: Use semantic versioning (e.g., `xgboost_v1.0.2`) for production models, track in predictions table
- **A/B Testing**: When adding Prophet (v2), run A/B test (50% users see XGBoost, 50% see Prophet) to compare accuracy

---

## ADR-003: Database Architecture (PostgreSQL + TimescaleDB vs Alternatives)

**Date**: 2026-01-08
**Status**: Accepted
**Deciders**: Solo Founder/Developer
**Research Citation**: [TimescaleDB for Time-Series Weather Data](https://maddevs.io/writeups/time-series-data-management-with-timescaledb/)

### Context

Weather data is **time-series by nature**: METAR observations timestamped every hour, predictions timestamped with forecast horizon (0h, 1h, ..., 48h). Database choice impacts:
1. **Query Performance**: 90% of queries are time-range filters (e.g., "last 48 hours of METAR data")
2. **Storage Costs**: 20+ years of data = 175K+ records, growing by 24 records/day
3. **Scalability**: Must handle millions of rows/second ingestion for real-time METAR updates
4. **Developer Experience**: Solo developer needs SQL familiarity, not new query languages

**Query Patterns**:
- Time-range filters: `SELECT * FROM metar_observations WHERE time > NOW() - INTERVAL '48 hours'`
- Aggregations: `SELECT AVG(wind_speed_kt) FROM metar_observations WHERE time > NOW() - INTERVAL '7 days'`
- Joins: Predictions table JOIN METAR observations (for accuracy validation)

### Decision

**PostgreSQL 15+ with TimescaleDB extension** for all persistent data storage.

### Rationale

#### Why PostgreSQL?

1. **Mature Ecosystem**: 30+ years of development, rock-solid reliability, extensive tooling
2. **SQL Standard**: No new query language → Faster development, easier onboarding
3. **ACID Compliance**: Ensures data integrity (critical for audit trail, GDPR compliance)
4. **Extensions**: TimescaleDB, PostGIS (future: geospatial weather analysis), pg_cron (scheduled jobs)
5. **Cloud Support**: Managed services on AWS RDS, GCP Cloud SQL, Azure Database → No operational burden

#### Why TimescaleDB Extension?

**Research Citation**: [TimescaleDB for Weather Data](https://maddevs.io/writeups/time-series-data-management-with-timescaledb/)

**Time-Series Optimizations**:

1. **Hypertables (Automatic Partitioning)**:
   - Converts table into time-based chunks (e.g., 1 chunk per week)
   - Queries only scan relevant chunks → 10-100x faster than full table scan
   - Example: Query last 48 hours → Scans 2 chunks (48h) instead of 520 chunks (20 years)

2. **Native Compression**:
   - Compresses data older than 7 days (configurable)
   - 90%+ storage savings on historical data → Reduces cloud storage costs from $50/month to $5/month
   - No performance impact (decompression on-the-fly)

3. **Continuous Aggregates**:
   - Pre-compute hourly/daily statistics (e.g., `AVG(wind_speed_kt)` per day)
   - Dashboards load instantly (query pre-computed view, not raw 175K records)
   - Example: "Average wind speed by month for last 2 years" → 24 rows returned, not 17,520 rows

4. **Data Retention Policies**:
   - Auto-delete data older than 3 years (GDPR: minimal data retention)
   - No manual DELETE queries (which are slow, lock tables, fragment indexes)

**Schema Example**:
```sql
CREATE TABLE metar_observations (
    time TIMESTAMPTZ NOT NULL,
    wind_speed_kt INT,
    wind_direction_deg INT,
    wind_gust_kt INT,
    wind_sector TEXT,
    visibility_m INT,
    temperature_c FLOAT,
    pressure_hpa FLOAT,
    runway_in_use TEXT,
    raw_metar TEXT
);

-- Convert to TimescaleDB hypertable
SELECT create_hypertable('metar_observations', 'time');

-- Compression policy: Compress data older than 7 days
SELECT add_compression_policy('metar_observations', INTERVAL '7 days');

-- Retention policy: Delete data older than 3 years
SELECT add_retention_policy('metar_observations', INTERVAL '3 years');
```

**Performance Benchmarks** (from research):
- **Vanilla PostgreSQL**: 2-5 seconds for time-range query on 175K rows
- **TimescaleDB Hypertable**: 20-50ms for same query (100x faster)
- **Continuous Aggregates**: <10ms for dashboard queries (500x faster)

### Alternatives Considered

| Database | Pros | Cons | Decision |
|----------|------|------|----------|
| **PostgreSQL + TimescaleDB** | Time-series optimized, SQL, mature, cost-effective | Requires learning hypertables | ✅ **Selected** |
| **MongoDB** | Flexible schema, JSON native | No time-series optimization, weaker analytics | ❌ Rejected |
| **InfluxDB** | Purpose-built for time-series | Limited ML integration, smaller ecosystem, InfluxQL learning curve | ❌ Rejected |
| **DynamoDB** | Serverless, auto-scaling | Expensive for large datasets, no SQL, poor for analytics | ❌ Rejected |
| **Vanilla PostgreSQL** | Simple, no extensions | 10-100x slower for time-range queries | ❌ Rejected (too slow) |

#### Why Not MongoDB?

- **No Time-Series Optimization**: No equivalent to hypertables → Scans all 175K documents for time-range queries
- **Weaker Analytics**: Aggregation framework more complex than SQL `GROUP BY`, `JOIN`
- **Data Integrity**: No ACID transactions (eventual consistency) → Risk of data loss during METAR ingestion failures

#### Why Not InfluxDB?

- **ML Integration**: Harder to connect scikit-learn, XGBoost (no native Python ORM like SQLAlchemy)
- **InfluxQL**: New query language → Learning curve for solo developer
- **Limited Ecosystem**: Fewer tools, libraries, StackOverflow answers vs PostgreSQL

#### Why Not DynamoDB?

- **Cost**: $0.25 per million reads → At 1,000 DAU × 10 API calls/day × 365 days = 3.65M reads/year = $900/year (vs $50/month for PostgreSQL RDS)
- **No SQL**: Query complexity increases (partition key design, GSI management)
- **Poor for Analytics**: No aggregations, joins (require application-level code)

### Consequences

**Positive**:
- ✅ **Query Performance**: Sub-100ms for all time-range queries → API response time <100ms achievable
- ✅ **Cost-Effective**: 90% compression on historical data → $5-10/month storage vs $50-100/month for uncompressed
- ✅ **Developer Productivity**: SQL familiarity → Faster feature development (no learning InfluxQL, MongoDB aggregation framework)
- ✅ **Scalability**: Proven to handle millions of rows/second → No architectural rewrite needed for 1,000+ DAU
- ✅ **GDPR Compliance**: Retention policies auto-delete old data → Minimal data retention requirement satisfied

**Negative**:
- ⚠️ **Learning Curve**: Solo developer must understand hypertables, compression policies, continuous aggregates (~1 week)
- ⚠️ **Extension Dependency**: TimescaleDB must be installed on PostgreSQL (adds deployment step, but managed services support it)

**Risks**:
- **TimescaleDB Support** (Low): If Timescale Inc. discontinues extension → **Mitigation**: Open-source project, active community, can fork if needed
- **Migration Complexity** (Low): If switch to different DB needed → **Mitigation**: PostgreSQL compatibility ensures easy migration (dump/restore)

### Status

**Accepted** - Implemented in MVP (Month 1-2: Data Acquisition phase)

### Notes

- **Managed Services**: Use AWS RDS for PostgreSQL with TimescaleDB extension (no self-hosting complexity)
- **Backup Strategy**: Automated daily backups (AWS RDS) + weekly manual dumps to S3 (disaster recovery)

---

## ADR-004: Security & Compliance Approach (GDPR, Data Protection)

**Date**: 2026-01-08
**Status**: Accepted
**Deciders**: Solo Founder/Developer
**Research Citation**: [Aviation Data Protection Laws](https://www.numberanalytics.com/blog/aviation-data-protection-laws-guide/)

### Context

The product targets **EU travelers** (Madeira is Portugal, EU jurisdiction) and handles **aviation-related data** (METAR observations, predictions). Compliance requirements:
1. **GDPR**: EU General Data Protection Regulation (€20M or 4% global revenue penalties for violations)
2. **IATA Data Protection**: Aviation industry-specific guidelines
3. **72-Hour Breach Notification**: Must report data breaches within 72 hours
4. **Data Minimization**: Collect only necessary data, delete when no longer needed

**Data Collected**:
- **METAR Data**: Public weather observations (no PII)
- **Predictions**: Disruption probabilities (no PII)
- **User Analytics**: Page views, session duration (Google Analytics with IP anonymization)
- **No User Accounts**: Anonymous usage for MVP (no email, password, names)

### Decision

Implement **privacy-first, GDPR-compliant architecture** from day 1:
1. **No User Accounts** (MVP): Anonymous usage, no PII collected
2. **IP Anonymization**: Google Analytics with IP masking
3. **Cookie Consent**: GDPR-compliant banner for EU visitors
4. **Data Retention**: Auto-delete METAR data older than 3 years (TimescaleDB retention policy)
5. **Security**: HTTPS-only (TLS 1.3), encrypted database connections, secrets in environment variables

### Rationale

#### 1. No User Accounts (MVP)

**Why**:
- **GDPR Simplified**: No PII = No data breach risk, no "right to erasure" requests, no consent management
- **Lower Barriers**: Users don't need to sign up → Higher conversion (anonymous users can check forecast immediately)
- **Solo Developer Friendly**: No authentication system to build, maintain, secure

**Trade-off**: Can't build personalized features (e.g., "Your saved flights") until v2 (when accounts are added)

#### 2. IP Anonymization (Google Analytics)

**Why**:
- **GDPR Article 4(1)**: IP addresses are PII under GDPR → Must anonymize
- **Google Analytics IP Anonymization**: Replaces last octet of IP with zeros (e.g., `192.168.1.123` → `192.168.1.0`)
- **Sufficient for Analytics**: Still tracks country, city (for user demographics) without storing full IP

**Implementation**:
```javascript
gtag('config', 'GA_MEASUREMENT_ID', {
  'anonymize_ip': true
});
```

#### 3. Cookie Consent Banner

**Why**:
- **GDPR Article 7**: Requires informed consent for non-essential cookies (analytics, marketing)
- **Essential Cookies**: Authentication, security (session tokens) → No consent needed
- **Analytics Cookies**: Google Analytics → **Requires consent** before setting cookies

**Implementation**: Use Cookiebot or similar GDPR-compliant consent management platform

#### 4. Data Retention Policies

**GDPR Article 5(1)(e)**: "Personal data shall be kept in a form which permits identification of data subjects for no longer than is necessary."

**Why Delete Old Data**:
- **Minimal Retention**: Only keep METAR data needed for model training (3 years sufficient)
- **Storage Cost**: Auto-delete reduces cloud storage bills
- **Compliance**: Automatic enforcement (TimescaleDB retention policy, no manual deletion)

**Implementation**:
```sql
SELECT add_retention_policy('metar_observations', INTERVAL '3 years');
```

#### 5. Security Measures

**Research Citation**: [Data Protection Strategies 2026](https://hyperproof.io/resource/data-protection-strategies-for-2026/) - AI transparency, quantum-safe encryption

**Why HTTPS-Only**:
- **GDPR Article 32**: "Appropriate technical and organizational measures to ensure a level of security appropriate to the risk"
- **Encryption in Transit**: TLS 1.3 prevents man-in-the-middle attacks on API requests

**Why Database Encryption**:
- **AWS RDS Encryption**: Data encrypted at rest (AES-256), encrypted backups
- **Connection Encryption**: PostgreSQL SSL connections (prevent credential sniffing)

**Why Secrets Management**:
- **No Hardcoded Credentials**: Database passwords, API keys in environment variables or AWS Secrets Manager
- **Prevents Leaks**: If code repository is compromised, secrets not exposed

### Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| **No User Accounts (Anonymous)** | GDPR-simple, lower barriers, faster MVP | No personalization | ✅ **MVP Choice** |
| **Email Accounts** | Enables notifications, personalization | GDPR complexity, requires auth system | ⏸️ **v2 Feature** |
| **Self-Hosted Analytics** | No third-party data sharing | More operational complexity | ❌ Rejected (overkill for MVP) |
| **No Analytics** | Maximum privacy | Blind to user behavior, can't optimize | ❌ Rejected (need metrics) |

### Consequences

**Positive**:
- ✅ **Legal Compliance**: GDPR-ready from day 1 → No risk of €20M fines
- ✅ **User Trust**: Privacy-first approach → Marketing differentiator ("We don't track you")
- ✅ **Operational Simplicity**: No user database to secure, back up, manage → Solo developer can focus on ML, not security

**Negative**:
- ⚠️ **Limited Features**: Can't build personalized experiences (flight-specific forecasts, push notifications) until user accounts added in v2
- ⚠️ **No Email Marketing**: Can't build email list for product updates → **Mitigation**: Add optional email capture form (with consent) for newsletter

**Risks**:
- **Data Breach** (Low Impact, Low Likelihood): If PostgreSQL compromised → No PII exposed (only public METAR data, anonymous predictions)
- **GDPR Misinterpretation** (Low): If GDPR lawyer finds compliance gaps → **Mitigation**: Consult aviation data protection lawyer before public launch

### Status

**Accepted** - Implemented from MVP day 1 (Month 1)

### Notes

- **Privacy Policy**: Must publish before public launch (Month 7), template: "We collect no personal data. Analytics with IP anonymization."
- **Terms of Service**: Disclaimer: "For informational purposes only, not for flight planning decisions"
- **Cookie Banner**: Must appear before Google Analytics loads (GDPR requirement)
- **Audit Trail**: Log all data access (who, when, what) for GDPR Article 30 compliance

---

## Summary Table: All ADRs

| ADR | Decision | Status | Impact | Research Citations |
|-----|----------|--------|--------|-------------------|
| **ADR-001** | Python + FastAPI + PostgreSQL/TimescaleDB | ✅ Accepted | High (foundational) | Context7: 40K+ snippets, TimescaleDB research |
| **ADR-002** | XGBoost (MVP), Prophet (v2), PyTorch (v3) | ✅ Accepted (XGBoost) | High (core ML) | Context7: XGBoost (1,618), Prophet (584), PyTorch (3,920) |
| **ADR-003** | PostgreSQL + TimescaleDB over MongoDB/InfluxDB | ✅ Accepted | High (performance) | TimescaleDB 10-100x faster for time-range queries |
| **ADR-004** | Privacy-first, no user accounts, GDPR compliance | ✅ Accepted | Medium (legal) | GDPR aviation data protection research |

---

**ADR Document Version**: 1.0
**Next Review**: After MVP launch (Month 5), review ADR-002 (model performance) and ADR-004 (add user accounts for v2)
**Owner**: Solo Founder/Developer
