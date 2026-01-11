# Product Roadmap: LPMA Weather Disruption Predictor

**Last Updated**: 2026-01-08
**Planning Horizon**: 12 months (MVP + v1 + v2)
**Team Context**: Solo developer/founder
**Status**: Pre-MVP (Data Acquisition Phase)

---

## Roadmap Overview

The roadmap follows a **research-validated, data-driven approach** to building a production-ready ML prediction system. Phases are designed for solo development with realistic timelines accounting for data engineering complexity, model experimentation, and iterative validation.

### Strategic Themes

1. **Foundation First** (Months 1-4): Acquire data, validate ML feasibility, prove core prediction accuracy
2. **Pilot & Learn** (Months 5-6): Small user group validation, real-time accuracy tracking
3. **Scale & Refine** (Months 7-12): Public launch, model improvements, feature expansion

### Timeline At-A-Glance

```
Month 1-2   : Data Acquisition & Engineering
Month 2-3   : ML Model Development & Validation
Month 3-4   : MVP Web UI + Deployment
Month 5-6   : Pilot User Group + Real-Time Validation
Month 7-8   : Public Launch + SEO/Marketing
Month 9-12  : Feature Expansion (v2)
```

---

## Phase 1: MVP - Prove the Prediction Engine (Months 1-4)

**Goal**: Validate that ML can accurately predict LPMA disruptions with >80% accuracy on historical data, deploy functional prototype for pilot users.

**Context**: Solo developer, 2-4 month rapid prototype timeline confirmed with user.

### Month 1-2: Data Acquisition & Engineering

**Objective**: Build clean, labeled dataset from 20+ years of METAR data + ANAC operational rules.

#### Tasks

**Week 1-2: METAR Data Acquisition**
- [ ] Research Iowa State University ASOS-AWOS-METAR API access (primary source per research)
- [ ] Identify NOAA Aviation Weather Center historical data endpoints
- [ ] Acquire 2004-2024 METAR/TAF archives for LPMA (ICAO code)
- [ ] Document data schema: timestamp, wind speed, wind direction, gusts, visibility, temp, pressure, runway
- [ ] Estimate dataset size (20 years × 24 observations/day × 365 days ≈ 175,000 records)

**Week 3-4: Data Engineering Pipeline**
- [ ] Set up PostgreSQL + TimescaleDB (research-validated for time-series weather data)
- [ ] Create hypertables for `metar_observations` with time-based partitioning
- [ ] Implement data ingestion scripts (Python + pandas)
- [ ] Data cleaning: Handle missing values, outliers, format inconsistencies
- [ ] Feature engineering: Derived features (wind sector classification, time-of-day, seasonality)

**Week 5-6: Rule-Based Labeling**
- [ ] Implement ANAC wind limit rules engine (per sector from research):
  - Sector 120°-190° MAG: RW05 20kt max, RW23 15kt max, gusts 30/25kt
  - Sector 200°-230° MAG: 25kt max
  - Sector 300°-015°: 20kt max
  - Sector 015°-040°: 25kt max
- [ ] Apply rules to METAR data → Generate binary labels (Disruption: True/False)
- [ ] Validate labeling against known disruption events (Aug 2024: 59 cancellations, 24 diversions)

**Week 7-8: Media Correlation Research (Manual MVP Phase)**
- [ ] Manually scrape news articles for LPMA disruptions (2020-2024 focus)
- [ ] Target sources: The Portugal News, Madeira Island Direct, FlightRadar24 blog
- [ ] Extract dates of "mass disruption" events
- [ ] Cross-reference with rule-based labels for validation accuracy
- [ ] Build ground truth validation dataset (100-200 labeled events minimum)

**Deliverables**:
- ✅ 175K+ METAR records in TimescaleDB
- ✅ Rule-based labeling engine (Python module)
- ✅ Ground truth validation set (100-200 events)
- ✅ Data quality report (missing data %, outliers, label distribution)

**Dependencies**:
- Access to Iowa State/NOAA METAR archives (public, but may need API keys)

**Risks**:
- **Data gaps** (Medium): Some historical METAR observations missing → Mitigation: Interpolate missing hours or exclude incomplete days
- **Labeling noise** (High): Rule-based labels may not perfectly match actual disruptions → Mitigation: Media correlation refines labels

---

### Month 2-3: ML Model Development & Validation

**Objective**: Train XGBoost binary classifier achieving >80% accuracy on hold-out test set.

#### Tasks

