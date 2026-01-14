# Product Backlog

> Prioritized list of user stories. Stories at the top are ready for the next sprint.
> Use `/story-create` to add new stories. Use `/sprint-plan` to pull stories into a sprint.

## Priority 1 - Next Sprint

<!-- Stories ready for immediate work. Must have clear acceptance criteria. -->

### STORY-002: Acquire Historical METAR Data for LPMA
**Points**: 5 | **Created**: 2026-01-11
**Labels**: feature

As a Data Engineer,
I want to download 20 years of METAR archives for LPMA (2004-2024),
So that I have a complete dataset for ML model training.

**Acceptance Criteria**:
- [ ] Automated download script created for bulk METAR retrieval
- [ ] All 20 years of data acquired (estimated 175,000+ records)
- [ ] Raw data stored in structured format (CSV or JSON intermediate storage)
- [ ] Data completeness report generated (records per year, missing dates identified)
- [ ] Sample validation: spot-check 10 random dates match official METAR archives

---

### STORY-003: Setup PostgreSQL and TimescaleDB Infrastructure
**Points**: 5 | **Created**: 2026-01-11
**Labels**: feature

As a Data Engineer,
I want to set up PostgreSQL with TimescaleDB extension,
So that I have an optimized time-series database for weather observations.

**Acceptance Criteria**:
- [ ] PostgreSQL 15+ installed and configured (local development environment)
- [ ] TimescaleDB extension installed and enabled
- [ ] Database created with appropriate user permissions
- [ ] Connection pooling configured for optimal performance
- [ ] Backup strategy documented (for future cloud deployment)

---

### STORY-004: Create METAR Observations Schema and Hypertables
**Points**: 3 | **Created**: 2026-01-11
**Labels**: feature

As a Data Engineer,
I want to design and create the `metar_observations` schema with TimescaleDB hypertables,
So that weather data is efficiently partitioned for time-range queries.

**Acceptance Criteria**:
- [ ] Schema created with all required fields: timestamp, wind_speed_kt, wind_direction_deg, gusts_kt, visibility_m, temperature_c, pressure_hpa, runway
- [ ] Hypertable created with time-based partitioning (daily or weekly chunks)
- [ ] Indexes created on time, wind_speed, wind_direction for query optimization
- [ ] Schema validated with sample data insertion (100+ test records)
- [ ] Query performance tested: time-range query completes in <100ms on sample data

---

### STORY-005: Build METAR Data Ingestion Pipeline
**Points**: 5 | **Created**: 2026-01-11
**Labels**: feature

As a Data Engineer,
I want to implement data ingestion scripts to load historical METAR data into TimescaleDB,
So that all 175K+ observations are stored in the database for analysis.

**Acceptance Criteria**:
- [ ] Python ingestion script created using pandas for batch processing
- [ ] METAR parsing implemented (using python-metar or metar library)
- [ ] Data cleaning logic handles missing values, outliers, format inconsistencies
- [ ] All 175K+ records successfully ingested into TimescaleDB
- [ ] Data validation: record counts match source files, no duplicate timestamps

---

### STORY-006: Implement Feature Engineering for Weather Data
**Points**: 3 | **Created**: 2026-01-11
**Labels**: feature

As a Data Engineer,
I want to create derived features from raw METAR observations,
So that ML models have richer input features for prediction.

**Acceptance Criteria**:
- [ ] Wind sector classification implemented (120-190°, 200-230°, 300-015°, 015-040° MAG)
- [ ] Time-of-day bins created (morning, midday, evening, night)
- [ ] Seasonal features extracted (month, quarter, is_winter_season)
- [ ] Derived features stored in database or computed on-demand (decision documented)
- [ ] Feature completeness: 100% of observations have all derived features

## Priority 2 - Soon

<!-- Important but not urgent. Will be refined before next sprint. -->

### STORY-007: Implement ANAC Wind Limit Rules Engine
**Points**: 5 | **Created**: 2026-01-11
**Labels**: feature

As a ML Engineer,
I want to implement the ANAC wind limit rules as a Python module,
So that I can automatically label METAR observations as disruption/no-disruption.

**Acceptance Criteria**:
- [ ] Rules engine implements all sector limits: Sector 120-190° (RW05: 20kt, RW23: 15kt, gusts 30/25kt), Sector 200-230° (25kt), Sector 300-015° (20kt), Sector 015-040° (25kt)
- [ ] Function accepts METAR observation and returns boolean disruption label
- [ ] Unit tests cover all sector boundaries and edge cases (10+ test cases)
- [ ] Rules engine applied to entire dataset (175K+ labels generated)
- [ ] Label distribution report: percentage of disruption vs no-disruption observations

---

### STORY-008: Build Ground Truth Validation Dataset from Media Sources
**Points**: 8 | **Created**: 2026-01-11
**Labels**: research

