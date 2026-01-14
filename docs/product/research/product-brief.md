# Product Briefing: LPMA Weather Disruption Predictor

## Product Vision
To provide travelers flying to or from Madeira Airport (LPMA) with a highly accurate, minimalistic, and intuitive tool for predicting flight disruptions caused by the island’s notorious wind conditions. By demystifying operational risks, we empower passengers to manage expectations and plan accordingly.

## The Problem
Madeira Airport is world-renowned for its challenging approach, where strong winds and turbulence frequently result in diverted flights, cancellations, and delays. For travelers, this creates significant anxiety and logistical uncertainty. Current general weather apps fail to translate raw meteorological data into operational realities based on strict aviation safety protocols.

## The Solution
We are building a machine learning-driven application that predicts the probability of operational disruptions at LPMA over specific future time windows. Unlike generic weather forecasts, our system is trained to understand the specific "Go/No-Go" criteria used by aviation authorities.

## Technical Stack & Architecture
The entire backend and analytical core will be built using **Python**, ensuring a unified ecosystem for data engineering, model development, and API services.

*   **Language:** Python 3.12+
*   **Data Engineering:** `pandas` and `numpy` for processing over 20 years of METAR data and real-time TAF/METAR ingestion.
*   **Machine Learning:** `scikit-learn` (or `PyTorch`/`XGBoost`) for training supervised models that map atmospheric conditions to disruption probabilities.
*   **Backend Framework:** `FastAPI` for a high-performance, asynchronous REST API to serve predictions to the client.
*   **Task Scheduling:** `Celery` or native Python async loops for fetching live weather data and updating predictions.

## Methodology
1.  **Data Ingestion:** The engine aggregates real-time aviation weather data with deep historical records.
2.  **Rule-Based Labeling:** We operationalize official ANAC wind limits (e.g., Sector 300°–010°: Max 15 knots landing) to create a baseline "disruption truth."
3.  **Validation via Media Correlation:** We cross-reference specific dates of reported mass disruptions (via media research) against our rule-based flags to validate and tune the correlation logic.
4.  **ML Prediction:** The model forecasts disruption probability based on forecasted weather parameters relative to these verified operational thresholds.

## User Experience (UX)
The interface will be strictly minimalistic to reduce user anxiety:
*   **Simple Status Indicators:** A traffic-light system (Green/Yellow/Red) for landing feasibility.
*   **Confidence Scores:** A clear percentage probability of disruption.
*   **Timeline View:** A clean forecast view for the next 24-48 hours.

## Future Roadmap
*   Integration of live flight tracking data (ADS-B) for real-time model reinforcement.
*   Push notifications for status changes.
*   Expansion to other wind-sensitive airports.

## Conclusion
This product bridges the gap between complex meteorological data and passenger peace of mind, turning operational opacity into transparent, actionable insight.
