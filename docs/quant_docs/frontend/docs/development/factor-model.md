---
id: factor-model
title: Factor Model
sidebar_label: Factor Model
slug: /factor-model
---

In deployment the factor model runs on [Spark](https://spark.apache.org/docs/latest/api/python/). This is to allow for compiled logs and scalability on robust infrastructure. The unfortunate side-effect is that it adds increased complexity to the deployment pipeline, but that's not something most have to worry about. When you navigate to the Yarn or Spark History UI in AWS EMR, there are a bunch of options, and it looks confusing. But it's not that bad. The YARN timeline server shows all the logs, and is generally easier to navigate, though its ui is less polished. Some of the logs don't show in certain pages, but if that happens there's usually a different way to navigate to the same data. For example, this page shows the all the logs on YARN for the second run of the model: https://container-id.us-east-1.amazonaws.com/containers/application_1622295546320_0001/container_1622295546320_0001_01_000002/. The second run contains the correct logs, but the first doesn't. I got to this page by clicking the "Logs" button on the "Application Attempt" page. That's probably the easiest way to get to the logs.

On Spark History UI, you should head to the "Executors" page. Something like this: https://container-id.us-east-1.amazonaws.com/shs/history/application_1622295546320_0001/1/executors/. You can get to it through the ui. Then you look at the "driver" logs. The other pages don't show all the logs necessarily.

After the cluster finishes, it may take about 10 minutes for the logs to show on the spark ui. Just be patient.