As a ML Engineer,
I want to manually research and validate historical disruption events from news sources,
So that I can verify the accuracy of rule-based labels.

**Acceptance Criteria**:
- [ ] Manual scraping/research of news articles for LPMA disruptions (2020-2024 focus)
- [ ] Target sources researched: The Portugal News, Madeira Island Direct, FlightRadar24 blog
- [ ] At least 100 labeled disruption events extracted with dates
- [ ] Cross-referenced with rule-based labels to calculate validation accuracy
- [ ] Ground truth validation dataset stored (CSV with date, source, event_type, rule_label, actual_disruption)
- [ ] Validation accuracy report: percentage of rule-based labels matching actual events

## Priority 3 - Later

<!-- Good ideas that need more definition or have dependencies. -->

### STORY-009: Conduct Exploratory Data Analysis on METAR Dataset
**Points**: 3 | **Created**: 2026-01-11
**Labels**: research

As a ML Engineer,
I want to perform EDA on the labeled METAR dataset,
So that I understand data patterns, correlations, and class balance before model training.

**Acceptance Criteria**:
- [ ] Jupyter notebook created with comprehensive EDA
- [ ] Label distribution analyzed (percentage of disruption vs no-disruption, expected 10-20%)
- [ ] Feature correlation analysis completed: which weather variables are most predictive
- [ ] Time-series patterns identified: seasonal trends, daily/weekly cycles
- [ ] Visualizations created: histograms, scatter plots, correlation heatmaps
- [ ] Key insights documented for feature engineering decisions

---

### STORY-010: Engineer ML Features with Lagged Variables
**Points**: 3 | **Created**: 2026-01-11
**Labels**: feature

As a ML Engineer,
I want to create lagged features (t-1, t-2, t-3 hours) and encode categorical variables,
So that the ML model has temporal context for predictions.

**Acceptance Criteria**:
- [ ] Lagged features created for key variables: wind speed, wind direction, gusts (t-1, t-2, t-3 hours)
- [ ] Categorical encoding: wind sector (one-hot), runway in use (ordinal), time-of-day bins (ordinal)
- [ ] Feature matrix prepared: all features ready for train/validation/test split
- [ ] Feature engineering pipeline documented (for reproducibility)
- [ ] No data leakage: lagged features only use past observations

---

### STORY-011: Train XGBoost Baseline Model
**Points**: 5 | **Created**: 2026-01-11
**Labels**: feature

As a ML Engineer,
I want to train an XGBoost binary classifier with default hyperparameters,
So that I establish a baseline prediction accuracy.

**Acceptance Criteria**:
- [ ] Train/validation/test split: 70% / 15% / 15% (time-series split: 2004-2018 train, 2019-2020 val, 2021-2024 test)
- [ ] XGBoost model trained with objective `binary:logistic`
- [ ] Class imbalance handled: `scale_pos_weight` parameter set or SMOTE applied
- [ ] Model saved as .pkl file for reuse
- [ ] Baseline accuracy calculated on validation set (target: >70%)

---

### STORY-012: Hyperparameter Tuning for XGBoost Model
**Points**: 5 | **Created**: 2026-01-11
**Labels**: feature

As a ML Engineer,
I want to optimize XGBoost hyperparameters using grid search or random search,
So that I maximize prediction accuracy.

**Acceptance Criteria**:
- [ ] Hyperparameter search configured: max_depth, learning_rate (eta), n_estimators, gamma, min_child_weight
- [ ] Search executed using cross-validation on training set
- [ ] Best hyperparameters identified and documented
- [ ] Optimized model trained with best parameters
- [ ] Validation accuracy improved over baseline (target: >75%)

---

### STORY-013: Comprehensive Model Evaluation and Validation
**Points**: 5 | **Created**: 2026-01-11
**Labels**: feature

As a ML Engineer,
I want to evaluate the trained model using multiple metrics and temporal validation,
So that I can verify it meets the >80% accuracy threshold.

**Acceptance Criteria**:
- [ ] Metrics calculated: Accuracy, Precision, Recall, F1-Score, ROC-AUC
- [ ] Confusion matrix visualized and analyzed
- [ ] Feature importance analysis: top 10 predictive variables identified
- [ ] Temporal validation: model performance consistent across 2021-2024 test years
- [ ] Error analysis: failure cases documented (when does model fail?)
- [ ] Model evaluation report: accuracy >80% on test set (success criterion)

---

### STORY-014: Develop FastAPI Backend with Forecast Endpoint
**Points**: 5 | **Created**: 2026-01-11
**Labels**: feature

As a Backend Developer,
I want to build a FastAPI REST API with a /forecast endpoint,
So that users can retrieve disruption predictions via HTTP.

