from airflow import DAG
import pendulum
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

with DAG(
    dag_id='dags_python_with_postgres_hook_bulk_load',
    start_date=pendulum.datetime(2024, 10, 1, tz='Asia/Seoul'),
    schedule=None,
    catchup=False
) as dag:
    
    def insrt_postgres(postgres_conn_id, tbl_nm, file_nm, **kwargs):
        postgres_hook = PostgresHook(postgres_conn_id)
        postgres_hook.bulk_load(tbl_nm, file_nm)

    insrt_postgres = PythonOperator(
        task_id='inst_postgres',
        python_callable=insrt_postgres,
        op_kwargs={'postgres_conn_id' : 'conn-db-postgres-custom',
                   'tbl_nm' : 'TbUseDaystatusView_bulk1',
                   'file_nm' : '/opt/airflow/files/TbUseDaystatusView/20241012/TbUseDaystatusView_2.csv'
                   }
    )

    insrt_postgres