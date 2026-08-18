import os
import json
from datetime import datetime, timezone

import requests
import boto3


# Configuration
GITHUB_TOKEN = os.environ["GH_TOKEN"]
S3_BUCKET = os.environ["S3_BUCKET"]

REPOSITORY = os.environ["GITHUB_REPOSITORY"]

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}


# Get workflow runs from GitHub
url = f"https://api.github.com/repos/{REPOSITORY}/actions/runs"

response = requests.get(
    url,
    headers=headers,
    params={"per_page": 100}
)

response.raise_for_status()

workflow_runs = response.json()["workflow_runs"]


# Calculate metrics
total_runs = len(workflow_runs)

successful_runs = sum(
    1 for run in workflow_runs
    if run["conclusion"] == "success"
)

failed_runs = sum(
    1 for run in workflow_runs
    if run["conclusion"] == "failure"
)

if total_runs > 0:
    success_rate = round(
        (successful_runs / total_runs) * 100, 2
    )
else:
    success_rate = 0


# Create metrics
metrics = {
    "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    "total_runs": total_runs,
    "successful_runs": successful_runs,
    "failed_runs": failed_runs,
    "success_rate": success_rate
}


# Save JSON locally
filename = "metrics.json"

with open(filename, "w") as file:
    json.dump(metrics, file, indent=2)


# Upload to S3
s3 = boto3.client("s3")

date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

s3.upload_file(
    filename,
    S3_BUCKET,
    f"metrics/{date}.json"
)

print("GitHub Actions metrics:")
print(json.dumps(metrics, indent=2))

print(f"Metrics uploaded to s3://{S3_BUCKET}/metrics/{date}.json")