**Acceptance Criteria**:
- [ ] FastAPI application created with project structure (routers, models, services)
- [ ] `GET /api/v1/forecast` endpoint implemented returning disruption status, confidence, last updated
- [ ] `GET /api/v1/status` health check endpoint implemented
- [ ] XGBoost model loaded and prediction logic integrated
- [ ] Response time <100ms tested with 100 concurrent requests
- [ ] OpenAPI documentation auto-generated and accessible at /docs

---

### STORY-015: Implement Redis Caching for Predictions
**Points**: 3 | **Created**: 2026-01-11
**Labels**: feature

As a Backend Developer,
I want to implement Redis caching for prediction results,
So that API response times are <100ms and compute costs are minimized.

**Acceptance Criteria**:
- [ ] Redis installed and configured (local development)
- [ ] Caching layer implemented in FastAPI: check cache before generating predictions
- [ ] Cache TTL set to 30 minutes (matches METAR update frequency)
- [ ] Cache hit rate measured: >80% in testing
- [ ] Response time reduced: <5ms for cache hits, <100ms for cache misses

---

### STORY-016: Build Celery Tasks for Real-Time METAR Ingestion
**Points**: 8 | **Created**: 2026-01-11
**Labels**: feature

As a Backend Developer,
I want to set up Celery with periodic tasks to fetch METAR data every 30-60 minutes,
So that predictions are based on real-time weather observations.

**Acceptance Criteria**:
- [ ] Celery configured with Redis broker
- [ ] Periodic task created: fetch METAR/TAF from Aviation Weather Center every 30-60 min
- [ ] METAR parsing logic reused from data ingestion pipeline
- [ ] New observations stored in TimescaleDB and trigger prediction update
- [ ] Error handling: retry logic with exponential backoff (max 3 retries)
- [ ] Task monitoring: Flower dashboard configured for debugging
- [ ] Task runs successfully for 24 hours without failure

---

### STORY-017: Build Frontend Web UI with Traffic-Light Status
**Points**: 5 | **Created**: 2026-01-11
**Labels**: feature

As an End User,
I want to see a simple web interface showing disruption status,
So that I can quickly understand flight disruption risk.

**Acceptance Criteria**:
- [ ] Single-page web app created (React or vanilla JS + Tailwind CSS)
- [ ] Traffic-light status indicator: Green (<20% risk), Yellow (20-60% risk), Red (>60% risk)
- [ ] Confidence score displayed as percentage (e.g., "73% disruption risk")
- [ ] 24-48h timeline forecast chart with hourly predictions
- [ ] Last updated timestamp shown
- [ ] Mobile-responsive design: works on phones, tablets, desktop
- [ ] WCAG AA color contrast compliance for accessibility

---

### STORY-018: Dockerize Application for Production Deployment
**Points**: 5 | **Created**: 2026-01-11
**Labels**: tech-debt

As a DevOps Engineer,
I want to containerize the entire application stack with Docker,
So that deployment is reproducible and cloud-ready.

**Acceptance Criteria**:
- [ ] Dockerfile created for FastAPI backend
- [ ] Dockerfile created for Celery worker
- [ ] Docker Compose configuration: FastAPI, Celery, Redis, PostgreSQL, Frontend
- [ ] Environment variables externalized (.env file support)
- [ ] Multi-stage builds optimize image size (<500MB total)
- [ ] Application runs successfully via `docker-compose up` on clean machine

---

### STORY-019: Deploy MVP to Cloud with Monitoring
**Points**: 8 | **Created**: 2026-01-11
**Labels**: tech-debt

As a DevOps Engineer,
I want to deploy the application to cloud infrastructure with monitoring,
So that the MVP is accessible to pilot users with 99%+ uptime.

**Acceptance Criteria**:
- [ ] Cloud provider selected (AWS EC2/Lightsail or GCP Cloud Run)
- [ ] Application deployed to production environment
- [ ] Domain registered and SSL configured (HTTPS)
- [ ] Uptime monitoring configured (UptimeRobot or similar)
- [ ] Error tracking configured (Sentry or CloudWatch Logs)
- [ ] CI/CD pipeline: GitHub Actions deploys on push to main branch
- [ ] Application accessible at production URL with <100ms API response time
- [ ] 99%+ uptime maintained for first 7 days post-deployment

## Icebox

<!-- Parked ideas. Low priority or blocked. Review quarterly. -->

---

## Story Template Reference

```markdown
### STORY-XXX: [Title]
**Points**: X | **Created**: YYYY-MM-DD
**Labels**: feature | bug | tech-debt | research

As a [user type],
I want [goal],
So that [benefit].

**Acceptance Criteria**:
- [ ] Criterion 1
- [ ] Criterion 2
```

---
Last updated: 2026-01-11 (19 stories, 91 points)
