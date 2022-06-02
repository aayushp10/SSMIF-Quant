# note - need to manually make the volumes 100gb
# and run the install script to configure environments

locals {
  servers = toset([
    "ssmif-factor-model",
    "ssmif-development",
  ])
}

resource "aws_cloud9_environment_ec2" "dev_server" {
  for_each = local.servers
  instance_type = "t3a.xlarge"
  name          = each.key
  description   = "${each.key} cloud9 environment"
  automatic_stop_time_minutes = 30
}
