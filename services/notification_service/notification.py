from conductor.client.worker.worker_task import worker_task
from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration

@worker_task(task_definition_name='notify_customer')
def notify_customer(input: object) -> object:
    return { 'notification_status': 'SENT' }

@worker_task(task_definition_name='notify_driver')
def notify_driver(input: object) -> object:
    return { 'notification_status': 'SENT' }

if __name__ == '__main__':
    api_config = Configuration()

    task_handler = TaskHandler(
        workers=[],
        configuration=api_config,
        scan_for_annotated_workers=True
    )
    task_handler.start_processes()
    task_handler.join_processes()