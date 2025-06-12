variable "credentials" {
  description = "Local Air Quality Credentials"
  default     = "REPLACE_ME_WITH_CREDENTIALS_PATH"
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

variable "vm_name" {
  description = "Name of the VM instance"
  type        = string
  default     = "local-air-quality"
}

variable "vm_machine_type" {
  description = "Machine type"
  type        = string
  default     = "e2-standard-4"
}

variable "zone" {
  description = "The zone to deploy the VM in"
  type        = string
  default     = "europe-west2-b"
}

variable "vm_boot_image" {
  description = "The boot image to use"
  type        = string
  default     = "ubuntu-2004-lts"
}

variable "vm_disk_size_gb" {
  description = "Boot disk size in GB"
  type        = number
  default     = 30
}

variable "vm_startup_script" {
  description = "Startup script to be run on VM boot"
  type        = string
  default     = ""
}

variable "vm_tags" {
  description = "Network tags for the VM"
  type        = list(string)
  default     = []
}
