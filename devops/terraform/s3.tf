resource "aws_s3_bucket" "ssmif-reports" {
  bucket = "ssmif-reports"
  acl    = "private"
}

resource "aws_s3_bucket" "factor-model-data" {
  bucket = "factor-model-data"
  acl    = "private"
}
