from conductor.client.worker.worker_task import worker_task

@worker_task(task_definition_name='notify_customer')
def notify_customer(input: object) -> object:
    return { 'notification_status': 'SENT' }

@worker_task(task_definition_name='notify_driver')
def notify_driver(input: object) -> object:
    return { 'notification_status': 'SENT' }
