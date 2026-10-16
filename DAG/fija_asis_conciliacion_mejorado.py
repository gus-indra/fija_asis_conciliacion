import pendulum 
from datetime import timedelta 
 
from airflow.models.dag import DAG 
from airflow.providers.ssh.operators.ssh import SSHOperator 
from airflow.providers.standard.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup 
#CLARO 
#RUTA_OPERACION = "/space/tareas/Proyecto_fija_asis" 
RUTA_OPERACION = "/opt/airflow/procesos"
#INDRA
SSH_CONN_ID = "limnwkddsv02" 
 
DEFAULT_ARGS = { 
    "owner": "C28231", 
    "depends_on_past": False, 
    "email": ["carlos.chavez@claro.com.pe"], 
    "email_on_failure": False, 
    "email_on_retry": False, 
    "retries": 1, 
    "retry_delay": timedelta(minutes=1), 
} 
 
 
# def crear_control(task_id: str, descripcion: str) -> SSHOperator: 
#     return SSHOperator( 
#         task_id=task_id, 
#         ssh_conn_id=SSH_CONN_ID, 
#         command=( 
#             "set -euo pipefail; " 
#             f"exec {RUTA_OPERACION}/venv/bin/python " 
#             f"{RUTA_OPERACION}/main.py " 
#             f"-c {task_id} -tc C " 
#             "--run-id '{{ run_id }}' " 
#             "--interval-start '{{ data_interval_start.isoformat() }}' " 
#             "--interval-end '{{ data_interval_end.isoformat() }}'" 
#         ), 
#         conn_timeout=30, 
#         cmd_timeout=3300, 
#         execution_timeout=timedelta(minutes=55), 
#         get_pty=True, 
#         pool="fija_asis_pool", 
#         do_xcom_push=False, 
#         doc_md=f"### {task_id}\n{descripcion}", 
#     ) 

def crear_control(task_id: str, descripcion: str) -> BashOperator:
    return BashOperator(
        task_id=task_id,
        bash_command=(
            "set -euo pipefail; "
            'exec python -u "$RUTA_OPERACION/main.py" '
            '-c "$COD_CONTROL" '
            "-tc C "
            '--run-id "$RUN_ID" '
            '--interval-start "$INTERVAL_START" '
            '--interval-end "$INTERVAL_END"'
        ),
        cwd=RUTA_OPERACION,
        env={
            "RUTA_OPERACION": RUTA_OPERACION,
            "COD_CONTROL": task_id,
            "RUN_ID": "{{ run_id }}",
            "INTERVAL_START": "{{ data_interval_start.isoformat() }}",
            "INTERVAL_END": "{{ data_interval_end.isoformat() }}",
        },
        append_env=True,
        execution_timeout=timedelta(minutes=55),
        pool="fija_asis_pool",
        do_xcom_push=False,
        doc_md=f"### {task_id}\n{descripcion}",
    )


with DAG( 
    dag_id="fija_asis_conciliacion_mejorado", 
    default_args=DEFAULT_ARGS, 
    description="Proceso de análisis de inconsistencias Fija Asis", 
    schedule="05 9-22 * * *", 
    start_date=pendulum.datetime(2024, 3, 1, tz="America/Lima"), 
    catchup=False, 
    max_active_runs=1, 
    tags=["fija", "conciliacion", "diario"], 
) as dag: 
 
    with TaskGroup("fija_sga", tooltip="Conciliaciones en SGA"): 
        mdc001305 = crear_control( 
            "MDC001305", 
            'SOT SGA en estado "Aprobadas" que no pasan a ejecución o rechazo', 
        ) 
        mdc001322 = crear_control("MDC001322", "Clientes sin agendamiento") 
        mdc001305 >> mdc001322 
 
    with TaskGroup("fija_bscs", tooltip="Conciliaciones ICG vs BSCS"): 
        mdc001246 = crear_control("MDC001246", "Velocidad provisionada distinta de la contratada") 
        mdc001244 = crear_control("MDC001244", "Clientes en ICG con contratos suspendidos") 
        mdc007760 = crear_control("MDC007760", "Clientes en ICG con contratos desactivos") 
        mdc001249 = crear_control("MDC001249", "Clientes en ICG con solicitud de corte atendida") 
        mdc001370 = crear_control("MDC001370", "Ciclo diferente entre Janus y BSCS") 
 
        mdc001246 >> mdc001244 >> mdc007760 >> mdc001249 >> mdc001370 
