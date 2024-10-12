from operators.seoul_api_to_csv_operator import SeoulApiToCsvOperator
from airflow import DAG
import pendulum

with DAG(
    dag_id='dags_seoul_api_corona',
    schedule=None,
    start_date=pendulum.datetime(2024, 10, 1, tz='Asia/Seoul'),
    catchup=False
) as dag:
    '''서울시 한강공원 주차장 이용현황 (코로나 확진자 발생 동향은 23.8까지만 제공)'''
    tb_hanriver_park_count_status = SeoulApiToCsvOperator(
        task_id='tb_hanriver_park_count_status',
        dataset_nm='TbUseDaystatusView',
        path='/opt/airflow/files/TbUseDaystatusView/{{data_interval_end.in_timezone("Asia/Seoul") | ds_nodash}}',
        file_name='TbUseDaystatusView.csv'
    )

    '''서울시 공공자전거 이용 정보'''
    tb_bicycle_count_status = SeoulApiToCsvOperator(
        task_id='tb_bicycle_count_status',
        dataset_nm='tbCycleRentUseDayInfo',
        path='/opt/airflow/files/tbCycleRentUseDayInfo/{{data_interval_end.in_timezone("Asia/Seoul") | ds_nodash}}',
        file_name='tbCycleRentUseDayInfo.csv',
        base_dt='{{data_interval_start.in_timezone("Asia/Seoul") | ds_nodash}}}'
    )

    tb_hanriver_park_count_status >> tb_bicycle_count_status