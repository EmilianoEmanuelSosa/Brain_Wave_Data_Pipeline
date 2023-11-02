from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowFailException


default_args = {
    "depends_on_past": False,
    "email": ['emilianoemanuel2850@gmail.com'],
    "email_on_failure": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    # "queue": "bash_queue",
    # "pool":'backfill'
    # "Priority_weight",
    # "end_date",
    # "wait_for_downstream": False,
    # "sla": timedelta(hours=2),
    # "execution_timeout": timedelta(seconds=300),
    # "on_failure_callback": some_functions, # or list of functions
    # "on_failure_callback": some_other_functions, # or list of functions
    # "on_retry_callback": another_function, # or list of functions
    # "sla_miss_callback": yet_another_function, # or list of functions
    # "trigger_rule": 'all_success'
}

dag = DAG(
    "test_1",  # Cambié ":" por "_" en el nombre del DAG
    description="Mi primer DAG",
    default_args=default_args,
    schedule_interval=timedelta(days=1),  # Corregido "schedule" a "schedule_interval"
    start_date=datetime(2023, 9, 24),
    catchup=False,
    tags=['example'],
    params={"commit":'00000'}
)

def task0_func(**kwargs):
    conf=kwargs['dag_run'].conf
    if "commit" in conf and conf["commit"]== "1":
        raise AirflowFailException("Ese commit es invalido para desplegar....")
        
    return {'ok': 1}

def task2_func(**kwargs):
    xcom_value=kwargs["ti"].xcom_pull(task_ids='task0')
    print('---------------------------------------------------------------------------------------------------------------HOLA--------------------------------------------------------------------------')
    print( xcom_value )
    return {'ok': 2}

task0 = PythonOperator(
    task_id='task0',
    python_callable=task0_func,  # Cambié "pyhton_callable" a "python_callable"
    provide_context=True,  # Agregado para pasar el contexto a la función
    dag=dag
)

task1 = BashOperator(
    task_id="print_date",
    bash_command='echo "la fecha es $(date)"',
    dag=dag
)

task2 = PythonOperator(
    task_id='task2',  # Cambiado de 'tarea2' a 'task2' para que coincida con el ID
    python_callable=task2_func,  # Cambié "PythonCallable" a "python_callable"
    provide_context=True,  # Agregado para pasar el contexto a la función
    dag=dag
)

task0 >> [task1, task2]