**Week 9-10: Exploratory Data Analysis & Feature Engineering**
- [ ] Analyze label distribution (class imbalance: expect 10-20% disruption rate)
- [ ] Feature correlation analysis: Which weather variables most predictive?
- [ ] Time-series patterns: Seasonal trends, daily/weekly cycles
- [ ] Create lagged features (t-1, t-2, t-3 hours for temporal context per scikit-learn best practices)
- [ ] Encode categorical features: wind sector, runway in use, time-of-day bins

**Week 11-12: XGBoost Model Training**
- [ ] Train/validation/test split: 70% / 15% / 15% (time-series split: 2004-2018 train, 2019-2020 val, 2021-2024 test)
- [ ] Baseline model: XGBoost with default hyperparameters
- [ ] Hyperparameter tuning: max_depth, learning_rate (eta), n_estimators, gamma (per Context7 /dmlc/xgboost best practices)
- [ ] Handle class imbalance: scale_pos_weight parameter or SMOTE oversampling
- [ ] Model objective: `binary:logistic` for probability outputs (0-1 scale)

**Week 13: Model Evaluation & Validation**
- [ ] Metrics: Accuracy, Precision, Recall, F1-Score, ROC-AUC, Confusion Matrix
- [ ] Feature importance analysis: Which variables drive predictions?
- [ ] Temporal validation: Does model perform consistently across years?
- [ ] Error analysis: When does model fail? (Rare edge cases, microclimate events)
- [ ] Target: >80% accuracy (stretch goal: >85% per research benchmarks)

**Week 14: Model Experimentation (If Time Permits)**
- [ ] Baseline comparison: Logistic Regression, Random Forest
- [ ] Ensemble methods: Stacking XGBoost + other classifiers
- [ ] Future exploration: Prophet for time-series forecasting (uncertainty intervals)

**Deliverables**:
- ✅ Trained XGBoost model (.pkl file, serialized)
- ✅ Model evaluation report (accuracy, confusion matrix, feature importance)
- ✅ Jupyter notebook with EDA and training pipeline
- ✅ Model achieves >80% accuracy on test set (success criterion)

**Dependencies**:
- Clean, labeled dataset from Phase 1

**Risks**:
- **Accuracy below threshold** (High): Complex orographic effects hard to capture → Mitigation: Add terrain/elevation features, try ensemble methods
- **Overfitting** (Medium): Model memorizes training data, poor generalization → Mitigation: Cross-validation, regularization (gamma, min_child_weight)

---

### Month 3-4: MVP Web UI + Deployment

**Objective**: Deploy functional web app with real-time METAR ingestion for pilot user group (10-100 users).

#### Tasks

**Week 15-16: Backend API Development**
- [ ] FastAPI REST API setup (per Context7 /websites/fastapi_tiangolo best practices)
- [ ] Endpoints:
  - `GET /api/v1/forecast` → Returns current disruption status + 24-48h forecast
  - `GET /api/v1/status` → Health check, model version, last METAR update timestamp
- [ ] Model inference: Load XGBoost model, predict on latest METAR data
- [ ] Redis caching: Cache predictions for 30min to reduce compute (per scaling research)
- [ ] Background tasks: Use FastAPI BackgroundTasks for async logging

**Week 17: Real-Time METAR Ingestion (Celery)**
- [ ] Set up Celery + Redis for task queue
- [ ] Periodic task: Fetch latest METAR/TAF from Aviation Weather Center every 30-60min
- [ ] Parse METAR data (use existing Python libraries: python-metar or metar-parser)
- [ ] Store in TimescaleDB, trigger model inference
- [ ] Error handling: Retry logic, alerting if data feed fails

**Week 18: Frontend Web UI**
- [ ] Simple single-page web app (React or vanilla JS + Tailwind CSS for minimalism)
- [ ] Components:
  - Traffic-light status indicator (Green/Yellow/Red with animation)
  - Confidence score (e.g., "73% disruption risk")
  - 24-48h timeline forecast (chart with hourly predictions)
  - Last updated timestamp
- [ ] Mobile-responsive design (80% of users on mobile)
- [ ] Accessibility: WCAG AA compliance for color contrast (anxiety-reducing design)

**Week 19: Deployment & DevOps**
- [ ] Dockerize application (FastAPI backend, Celery worker, Redis, PostgreSQL, Frontend)
- [ ] Deploy to cloud (AWS EC2/Lightsail or GCP Cloud Run - low-cost options for MVP)
- [ ] Set up monitoring: Uptime (UptimeRobot), error tracking (Sentry), logs (CloudWatch/GCP Logs)
- [ ] Domain + SSL: Register domain (e.g., lpmaweather.com), configure HTTPS
- [ ] CI/CD: Basic GitHub Actions for automated deployment on push to main

