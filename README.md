**GitHub Actions Monitoring
Project Description**

A Python-based monitoring project that retrieves GitHub Actions workflow run data, calculates basic metrics such as total runs, successful/failed runs, and success rate, and stores the results as JSON files in an AWS S3 bucket using a scheduled GitHub Actions workflow.

This project automates the monitoring of GitHub Actions workflow executions for a target repository.

A scheduled GitHub Actions workflow runs the monitoring process daily. It uses the GitHub REST API to retrieve workflow run information and calculates key CI/CD metrics such as:

Total number of workflow runs
Successful workflow runs
Failed workflow runs
Overall workflow success rate
Monitoring date

The calculated metrics are stored as a JSON file and automatically uploaded to an Amazon S3 bucket for historical storage.

After the monitoring process completes, an automated email report is sent with the latest workflow statistics and the overall status of the repository.

**Architecture**
**1. GitHub Actions starts the monitoring workflow based on a cron schedule or manual trigger.
2. Python dependencies are installed.
3. AWS credentials are configured.
4. AWS connectivity and S3 access are validated.
5. monitor.py calls the GitHub REST API.
6. Workflow execution data is retrieved.
7. Python calculates the monitoring metrics.
8. Metrics are written to metrics.json.
9. The JSON report is uploaded to the configured S3 bucket.
10. GitHub Actions sends an email containing the monitoring results.**
    
                    ┌──────────────────────────┐
                    │    GitHub Actions        │
                    │   Scheduled Workflow     │
                    │     (Daily / Manual)     │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │      monitor.py          │
                    │   Python Monitoring      │
                    └────────────┬─────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
          ┌──────────────────┐       ┌──────────────────┐
          │   GitHub REST    │       │    AWS S3        │
          │      API         │       │ Metrics Storage  │
          │                  │       │                  │
          │ Workflow Runs    │       │ metrics/date.json│
          └────────┬─────────┘       └──────────────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ Calculate Metrics│
          │                  │
          │ • Total Runs     │
          │ • Successful     │
          │ • Failed        │
          │ • Success Rate   │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │   Email Report   │
          │                  │
          │ Gmail SMTP       │
          │ Monitoring Stats │
          └──────────────────┘
