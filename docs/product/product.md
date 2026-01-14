# Product Vision: LPMA Weather Disruption Predictor

**Status**: Concept → MVP Development
**Last Updated**: 2026-01-08
**Owner**: Product Team

---

## Executive Summary

The LPMA Weather Disruption Predictor is a machine learning-driven application that predicts flight disruption probability at Madeira Airport (LPMA) caused by the island's notorious wind conditions. By translating complex meteorological data and aviation safety protocols into simple, actionable insights, we empower travelers to manage expectations and plan accordingly.

**Target Users**: Passengers flying to/from Madeira (B2C)
**Differentiation**: Hyper-local LPMA expertise, operational impact translation, proprietary ML model with 20+ years validation
**MVP Timeline**: 2-4 months (rapid prototype)
**Success Metrics**: >85% prediction accuracy, growing daily active user base

---

## The Problem

### Problem Statement

Madeira Airport (LPMA) is **the only airport in the world with mandatory wind limits**, creating frequent flight disruptions that generate significant anxiety and logistical uncertainty for travelers. Current weather applications fail to translate raw meteorological data (METAR/TAF reports) into operational realities based on strict aviation safety protocols.

### Scope and Impact

**Operational Constraints**:
- LPMA has mandatory wind limits imposed by ANAC (Autoridade Nacional da Aviação Civil) since 1964
- Limits vary by wind sector and runway in use (15-25 knots depending on sector)
- Runway 05/23 surrounded by tall mountains creating turbulence, windshear, orographic effects
- Only captain allowed to land/takeoff (special LPMA certification required)
- Mandatory visual approach despite challenging terrain

**Current Disruption Patterns** (validated by research):
- August 2024 event: 59 cancellations + 24 diversions in 48 hours (19% of departing flights affected)
- Departure delays average 33 minutes (12% of flights)
- Arrival delays average 57 minutes (9% of flights)
- Common diversions to Lisbon (LIS), Tenerife South (TFS), Porto Santo (LPPS)

### Why Current Solutions Fall Short

**General Weather Apps** (ForeFlight, Windy.com, Aviation Weather Center):
- Show raw METAR data but don't interpret operational impact
- Don't understand ANAC-specific wind limits per sector (120°-190° MAG, 200°-230° MAG, 300°-015°, 015°-040°)
- Provide generic forecasts, not LPMA-specific Go/No-Go predictions
- Overwhelming data for non-pilots, causing anxiety rather than clarity

**Flight Tracking Apps** (FlightAware, Flightradar24):
- Show real-time status but no predictive capability
- Reactive (you learn about disruptions after booking/arriving at airport)
- No historical pattern analysis or probability forecasting

**Gap in Market**: No product specifically translates LPMA's unique meteorological challenges and ANAC operational constraints into passenger-friendly disruption probability forecasts.

---

## Our Solution

### Product Overview

A minimalistic web application that provides:

1. **Traffic-Light Disruption Status** (Green/Yellow/Red)
   - Green: Low disruption risk (<20% probability)
   - Yellow: Moderate disruption risk (20-60% probability)
   - Red: High disruption risk (>60% probability)

2. **Confidence Scores**: Clear percentage probability of disruption (e.g., "73% chance of delays or diversions")

3. **Timeline Forecast**: 24-48 hour forecast view showing when conditions improve/worsen

4. **Real-Time Updates**: Automated METAR/TAF ingestion via Celery, updates every 30-60 minutes

### How It Works

**Data Foundation**:
- Ingest 20+ years of historical METAR data from Iowa State University ASOS-AWOS-METAR archive
- Real-time METAR/TAF data from Aviation Weather Center
- Structured storage in PostgreSQL + TimescaleDB (optimized for time-series queries)

**ML Prediction Engine**:
- **Rule-Based Labeling**: Operationalize ANAC wind limits to create ground truth "disruption labels"
  - Example: If wind 310° at 22 kt → exceeds Sector 300°-015° limit (20 kt max) → Label: Disruption
