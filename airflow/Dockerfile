FROM apache/airflow:2.6.0-python3.9

ARG USER_NAME=airflow

ENV PYTHONUNBUFFERED=1
ARG USER_NAME=airflow
ENV PYTHONUNBUFFERED=1
ENV AIRFLOW_HOME=/opt/airflow
RUN mkdir -p $AIRFLOW_HOME/logs && chmod -R 777 $AIRFLOW_HOME/logs && chown -R ${USER_NAME}: $AIRFLOW_HOME/logs

USER ${USER_NAME}
COPY requirements.txt /requirements.txt
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r /requirements.txt
RUN pip install --no-cache-dir --user 'apache-airflow-providers-apache-spark'
