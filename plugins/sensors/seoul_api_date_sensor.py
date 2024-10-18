from airflow.sensors.base import BaseSensorOperator
from airflow.hooks.base import BaseHook


class SeoulApiDateSensor(BaseSensorOperator):
    template_fields = ('endpoint',)

    def __init__(self, dataset_nm, base_dt_col, day_off=0, **kwargs):
        super().__init__(**kwargs)
        self.http_conn_id = 'openapi.seoul.go.kr'
        self.endpoint = '{{var.value.apikey_openapi_seoul_go_kr}}/json/' + dataset_nm + '/1/10/'
        self.base_dt_col = base_dt_col
        self.day_off = day_off

    def poke(self, context):
        import requests
        import json
        from dateutil.relativedelta import relativedelta

        connection = BaseHook.get_connection(self.http_conn_id)
        url = f'http://{connection.host}:{connection.port}/{self.endpoint}'
        self.log.info(f'request url : {url}')
        response = requests.get(url)

        contents = json.loads(response.text)
        key_nm = list(contents.keys())[0]
        row_data = contents.get(key_nm).get('row')
        last_dt = row_data[0].get(self.base_dt_col)
        last_date = last_dt[:10]
        last_date = last_date.replace('.', '-').replace('/', '-')
        search_ymd = (context.get('data_interval_end').in_timezone('Asia/Seoul') + relativedelta(days=self.day_off)).strftime('%Y-%m-%d')

        try:
            import pendulum
            pendulum.from_format(last_date, 'YYYY-MM-DD')
        except:
            from airflow.exceptions import AirflowException
            AirflowException(f'{self.base_dt_col} 컬럼은 YYYY.MM.DD EHSMS YYYY/MM/DD 형태가 아닙니다.')

        if last_date >= search_ymd:
            self.log.info(f'생성확인 (기준 날짜 : {search_ymd} / API Last 날짜 : {last_date}')
            return True
        else:
            self.log.info(f'Update 미완료 (기준 날짜 : {search_ymd} / API Last 날짜 : {last_date}')
            return False

    
        
        while True:
            self.log.info(f'시작:{start_row}')
            self.log.info(f'끝:{end_row}')
            row_df = self._call_api(self.base_url, start_row, end_row)
            total_row_df = pd.concat([total_row_df, row_df])
            if len(row_df) < 1000:
                break
            else:
                start_row = end_row + 1
                end_row += 1000

        if not os.path.exists(self.path):
            os.system(f'mkdir -p {self.path}')
        total_row_df.to_csv(self.path + '/' + self.file_name, encoding='utf-8', index=False)

    def _call_api(self, base_url, start_row, end_row):
        import requests
        import json

        headers = {'Content-Type' : 'application/json',
                   'charset' : 'utf-8',
                   'Accept' : '*/*'
                   }
        request_url = f'{base_url}/{start_row}/{end_row}'
        if self.base_dt is not None:
            request_url = f'{base_url}/{start_row}/{end_row}/{self.base_dt}'
        response = requests.get(request_url, headers)
        contents = json.loads(response.text)

        key_nm = list(contents.keys())[0]
        row_data = contents.get(key_nm).get('row')
        row_df = pd.DataFrame(row_data)

        return row_df