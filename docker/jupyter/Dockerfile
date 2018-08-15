FROM jupyter/scipy-notebook

USER root

RUN pip install --no-cache-dir \
  boto3 \
  neomodel \
  dateparser

USER jovyan
