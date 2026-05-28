terraform {
  backend "s3" {
    bucket         = "cursoai-tfstate"
    key            = "dev/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "cursoai-tfstate-lock"
    encrypt        = true
  }
}
