locals {
  repostories = toset([
    "ssmif-bailey-api",
    "ssmif-bailey-frontend",
    "ssmif-stock-data-update",
    "ssmif-stop-loss-update",
    "ssmif-weekly-report",
  ])
  repositories_stages = formatlist("%s-stages", local.repostories)
  all_repositories = toset(concat(tolist(local.repostories), tolist(local.repositories_stages)))
}

resource "aws_ecr_repository" "repositories" {
  for_each = local.all_repositories
  name     = each.key

  image_scanning_configuration {
    scan_on_push = true
  }
}