**Deliverables**:
- ✅ FastAPI backend with /forecast endpoint (< 100ms response time with Redis caching)
- ✅ Celery scheduled tasks fetching METAR every 30-60min
- ✅ Mobile-friendly web UI with traffic-light status
- ✅ Deployed to production (99%+ uptime target)
- ✅ Monitoring and alerting configured

**Dependencies**:
- Trained model from Month 2-3
- METAR API access for real-time data

**Risks**:
- **METAR API outages** (Low): Aviation Weather Center downtime → Mitigation: Fallback to secondary source (e.g., CheckWX API)
- **Deployment complexity** (Medium): Solo developer managing full DevOps → Mitigation: Use managed services (AWS RDS for PostgreSQL, managed Redis)

---

## Phase 2: Pilot User Group + Real-Time Validation (Months 5-6)

**Goal**: Validate product-market fit with 10-100 pilot users, track real-time prediction accuracy vs actual LPMA operations.

### Month 5: Pilot Launch & Monitoring

#### Tasks

**Week 20-21: Pilot User Recruitment**
- [ ] Recruit 10-50 pilot users:
  - Personal network: Friends, family planning Madeira trips
  - Aviation forums: FlyerTalk, AvCanada LPMA discussion threads
  - Reddit: r/madeira, r/aviation (soft launch post: "Built a tool to predict LPMA disruptions...")
- [ ] Set up feedback mechanism: Google Form, email (founder@lpmaweather.com)
- [ ] Set expectations: "Beta product, prediction accuracy improving, your feedback invaluable"

**Week 22-23: Real-Time Validation Tracking**
- [ ] Build internal tracking system:
  - Log all predictions (timestamp, forecast, confidence)
  - Scrape actual LPMA operations (FlightAware API or manual): cancellations, diversions, delays
  - Compare predictions vs actuals daily
- [ ] Accuracy dashboard (internal Streamlit app):
  - Daily accuracy %, confusion matrix, false positive/negative analysis
  - Trend tracking: Is accuracy improving week-over-week?
- [ ] Iterative model improvements: Retrain on new data weekly

**Week 24: User Feedback Analysis**
- [ ] Synthesize qualitative feedback: What users love, what confuses them
- [ ] Quantitative metrics: DAU, session frequency, bounce rate
- [ ] Identify product gaps: Do users want push notifications? Historical data?
- [ ] Prioritize v2 features based on feedback

**Deliverables**:
- ✅ 10-50 active pilot users checking forecasts
- ✅ Real-time accuracy tracking system operational
- ✅ Feedback collected and analyzed (>20 responses)
- ✅ Model accuracy improves to >82% (stretch: >85%)

**Dependencies**:
- MVP deployed and stable
- Access to actual LPMA operations data (FlightAware or manual tracking)

**Risks**:
- **Low pilot adoption** (Medium): Users don't return after first visit → Mitigation: Email updates with accuracy reports, ask for referrals
- **Accuracy stagnates** (High): Real-world performance worse than historical validation → Mitigation: Root cause analysis, model debugging, collect more edge case data

---

### Month 6: Refinement & Pre-Launch Prep

#### Tasks

**Week 25-26: Model Refinement**
- [ ] Incorporate 2 months of real-time validation data into training set
- [ ] Retrain model with updated labels (validated actual disruptions)
- [ ] A/B test: Old model vs new model on pilot users (track accuracy)
- [ ] Deploy improved model to production

**Week 27: Product Polish**
- [ ] UI/UX improvements based on pilot feedback
- [ ] Add FAQ page: "How does this work? What data sources? How accurate?"
- [ ] About page: Mission, methodology, founder story
- [ ] SEO foundation: Meta tags, sitemap, Google Analytics setup

**Week 28: Launch Preparation**
- [ ] Write launch blog post: "Introducing LPMA Weather Disruption Predictor"
- [ ] Prepare social media content: Screenshots, demo video, testimonials
- [ ] Reach out to aviation media: Send press release to FlightRadar24, Aviation Week
- [ ] Set up email capture: Mailchimp/ConvertKit for launch announcements

**Deliverables**:
- ✅ Model accuracy >85% (validated on real-time data)
- ✅ Product polished based on pilot feedback
- ✅ Launch marketing materials ready
- ✅ SEO and analytics configured

**Dependencies**:
- Pilot phase feedback and data

**Risks**:
- **Launch readiness pressure** (Low): Rushing product before model is accurate → Mitigation: Delay launch if accuracy <82%, communicate openly with users

---

## Phase 3: Public Launch + Growth (Months 7-8)

**Goal**: Scale to 1,000+ DAU, establish product-market fit, achieve >85% prediction accuracy.

