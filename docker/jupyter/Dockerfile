FROM jupyter/scipy-notebook

USER root

RUN apt-get update 
RUN apt-get -y install screen

RUN pip install --no-cache-dir \
  boto3 \
  neomodel \
  dateparser \
  requests \
  arrow \
  tqdm

USER jovyan
