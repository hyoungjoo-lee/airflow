from airflow.sensors.bash import BashSensor
from airflow.operators.bash import BashOperator
from airflow import DAG
import pendulum

with DAG(
    dag_id='dags_bash_sensor',
    start_date=pendulum.datetime(2024, 10, 1, tz='Asia/Seoul'),
    schedule=None,
    catchup=False
) as dag:
    
    sensor_task_by_poke = BashSensor(
        task_id='sensor_task_by_poke',
        env={'FILE':'/opt/airflow/files/TbUseDaystatusView/{{data_interval_end.in_timezone("Asia/Seoul") | ds_nodash }}/TbUseDaystatusView.csv'},
        bash_command=f'''echo $FILE && 
                        if [ -f $FILE ]; then 
                              exit 0
                        else 
                              exit 1
                        fi''',
        poke_interval=30,      #30초
        timeout=60*2,          #3분
        mode='poke',
        soft_fail=False
    )

    sensor_task_by_reschedule = BashSensor(
        task_id='sensor_task_by_reschedule',
        env={'FILE':'/opt/airflow/files/TbUseDaystatusView/{{data_interval_end.in_timezone("Asia/Seoul") | ds_nodash }}/TbUseDaystatusView.csv'},
        bash_command=f'''echo $FILE && 
                        if [ -f $FILE ]; then 
                              exit 0
                        else 
                              exit 1
                        fi''',
        poke_interval=60*1,    # 1분
        timeout=60*3,          # 3분
        mode='reschedule',
        soft_fail=True
    )

    bash_task = BashOperator(
        task_id='bash_task',
        env={'FILE': '/opt/airflow/files/TbUseDaystatusView/{{data_interval_end.in_timezone("Asia/Seoul") | ds_nodash }}/TbUseDaystatusView.csv'},
        bash_command='echo "건수: `cat $FILE | wc -l`"',
    )

    [sensor_task_by_poke, sensor_task_by_reschedule] >> bash_task