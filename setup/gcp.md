## GCP

### Initial Setup

1. Create an account with your Google email ID
2. Setup your first [project](https://console.cloud.google.com/) if you haven't already
    * eg. "Local Air Quality", and note down the "Project ID" (we'll use this later when deploying infra with Terraform)
3. Setup [service account & authentication](https://cloud.google.com/iam/docs/service-accounts-create#console) for this project
    * Grant `Viewer` role to begin with.
    * Download service-account-keys (`.json`) for auth. (Please do not share this key file publicly. Keep it secure!)
    * Rename the `.json` key file to `google_credentials.json`
4. Download [SDK](https://cloud.google.com/sdk/docs/quickstart) for local setup
5. Set environment variable to point to your downloaded GCP keys:
   ```shell
   export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/google_credentials.json>"

   # Refresh token/session, and verify authentication
   gcloud auth application-default login
   ```

### Setup for Access

1. [IAM Roles](https://cloud.google.com/storage/docs/access-control/iam-roles) for Service account:
   * Go to the *IAM* section of *IAM & Admin* https://console.cloud.google.com/iam-admin/iam
   * Click the *Edit principal* icon for the service account you have previously set up.
   * Add these roles in addition to *Viewer* : **Storage Admin** + **Storage Object Admin** + **BigQuery Admin** + **Compute Instance Admin**

2. Enable these APIs for your project:
   * https://console.cloud.google.com/apis/library/iam.googleapis.com
   * https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com

3. Please ensure `GOOGLE_APPLICATION_CREDENTIALS` environment variable is set.
   ```shell
   export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"
   ```