### Month 7: Public Launch

#### Tasks

**Week 29: Launch Campaign**
- [ ] Post launch announcement:
  - Reddit: r/madeira, r/portugal, r/aviation, r/travel
  - Hacker News: Show HN post with demo link
  - X/Twitter: Tag aviation influencers (@airlivenet, @flightradar24)
- [ ] Email pilot users: "We're live! Share with friends traveling to Madeira"
- [ ] Press outreach: Send to aviation blogs, travel media

**Week 30-32: Growth & SEO**
- [ ] SEO optimization: Target keywords "Madeira airport wind forecast," "LPMA disruptions," "Funchal flight cancellations"
- [ ] Content marketing: Blog posts "Understanding LPMA Wind Patterns," "How We Predict Disruptions"
- [ ] Backlinks: Reach out to travel blogs, Madeira tourism sites for mentions
- [ ] Monitor growth: Track DAU, traffic sources (Google Analytics), user retention

**Deliverables**:
- ✅ 1,000+ DAU within 4 weeks of launch
- ✅ Featured on 2-3 aviation/travel media outlets
- ✅ Organic traffic growing (100+ visits/day from Google search)

**Dependencies**:
- Product accurate and stable (>85% accuracy maintained)

**Risks**:
- **Launch fizzles** (Medium): Low viral traction, user growth stagnates → Mitigation: Paid ads (Google, Facebook) targeting Madeira travelers, partnership with booking platforms

---

### Month 8: Monetization Experiments (Optional MVP+)

#### Tasks

**Week 33-36: Monetization Testing**
- [ ] A/B test: Introduce "Donate / Support" button (voluntary contributions)
- [ ] Premium features brainstorm: What would users pay for?
  - Push notifications (iOS/Android via web push)
  - Historical accuracy data (transparency report)
  - Flight-specific forecasts (API integration with FlightAware)
- [ ] B2B outreach: Email airlines (TAP Portugal, easyJet), booking platforms (Booking.com, Expedia) for white-label API partnership
- [ ] Revenue target: $0-500 MRR (not goal for MVP, but exploratory)

**Deliverables**:
- ✅ Monetization hypothesis tested (donations or premium features)
- ✅ 1-2 B2B partnership conversations initiated

**Dependencies**:
- Strong user adoption (1,000+ DAU) demonstrates value

**Risks**:
- **Premature monetization** (Medium): Introducing fees before product-market fit kills growth → Mitigation: Keep core free, premium features optional

---

## Phase 4: Feature Expansion (v2) (Months 9-12)

**Goal**: Increase user retention, deepen value proposition with advanced features.

### Month 9-10: Push Notifications & Alerts

#### Tasks

- [ ] Implement web push notifications (using Firebase Cloud Messaging or OneSignal)
- [ ] Alert logic: Notify users when status changes (Green → Yellow or Yellow → Red)
- [ ] User preference settings: Opt-in/opt-out, notification frequency
- [ ] Email alerts: Alternative for users who prefer email over push

**Deliverables**:
- ✅ Push notifications live
- ✅ 20% of users opt-in to alerts

**Research Citation**: User retention increases 30-50% with well-timed push notifications (mobile app best practices research)

---

### Month 11: Historical Accuracy Dashboard (Public Transparency)

#### Tasks

- [ ] Public-facing dashboard: "Our Prediction Accuracy Over Time"
- [ ] Monthly accuracy charts, confusion matrices, case studies
- [ ] Build trust through transparency: "We predicted 87% of disruptions in Dec 2026"
- [ ] Blog posts: Deep-dives on model improvements, interesting disruption events

**Deliverables**:
- ✅ Public accuracy dashboard
- ✅ Trust signal: Users cite dashboard in testimonials/reviews

---

### Month 12: Prophet Integration & Uncertainty Intervals

#### Tasks

- [ ] Integrate Prophet (/facebook/prophet) for time-series forecasting
- [ ] Add uncertainty intervals to forecasts: "70% confidence: 50-80% disruption risk"
- [ ] Seasonal pattern analysis: "November-February highest disruption months"
- [ ] Long-range forecasts: 7-day outlook (experimental feature)

**Deliverables**:
- ✅ Uncertainty intervals displayed in UI
- ✅ Prophet model running alongside XGBoost (ensemble predictions)

**Research Citation**: Prophet enables uncertainty quantification via MCMC sampling (per Context7 /facebook/prophet best practices)

---

## Feature Prioritization Framework

**Must-Have (MVP)**:
- Core ML prediction engine ✅
- Real-time METAR ingestion ✅
- Simple web UI (traffic-light status) ✅

