variable "credentials" {
  description = "Local Air Quality Credentials"
  default     = "/home/gilsegev/keys/local-air-quality.json"
}


variable "project" {
  description = "Project"
  default     = "local-air-quality-454807"
}

variable "region" {
  description = "Region"
  default     = "europe-west2"
}

variable "location" {
  description = "Project Location"
  default     = "EU"
}

variable "bq_dataset_name" {
  description = "My Local Air Quality dataset"
  default     = "local_air_quality"
}

variable "gcs_bucket_name" {
  description = "My Local Air Quality bucket"
  default     = "local-air-quality-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}
