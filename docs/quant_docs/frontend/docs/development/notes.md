---
id: notes
title: Notes
sidebar_label: Notes
slug: /notes
---

- with sdk, use `pipenv shell` in the sdk folder (no conda environment, otherwise things break)
- with bailey, use `conda activate bailey`
- they should be completed in separate terminals

## updating the sdk once you install it in conda environment

- in sdk, first run precommit (or update manually) `pipenv run pipenv-setup sync`
- `python -m build`
- `pip install ../sdk/dist/ssmif_sdk-1.0.0.tar.gz --force` (optional --no-cache-dir)


## random

- `conda create --name bailey python=3.8`
- https://stackoverflow.com/questions/57622556/cant-change-python-path-and-configure-for-anaconda

## swagger

- using swagger ui
- swagger package: https://pypi.org/project/flask-swagger/
- ui installation (using docker): https://github.com/swagger-api/swagger-ui/blob/master/docs/usage/installation.md
- configuration variables for docker: https://github.com/swagger-api/swagger-ui/blob/master/docs/usage/configuration.md#docker
- found a better way. just use flask-restful and flask-apispec, avoiding writing docstrings that look terrible
- http://54.161.254.251:5000/swagger-ui, http://54.161.254.251:5000/swagger are the 2 swagger endpoints

## github actions

delete old workflows: https://stackoverflow.com/questions/57927115/anyone-know-a-way-to-delete-a-workflow-from-github-actions/65374631#65374631

## docker

- https://stackoverflow.com/a/44785784
- `docker images`, `docker container ls`
- problem with adding more build args: https://github.com/whoan/docker-build-with-cache-action/issues/95
