# 🏙️ Local Air Quality Data Engineering Pipeline (wip)

> A data engineering project to monitor and visualise air quality in areas of London that are personally relevant using modern tools like Airflow, dbt, BigQuery, and Looker Studio on Google Cloud.

![Build](https://img.shields.io/badge/status-active-brightgreen)
![GCP](https://img.shields.io/badge/cloud-Google--Cloud-blue)
![Licence: MIT](https://img.shields.io/badge/licence-MIT-lightgrey)

---

## Project Background

Air quality can significantly impact health and wellbeing, particularly in cities like London. This project aims to increase the visibility of air pollution levels in any chosen area, to protect our long-term health. I achieve this by:

- Tracking historical air quality near my home, workplace, and areas I frequent.
- Visualise trends over time and analyse pollutant levels.
- Building a robust, scalable data pipeline using industry-standard tools.

This project can be modified to extract and analyse data for any location to suit the user's interests.

---

## Architecture and Tools

![Architecture Diagram](./docs/local_air_quality_architecture.png)

| Layer           | Tool / Service                     | Purpose                                     |
|----------------|------------------------------------|---------------------------------------------|
| Data Ingestion | [OpenWeather API](https://openweathermap.org/api/air-pollution) | Source of historical air quality data        |
| Orchestration  | [Apache Airflow](https://airflow.apache.org/) | Automates ingestion                |
| Infrastructure | [Google Cloud Platform](https://cloud.google.com/), [Terraform](https://www.terraform.io/) | Cloud services and provisioning             |
| Storage        | Google Cloud Storage               | Stores raw and intermediate data             |
| Processing     | [dbt](https://www.getdbt.com/) + [BigQuery](https://cloud.google.com/bigquery) | Transforms and models data                   |
| Visualisation  | [Looker Studio](https://lookerstudio.google.com/) | Interactive dashboard for analytics         |
| Containerisation | [Docker](https://www.docker.com/) | Local development and portability           |

> **Keywords**: data engineering, air quality, GCP, Apache Airflow, dbt, BigQuery, Looker Studio, ETL pipeline, Terraform, London air pollution

---

## Data Flow Summary

1. **Ingestion**
   - Airflow DAGs fetch air quality metrics (e.g. PM2.5, PM10, NO₂) as JSON data from the OpenWeather API.
   - Data is serialised and stored in **Google Cloud Storage** as parquet files.

2. **Transformation**
   - `dbt` models raw data within **BigQuery**, applying logic like deduplication, enrichment, and timestamp conversion.

![DBT Lineage](./docs/local_air_quality_dbt_lineage.png)

3. **Visualisation**
   - Cleaned datasets are explored using **Looker Studio**, enabling analysis by location, pollutant, and time.

![Looker Studio Dashboard](./docs/dashboard.png)

---

##

Instructions for setting up the environment, deploying infrastructure with Terraform, running Airflow, and managing dbt models will be provided in the Setup section below.

---

## Future Improvements

- Build tables incrementally instead of a full data refresh.
- Schedule hourly pipline runs to update the dashboard in line with the API data frequency.
- Encompass DBT transformation in Airflow DAG.
- Add data quality tests e.g. anomaly detection and threshold-based alerts.
- Implement CI/CD for pipeline updates.
- Allow for more seamless changes to air quality measurment locations.
- Enrich data with local weather information.

---

## Acknowledgements

- [OpenWeather](https://openweathermap.org/) for free API access.
- Open-source contributors to Airflow, dbt, Terraform, and the GCP ecosystem.
- [DataTalksClub](https://datatalks.club/) for inspiration and learning material.

---

## Setup & Deployment

**WARNING: You will be charged for all the GCP infra setup. You can obtain 300$ in credits for free by creating a new account on GCP.**
### Pre-requisites

The following instructions can be performed in any Ubuntu distribution. I used a WSL2 instance on my local machine for the intial project set up. I am yet to add Windows/macOS setup instructions.

Clone the repository in your local machine.

```bash
git clone https://github.com/gilsegev99/local-air-quality.git
```

If you already have a Google Cloud account and a working terraform setup, you can skip the pre-requisite steps.

- Google Cloud Platform.
  - [GCP Account and Access Setup](setup/gcp.md)


- Procure infra on GCP with Terraform - [Setup](setup/terraform.md)

# Setup Infrastructure

#### [Setup Reference - Ankur Chavda](https://github.com/ankurchavda/streamify/README.md)
