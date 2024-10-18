from sensors.seoul_api_date_sensor import SeoulApiDateSensor
from airflow import DAG
import pendulum

with DAG(
    dag_id='dags_custom_sensor',
    start_date=pendulum.datetime(2024, 10, 1, tz='Asia/Seoul'),
    schedule=None,
    catchup=False
) as dag:
    
    tb_hanriver_park_count_status = SeoulApiDateSensor(
        task_id='tb_hanriver_park_count_status',
        dataset_nm='TbUseDaystatusView',
        base_dt_col='DT',
        day_off=-3,
        poke_interval=600,
        mode='reschedule'
    )

    '''서울시 공공자전거 이용 정보'''
    tb_bicycle_count_status = SeoulApiDateSensor(
        task_id='tb_bicycle_count_status',
        dataset_nm='tbCycleRentUseDayInfo',
        base_dt_col='RENT_DT',
        day_off=-3,
        poke_interval=600,
        mode='reschedule'
    )