- **Media Correlation Validation**: Cross-reference with news reports of mass disruption events to validate labeling accuracy
- **Supervised ML Model**: XGBoost classifier trained on labeled historical data to predict disruption probability
- **Features**: Wind speed, wind direction, gusts, visibility, temperature, pressure, time-of-day, seasonality, runway in use
- **Output**: Probability score (0-100%) + confidence intervals

**User Experience**:
- Mobile-friendly web interface (no app install required for MVP)
- Single-page view: Current status + 24-48h timeline
- Minimal cognitive load: See status in <5 seconds
- Anxiety-reducing design: Clear, calm, actionable information

### Key Differentiators

1. **LPMA-Specific Hyper-Local Expertise**
   - Only product purpose-built for LPMA's unique operational constraints
   - Understands all ANAC wind limits per sector (120°-190°, 200°-230°, 300°-015°, 015°-040° MAG)
   - Accounts for terrain effects: orographic lift, windshear, turbulence from surrounding mountains

2. **Operational Impact Translation**
   - Converts raw weather data → Go/No-Go disruption probability
   - Speaks passenger language, not pilot/meteorologist jargon
   - Answers the question travelers actually care about: "Will my flight be affected?"

3. **Proprietary ML Model with 20+ Years Validation**
   - Trained on historical METAR data labeled with ANAC operational rules
   - Validated against documented disruption events (August 2024: 59 cancellations, 24 diversions)
   - Continuously improves: Real-time validation against actual LPMA operations

---

## Target Users

### Primary Persona: The Anxious Traveler

**Demographics**:
- Passengers flying to/from Madeira (tourists, business travelers, returning residents)
- International travelers unfamiliar with LPMA's unique challenges
- Age: 25-65, digitally savvy, mobile-first

**Behaviors**:
- Books flights to Madeira weeks/months in advance
- Anxiously checks weather forecasts days before departure
- Googles "Madeira airport wind problems" and finds scary pilot forum discussions
- Arrives at origin airport uncertain whether flight will actually land in Funchal

**Pain Points**:
- **Uncertainty**: "Will my flight be cancelled or diverted?"
- **Anxiety**: "Should I have booked the earlier/later flight?"
- **Information Gap**: "What does '15 knot crosswind at 310°' mean for my flight?"
- **Planning Challenges**: "Do I need to book a backup plan?"

**Jobs to Be Done**:
- Know disruption risk before booking flights (choose less risky times)
- Check probability 1-2 days before departure (prepare contingency plans)
- Monitor status morning-of-flight (adjust airport arrival timing)
- Understand when conditions improve (reschedule if needed)

**Success Criteria**:
- Reduced anxiety through transparency and clarity
- Ability to make informed travel decisions
- Peace of mind from accurate, timely forecasts

---

## Market Opportunity

### Market Size

**Total Addressable Market (TAM)**: Aviation AI/ML Technology Market
- Aircraft computers market: **$2.58B (2025) → $5.19B (2035)** at 15% CAGR
- Aviation AI/ML growing at double-digit annual rate for predictive operations

**Serviceable Addressable Market (SAM)**: Flight Disruption Management Tools
- Subset of aviation weather/operations tools (no specific market size data available for "airport-specific disruption prediction")
- Aviation weather services market (ForeFlight, FlightAware subscriptions): ~$500M annually

**Serviceable Obtainable Market (SOM)**: LPMA-Specific Users
- Madeira Airport traffic: ~3.8M passengers annually (2023)
- Target capture: 1-5% of passengers (38K-190K potential users in first 2 years)
- Conversion target: 10-100 daily active users in MVP pilot phase

**Market Trend**: Airlines and airports increasingly using AI for operations efficiency and cost reduction (2026 industry trend). Passengers demand transparency and control over travel disruptions.

### Competitive Landscape

**Researched Competitors**:

1. **ForeFlight** (Market Leader)
   - **Strengths**: Comprehensive aviation weather suite ($100/year subscription), trusted by pilots, METARs/TAFs/SIGMETs integration
   - **Weaknesses**: Pilot-focused (complex for passengers), generic weather (no LPMA-specific operational translation), expensive for casual travelers
   - **Positioning**: Professional aviation tool vs our passenger-friendly predictor

