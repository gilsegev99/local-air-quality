## Terraform Infra Setup

1. Navigate to local-air-quality/terraform. Initiate terraform and download the required dependencies-

  ```bash
  terraform init
  ```
2. Edit your zone, region and credentials path in ```variables.tf ``` to the appropriate values.

3. Run ```bash terraform plan ``` and ensure that the correct GCP project ID and credentials are provided. The output should show that a BigQuery dataset, GCS Bucket and VM will be set up.

4. Run ```bash terraform apply ```
