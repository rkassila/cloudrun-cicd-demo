# Cloud Run CI/CD with GitHub Actions

This repository demonstrates a minimal **CI/CD setup** for deploying a Python app to **Cloud Run** using **Artifact Registry** and **GitHub Actions**.  

---

## Project Structure
```
.
├── app.py                  # Your FastAPI or Python app
├── Dockerfile              # Docker build instructions
├── README.md               # Project documentation
└── .github
    └── workflows
        └── deploy.yml      # GitHub Actions workflow for CI/CD
```

---

## GCP Setup

### 1. Enable Required APIs

Before using the workflow, enable the following APIs:

- **Cloud Run API**: deploy and manage Cloud Run services.  
```bash
gcloud services enable run.googleapis.com --project=<PROJECT_ID>
```
- **Artifact Registry API**: push Docker images from GitHub Actions.
```bash
gcloud services enable artifactregistry.googleapis.com --project=<PROJECT_ID>
```

## 2. Create or Use a Service Account

The GitHub Actions workflow requires a service account with the following roles:

| Role | Purpose |
|------|---------|
| `roles/run.admin` | Deploy and manage Cloud Run services |
| `roles/artifactregistry.writer` | Push Docker images to Artifact Registry |
| `roles/iam.serviceAccountUser` | Allow workflow to act as the service account |

Assign roles with:
```bash
PROJECT=<PROJECT_ID>
SA_EMAIL=your-sa-name@${PROJECT}.iam.gserviceaccount.com

gcloud projects add-iam-policy-binding $PROJECT \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding $PROJECT \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/iam.serviceAccountUser"
```

## 3. Artifact Registry Repository

Ensure a Docker repository exists in the same region as Cloud Run:
```bash
gcloud artifacts repositories create cloud-run-repo \
  --repository-format=docker \
  --location=asia-northeast1 \
  --description="Docker repo for Cloud Run"
```
---
## GitHub Secrets

Add the following secrets to your GitHub repository:

| Secret | Value |
|--------|-------|
| `GCP_PROJECT_ID` | Your GCP project ID |
| `GCP_SA_KEY` | JSON key of the service account |
| `GCP_REGION` | Cloud Run region |

---

## GitHub Actions Workflow

- Located at `.github/workflows/deploy.yml`.  
- Triggered automatically on push to the `master` branch.  

Workflow steps:

1. Checkout repository.  
2. Authenticate to GCP using the service account.  
3. Configure Docker for Artifact Registry.  
4. Build and push Docker image.  
5. Deploy to Cloud Run.  

---

## Running Locally

To test your app locally:

```bash
# Install dependencies
pip install fastapi uvicorn

# Run app
uvicorn app:app --host 0.0.0.0 --port 8080
```
---

## Deploying

Simply **push to `master`** and GitHub Actions will:

1. Build the Docker image.  
2. Push it to Artifact Registry.  
3. Deploy the app to Cloud Run.  

---

## Notes

- Ensure your service account has **all required roles**.  
- The Artifact Registry repository and Cloud Run must be in the **same region**.
- Be careful about costs from GCP 