2. **FlightAware** (Flight Tracking)
   - **Strengths**: Real-time flight tracking, delay alerts
   - **Weaknesses**: Reactive (not predictive), no weather-to-operations translation, no LPMA specificity
   - **Positioning**: "What's happening now" vs our "What will happen in 24-48h"

3. **Windy.com, ClimaVision, General Aviation Weather Apps**
   - **Strengths**: Beautiful visualizations, ECMWF/GFS weather models, free/freemium
   - **Weaknesses**: Generic global weather, no airport-specific operational limits, no disruption probability
   - **Positioning**: General weather enthusiasts vs our LPMA-targeted passengers

4. **Aviation Weather Center (NOAA/FAA)**
   - **Strengths**: Authoritative, free, comprehensive
   - **Weaknesses**: Government site UX, pilot jargon, no predictive ML, no mobile optimization
   - **Positioning**: Official source vs our user-friendly interpretation

**White Space**: No product combines LPMA-specific operational expertise, ML-driven probability forecasting, and passenger-friendly UX. We occupy a unique niche.

---

## Product Principles

1. **Anxiety-Reducing Simplicity**: Information architecture prioritizes clarity over comprehensiveness. Show only what matters: current risk, forecast trend, confidence level.

2. **Transparency & Trust**: All predictions cite data sources and model confidence. Users understand *why* a forecast says "Red."

3. **Operational Accuracy Over Weather Accuracy**: We predict disruptions (operational outcome), not just weather. ANAC rules + terrain effects + historical patterns inform model.

4. **Privacy-First**: No user accounts or personal data required for MVP. Free, anonymous access builds trust and adoption.

5. **Continuous Learning**: Model improves through real-time validation. Every actual disruption event refines predictions.

---

## Success Metrics

### Primary Metrics

**1. Prediction Accuracy** (Target: >85%)
- **Definition**: Percentage of correct disruption forecasts validated against actual LPMA operations
- **Measurement**:
  - Historical validation: Cross-validation on 2004-2020 train data, test on 2021-2024
  - Real-time validation: Compare 24h forecast vs actual disruptions over 3-6 months post-launch
- **Benchmark**: Weather ML research shows 88-89% accuracy achievable for classification tasks
- **Why It Matters**: Trust is everything. Inaccurate predictions = user churn + reputational damage

**2. User Adoption** (Target: 10-100 DAU in pilot phase, then 1K+ DAU)
- **Definition**: Daily active users checking disruption forecasts
- **Measurement**: Unique visits/day, returning visitor rate, session frequency
- **Growth Strategy**:
  - Pilot: Friends, family, aviation enthusiasts (10-100 users)
  - Launch: Reddit (r/madeira, r/aviation), aviation forums, social media (1K-10K users)
  - Scale: SEO for "Madeira airport wind," partnerships with booking platforms (10K+ users)
- **Why It Matters**: Product-market fit indicator. Users return when predictions prove valuable.

### Secondary Metrics

**3. User Engagement**
- Time on site, bounce rate, forecast check frequency
- Target: Users check forecast 1-3 days before flight + morning-of-flight

**4. Forecast Utility**
- User-reported: "Did this forecast help you plan?" (future feature)
- Qualitative feedback via social media mentions, email

**5. Technical Performance**
- API response time (<100ms target with Redis caching)
- Uptime (99%+ target), METAR data freshness (<60min lag)

---

## Vision Timeline

### Phase 1: MVP Launch (Months 1-4)

**Goal**: Validate core prediction engine with small pilot group

**Deliverables**:
- Acquire 20+ years METAR data from Iowa State/NOAA (4-6 weeks data engineering)
- Build XGBoost binary classification model with ANAC rule-based labeling
- Simple web UI (traffic-light status, 24-48h forecast, confidence %)
- Automated METAR/TAF ingestion via Celery (every 30-60min)
- PostgreSQL + TimescaleDB time-series database
- Deploy on cloud (AWS/GCP), Docker containerized

