---
id: cron-jobs
title: Cron Jobs
sidebar_label: Cron Jobs
slug: /cron-jobs
---

For building the weekly report, the following cron job config is used in aws: `cron(30 13 ? * SUN *)`. It runs every sunday at 8:30 a.m. (because the cron expression follows UTC time). See https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html for more information.
