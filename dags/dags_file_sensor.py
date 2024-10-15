from airflow import DAG
from airflow.sensors.filesystem import FileSensor
import pendulum

with DAG(
    dag_id='dags_file_sensor',
    start_date=pendulum.datetime(2024,10,1, tz='Asia/Seoul'),
    schedule=None,
    catchup=False
) as dag:
    TbUseDaystatusView_sensor = FileSensor(
        task_id='TbUseDaystatusView_sensor',
        fs_conn_id='conn_file_opt_airflow_files',
        filepath='TbUseDaystatusView/{{data_interval_end.in_timezone("Asia/Seoul") | ds_nodash }}/TbUseDaystatusView.csv',
        recursive=False,
        poke_interval=60,
        timeout=60*60*24, # 1일
        mode='reschedule'
    )