**Success Criteria**:
- Model achieves >80% accuracy on historical validation set
- 10-100 pilot users actively checking forecasts
- Technical infrastructure stable (99%+ uptime)

### Phase 2: Public Launch & Validation (Months 5-8)

**Goal**: Scale to broader aviation community, refine model with real-time data

**Deliverables**:
- SEO optimization ("Madeira airport disruption forecast" keyword targeting)
- Social media launch (Reddit, X/Twitter aviation accounts)
- Real-time validation tracking: Forecast vs actual disruptions
- Model retraining pipeline based on new data
- Basic analytics dashboard (internal use: track accuracy trends)

**Success Criteria**:
- 1,000+ DAU checking forecasts
- >85% prediction accuracy on real-time validation
- Positive user feedback (qualitative testimonials, social media sentiment)

### Phase 3: Feature Expansion (Months 9-12)

**Goal**: Increase user retention and utility

**Deliverables**:
- Push notifications / email alerts for status changes
- Historical accuracy dashboard (public: "We predicted 87% of disruptions in Dec 2026")
- Prophet integration for seasonal pattern analysis + uncertainty intervals
- Flight-specific recommendations (future: "Your TAP123 flight has 68% disruption risk")

**Success Criteria**:
- 5,000+ DAU
- 30% user retention (users return for multiple trips)
- Monetization experiments (freemium, optional premium features)

### Long-Term Vision (Year 2+)

- **ADS-B Integration**: Real-time flight tracking + approach monitoring for post-facto validation
- **Multi-Airport Expansion**: Apply methodology to other wind-sensitive airports (Gibraltar, Innsbruck, Toncontin)
- **B2B Partnerships**: White-label API for airlines, booking platforms, travel agencies
- **Native Mobile Apps**: iOS/Android with push notifications, offline mode
- **Community Features**: User-reported disruptions, traveler Q&A forum

---

## Risks and Assumptions

### Key Assumptions

1. **Data Availability**: Iowa State/NOAA METAR archives provide sufficient historical data (20+ years) for model training
   - **Validation**: Confirmed via research - Iowa Environmental Mesonet is standard source for METAR data

2. **ANAC Wind Limits Stability**: Current operational limits remain consistent, or 2026 review maintains similar thresholds
   - **Risk**: ANAC reviewing limits in 2026 after €4.5M wind equipment upgrade (may relax limits, reducing disruption frequency)

3. **Model Generalizability**: Patterns learned from 2004-2020 data apply to 2026+ weather patterns
   - **Mitigation**: Continuous retraining with new data, real-time validation monitoring

4. **User Demand**: Travelers genuinely want predictive disruption information and will use it to inform decisions
   - **Validation**: Pilot phase with 10-100 users will test demand hypothesis

5. **Accuracy Threshold**: 85% prediction accuracy is "good enough" for users to trust and adopt
   - **Benchmark**: Weather ML research shows 88-89% achievable; aviation forecasting is inherently uncertain

### Key Risks

1. **Data Acquisition Challenges** (High Impact, Medium Likelihood)
   - METAR data harder to obtain than expected (API rate limits, cost, quality issues)
   - News scraping for validation blocked by anti-bot measures
   - **Mitigation**: Budget 4-6 weeks for data engineering, consider paid data provider partnerships

2. **Model Accuracy Below Threshold** (High Impact, Medium Likelihood)
   - Complex orographic effects + microclimate at LPMA harder to model than anticipated
   - 20 years data insufficient for rare edge cases
   - **Mitigation**: Start with simpler model (XGBoost), iterate with ensemble methods, Prophet for uncertainty

3. **Competitive Response** (Medium Impact, Low Likelihood)
   - ForeFlight or FlightAware adds LPMA-specific feature
   - **Mitigation**: First-mover advantage, hyper-local expertise moat, free/freemium barrier to entry

