from airflow.providers.slack.hooks.slack_webhook import SlackWebhookHook
import pendulum

def sla_miss_callback_to_slack(dag, task_list, blocking_task_list, slas, blocking_tis):
    slack_hook = SlackWebhookHook(slack_webhook_conn_id='conn_slack_airflow_bot')
    text = 'SLA Miss 알람'
    block_fields = []

    for task in task_list.split('\n'):
        task_id = task.split(' ')[0]
        execution_date = task.split(' ')[2]
        execution_date_kr = pendulum.parse(execution_date, tz='UTC').in_timezone('Asia/Seoul').strftime('%Y-%m-%dT%H:%M:%S+09:00')
        block_fields.append(
            {
                'type' : 'mrkdwn',
                'text' : f'*DAG:*: {dag.dag_id}, *task_id*: {task_id}, *Execution_date*: {execution_date_kr}'
            }
        )
        blocks = [
            {
                'type' : 'section',
                'text' : {
                    'type' : 'mrkdwn',
                    'text' : 'SLA Miss 알람!'
                }
            },
            {
                'type' : 'section',
                'fields' : block_fields 
            }
        ]

        slack_hook.send(text=text, blocks=blocks)