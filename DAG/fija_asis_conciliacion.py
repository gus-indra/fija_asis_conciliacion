import textwrap
import pendulum
from datetime import datetime, timedelta

from airflow.models.dag import DAG
from airflow.utils.edgemodifier import Label
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup


ruta_operacion = '/space/tareas/Proyecto_fija_asis'

with DAG(
    "fija_asis_conciliacion",
    default_args={
        "depends_on_past": False,
        "email": ["carlos.chavez@claro.com.pe"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=1),
        "schedule": "05 9-22 * * *",
        "catchup": False,
        "owner": 'C28231',
    },
    description="Proceso diario de analisis de inconsistencias Fija Asis conciliaciones",
    schedule= "05 9-22 * * *",
    start_date=datetime(2024, 3, 1),
    catchup=False,
    tags=["fija", "conciliacion", "diario"],
) as dag:
    with TaskGroup(
        "fija_sga",
        tooltip= "Este grupo procesa conciliaciones en SGA"
    ) as Conciliaciones_SGA:
        #MDC001311 = SSHOperator(
        #    task_id = 'MDC001311',
        #    ssh_conn_id="limnwkddsv02",
        #    command=f"{ruta_operacion}/venv/bin/python {ruta_operacion}/main.py -c MDC001311 -tc C",
        #    do_xcom_push = True,
        #    dag = dag,
        #    doc_md="""### MDC001311
        #            Clientes cuentan con servicio VOD activo en SGA pero no estan aprovisionados en ICG
        #            """,
        #)
        # MDC001321 = SSHOperator(
        #     task_id = 'MDC001321',
        #     ssh_conn_id="limnwkddsv02",
        #     command=f"{ruta_operacion}/venv/bin/python {ruta_operacion}/main.py -c MDC001321 -tc C",
        #     do_xcom_push = True,
        #     dag = dag,
        #     doc_md="""### MDC001321
        #             Clientes cuentan con mas de un SID - PID
        #             """,
        # )
        MDC001322 = SSHOperator(
            task_id = 'MDC001322',
            ssh_conn_id="limnwkddsv02",
            command=f"{ruta_operacion}/venv/bin/python {ruta_operacion}/main.py -c MDC001322 -tc C",
            do_xcom_push = True,
            dag = dag,
            doc_md="""### MDC001322
                    Clientes sin agendamiento
                    """,
        )
        # MDC001260 = SSHOperator(
        #     task_id = 'MDC001260',
        #     ssh_conn_id="limnwkddsv02",
        #     command=f"{ruta_operacion}/venv/bin/python {ruta_operacion}/main.py -c MDC001260 -tc C",
        #     do_xcom_push = True,
        #     dag = dag,
        #     doc_md="""### MDC001260
        #             Clientes sin agendamiento
        #             """,
        # )
        #MDC001363 = SSHOperator(
        #    task_id = 'MDC001363',
        #    ssh_conn_id="limnwkddsv02",
        #    command=f"{ruta_operacion}/venv/bin/python {ruta_operacion}/main.py -c MDC001363 -tc C",
        #    do_xcom_push = True,
        #    dag = dag,
        #    doc_md="""### MDC001363
        #            Clientes que cuentan con fec_fin pero esten con el estado activo en SGA
        #            """,
        #)
        #MDC001301 = SSHOperator(
        #    task_id = 'MDC001301',
        #    ssh_conn_id="limnwkddsv02",
        #    command=f"{ruta_operacion}/venv/bin/python {ruta_operacion}/main.py -c MDC001301 -tc C",
        #    do_xcom_push = True,
        #    dag = dag,
        #    doc_md="""### MDC001301
        #            SOT SGA con estado "Aprobadas" y no pasan a "En ejecución" o "Rechazadas"
        #            """,
        #)
        MDC001305 = SSHOperator(
            task_id = 'MDC001305',
            ssh_conn_id="limnwkddsv02",
            command=f"{ruta_operacion}/venv/bin/python {ruta_operacion}/main.py -c MDC001305 -tc C",
            do_xcom_push = True,
            dag = dag,
            doc_md="""### MDC001305
                    SOT SGA con estado "Aprobadas" y no pasan a "En ejecución" o "Rechazadas"
                    """,
        #)
        #MDC001347 = SSHOperator(
        #    task_id = 'MDC001347',
        #    ssh_conn_id="limnwkddsv02",
        #    command=f"{ruta_operacion}/venv/bin/python {ruta_operacion}/main.py -c MDC001347 -tc C",
        #    do_xcom_push = True,
        #    dag = dag,
        #    doc_md="""### MDC001347
        #            Control de lineas disponibles SGA
        #            """,
        )
        # MDC001353 = SSHOperator(
        #     task_id = 'MDC001353',
        #     ssh_conn_id="limnwkddsv02",
        #     command=f"{ruta_operacion}/venv/bin/python {ruta_operacion}/main.py -c MDC001353 -tc C",
        #     do_xcom_push = True,
        #     dag = dag,
        #     doc_md="""### MDC001353
        #             CReporte de Ejecución SOTs Diario
        #             """,
        # )
        MDC001305 >> MDC001322
        #MDC001305 >> MDC001322 >> MDC001347
        #MDC001305 >> MDC001322 >> MDC001353 # >> MDC001347  
        #MDC001311 >> MDC001321 >> MDC001363 >> MDC001301 >> MDC001305 >> MDC001322 >> MDC001353 # >> MDC001260 >> MDC001347
    with TaskGroup(
        "fija_bscs",
        tooltip= "Este grupo procesa conciliaciones en ICG vs BSCS"    
    ) as Conciliaciones_BSCS:
        MDC001246 = SSHOperator(
            task_id = 'MDC001246',
            ssh_conn_id="limnwkddsv02",
            command=f"{ruta_operacion}/venv/bin/python {ruta_operacion}/main.py -c MDC001246 -tc C",
            do_xcom_push = True,
            dag = dag,
            doc_md="""### MDC001246
                    Clientes que cuentan con una velocidad provisionada distinta a la contratada
                    """,
        )
        MDC001244 = SSHOperator(
            task_id = 'MDC001244',
            ssh_conn_id="limnwkddsv02",
            command=f"{ruta_operacion}/venv/bin/python {ruta_operacion}/main.py -c MDC001244 -tc C",
            do_xcom_push = True,
            dag = dag,
            doc_md="""### MDC001244
                    Clientes aprovisionados en ICG con contratos suspendidos en BSCS/BSCSIX
                    """,
        )
        MDC001249 = SSHOperator(
            task_id = 'MDC001249',
            ssh_conn_id="limnwkddsv02",
            command=f"{ruta_operacion}/venv/bin/python {ruta_operacion}/main.py -c MDC001249 -tc C",
            do_xcom_push = True,
            dag = dag,
            doc_md="""### MDC001249
                    Clientes aprovisionados en ICG con Solicitud de corte atendida
                    """,
        )
        MDC007760 = SSHOperator(
            task_id = 'MDC007760',
            ssh_conn_id="limnwkddsv02",
            command=f"{ruta_operacion}/venv/bin/python {ruta_operacion}/main.py -c MDC007760 -tc C",
            do_xcom_push = True,
            dag = dag,
            doc_md="""### MDC007760
                    Clientes aprovisionados en ICG con contratos desactivos en BSCS
                    """,
        )
        # MDC007762 = SSHOperator(
        #     task_id = 'MDC007762',
        #     ssh_conn_id="limnwkddsv02",
        #     command=f"{ruta_operacion}/venv/bin/python {ruta_operacion}/main.py -c MDC007762 -tc C",
        #     do_xcom_push = True,
        #     dag = dag,
        #     doc_md="""### MDC007762
        #             Clientes que cuentan con un ciclo distinto en Janus vs BSCS
        #             """,
        # )
        MDC001370 = SSHOperator(
            task_id = 'MDC001370',
            ssh_conn_id="limnwkddsv02",
            command=f"/space/tareas/Proyecto_fija_dev/venv/bin/python /space/tareas/Proyecto_fija_dev/main.py -c MDC001370 -tc C",
            do_xcom_push = True,
            dag = dag,
            doc_md="""### MDC001370
                    Clientes que cuentan con un ciclo distinto en Janus vs BSCS
                    """,
        )
        #MDC001246 >> MDC001244 >> MDC007762 >> MDC007760 >>  MDC001249 >> MDC001370
        MDC001246 >> MDC001244 >> MDC007760 >>  MDC001249 >> MDC001370

Conciliaciones_SGA 
Conciliaciones_BSCS