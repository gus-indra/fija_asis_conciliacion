FROM apache/airflow:3.3.2-python3.12

USER airflow

COPY --chown=airflow:root procesos/requirements.txt /tmp/requirements-proceso.txt

RUN python -m venv /opt/airflow/venv-procesos \
    && /opt/airflow/venv-procesos/bin/python -m pip install \
        --no-cache-dir \
        -r /tmp/requirements-proceso.txt \
    && /opt/airflow/venv-procesos/bin/python -m pip check