**Should-Have (v1)**:
- Real-time validation tracking ✅
- Public launch + SEO ✅
- Model retraining pipeline ✅

**Nice-to-Have (v2)**:
- Push notifications 📱
- Historical accuracy dashboard 📊
- Prophet uncertainty intervals 📈

**Future Exploration (v3+)**:
- ADS-B integration for real-time flight tracking
- Multi-airport expansion (Gibraltar, Innsbruck)
- Native mobile apps (iOS/Android)
- B2B white-label API

---

## Dependencies and Blockers

### External Dependencies

1. **METAR Data Availability**: Iowa State/NOAA archives accessible (public, low risk)
2. **Real-Time METAR Feed**: Aviation Weather Center API stable (government service, high reliability)
3. **Cloud Infrastructure**: AWS/GCP uptime (99.9%+ SLA, low risk)
4. **ANAC Wind Limit Stability**: 2026 review may change limits → **Monitor ANAC announcements Q1-Q2 2026**

### Internal Dependencies

1. **Solo Developer Capacity**: All tasks sequential (no parallelization) → **Timeline assumes full-time focus**
2. **Data Engineering Success**: If METAR acquisition fails, entire timeline delays → **Mitigate: Start with data acquisition immediately**
3. **Model Accuracy Threshold**: If <80% accuracy, may need to pivot approach → **Mitigate: Budget 2 weeks for model experimentation**

---

## Risk Mitigation Strategies

### Top 3 Risks

1. **Model Accuracy Below Threshold** (High Impact)
   - Mitigation: Start with simple XGBoost baseline, iterate with ensemble methods, collect more ground truth data
   - Contingency: Extend MVP timeline by 1 month for additional model R&D

2. **Data Acquisition Delays** (High Impact)
   - Mitigation: Allocate 6 weeks instead of 4 for data engineering (buffer time)
   - Contingency: Consider paid data providers (CheckWX, Weather Source) if free sources inadequate

3. **Low User Adoption in Pilot** (Medium Impact)
   - Mitigation: Actively solicit feedback, iterate on UX rapidly, offer incentives (e.g., early access to premium features)
   - Contingency: Extend pilot phase, recruit more users via targeted ads

---

## Success Criteria by Phase

| Phase | Success Metric | Target | Status |
|-------|---------------|--------|--------|
| MVP (Month 1-4) | Model accuracy (historical validation) | >80% | Pending |
| MVP (Month 1-4) | MVP deployed to production | 99%+ uptime | Pending |
| Pilot (Month 5-6) | Pilot user adoption | 10-50 active users | Pending |
| Pilot (Month 5-6) | Real-time accuracy | >82% | Pending |
| Launch (Month 7-8) | Public user adoption | 1,000+ DAU | Pending |
| Launch (Month 7-8) | Sustained accuracy | >85% | Pending |
| v2 (Month 9-12) | User retention | 30% return users | Pending |

---

## Research Citations

This roadmap is informed by research on ML development timelines, solo developer productivity, and aviation weather data pipelines.

### Technology & Architecture Research

- **METAR data sources**: [METAR Data Engineering Project](https://github.com/MarieeCzy/METAR-Data-Engineering-and-Machine-Learning-Project) - Real-world pipeline taking 2-4 weeks for data acquisition/cleaning
- **Time-series database**: [TimescaleDB for Weather Data](https://maddevs.io/writeups/time-series-data-management-with-timescaledb/) - Hypertables, continuous aggregates, compression best practices
- **XGBoost training**: Context7 /dmlc/xgboost - Binary classification, hyperparameter tuning, class imbalance handling
- **FastAPI production patterns**: Context7 /websites/fastapi_tiangolo - BackgroundTasks, async operations, Redis caching
- **Celery scheduling**: Context7 /websites/celeryq_dev_en_stable - Periodic tasks for real-time data ingestion

### Domain & Market Research

- **LPMA wind limits**: [Madeira Airport Wind Limits](https://madeiraspotting.com/madeira-airport-wind-limits/) - ANAC operational rules per sector
- **Historical disruptions**: [80+ Diversions Event](https://www.flightradar24.com/blog/aviation-news/madeira-airport-sees-over-80-flight-diversions-and-cancellations/) - Validates disruption frequency
- **ML weather accuracy benchmarks**: [Probabilistic Weather Forecasting (Nature)](https://www.nature.com/articles/s41586-024-08252-9) - 88-89% accuracy achievable for classification

---

**Roadmap Version**: 1.0
**Next Review**: End of Month 2 (after data acquisition phase complete)
**Owner**: Solo Founder/Developer