4. **Regulatory/Legal** (Low Impact, Low Likelihood)
   - ANAC objects to public disruption forecasts (perceived interference with operations)
   - Data usage terms violated (scraping restrictions)
   - **Mitigation**: Public data only, add disclaimers ("For informational purposes, not flight planning"), consult aviation lawyer if needed

5. **Seasonality/Low Disruption Periods** (Medium Impact, Medium Likelihood)
   - Summer months may have minimal disruptions, reducing perceived value
   - **Mitigation**: Historical data dashboard shows long-term accuracy, market to winter travelers (peak disruption season)

---

## Research Citations

This product vision is informed by comprehensive research across technology, market, domain, and compliance areas.

### Technology Documentation (Context7)

- **FastAPI** (/websites/fastapi_tiangolo): Production ML API patterns, BackgroundTasks for async operations, high-performance REST API design
- **scikit-learn** (/websites/scikit-learn_stable): Time-series forecasting with lagged features, probability classification best practices
- **Celery** (/websites/celeryq_dev_en_stable): Periodic task scheduling for real-time data ingestion
- **XGBoost** (/dmlc/xgboost): Binary classification with probability prediction for imbalanced weather data
- **Prophet** (/facebook/prophet): Time-series forecasting with seasonality and uncertainty intervals (MCMC sampling)
- **PyTorch** (/pytorch/pytorch): LSTM sequence-to-sequence models for advanced time-series forecasting

### Market & Competitive Research (WebSearch)

- Market size: [Aviation Weather ML APIs](https://www.weathercompany.com/blog/the-foundation-of-flight-low-latency-high-scale-aviation-weather-apis-for-modern-airline-operations/)
- Competitors: [Top Aviation Weather Apps 2025](https://ipadpilotnews.com/2025/06/the-10-best-weather-apps-for-pilots-2025-edition/)
- ForeFlight weather services: [ForeFlight Weather Features](https://foreflight.com/products/foreflight-mobile/weather/)
- Industry trends: [Aviation 2026 Innovation Trends](https://www.cockpitinnovation.com/aviation-news/news/aviation-2026-between-technological-acceleration-and-a-shaky-geopolitical-reality-part-ii/)

### Domain-Specific Research (WebSearch + Academic)

- LPMA wind limits: [Madeira Airport Wind Limits](https://madeiraspotting.com/madeira-airport-wind-limits/)
- Only airport with mandatory limits: [Funchal Airport Winds](https://ops.group/blog/funchal-airport-winds/)
- ANAC review 2026: [Airport Wind Limit Review](https://www.madeiraislanddirect.com/blog/2023/05/airport-wind-limit-to-be-reviewed/)
- Terrain & orographic effects: [Madeira Airport Wikipedia](https://en.wikipedia.org/wiki/Madeira_Airport)
- Historical disruptions: [80+ Flight Diversions Event](https://www.flightradar24.com/blog/aviation-news/madeira-airport-sees-over-80-flight-diversions-and-cancellations/)
- Academic study: [Air-Traffic Restrictions at LPMA](https://www.mdpi.com/2073-4433/11/11/1257)

### Architecture & Security Research (WebSearch)

- Scalability patterns: [Scaling FastAPI ML to 1M predictions/hour](https://medium.com/@connect.hashblock/how-i-scaled-a-fastapi-ml-inference-server-to-handle-1m-predictions-per-hour-6c2424aa4faf)
- METAR processing: [METAR ML Engineering Project](https://github.com/MarieeCzy/METAR-Data-Engineering-and-Machine-Learning-Project)
- Time-series database: [TimescaleDB for Weather Data](https://maddevs.io/writeups/time-series-data-management-with-timescaledb/)
- GDPR compliance: [Aviation Data Protection](https://www.numberanalytics.com/blog/aviation-data-protection-laws-guide/)
- ML weather forecasting: [Probabilistic Weather Forecasting with ML (Nature)](https://www.nature.com/articles/s41586-024-08252-9)

---

**Document Version**: 1.0
**Next Review**: After MVP pilot phase (Month 4)
