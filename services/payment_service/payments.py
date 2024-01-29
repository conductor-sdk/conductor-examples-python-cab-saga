from conductor.client.worker.worker_task import worker_task
from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.models.task_result import TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus

@worker_task(task_definition_name='make_payment')
def make_payment(booking_id: str, rider_id: str) -> object:
    task_result = TaskResult()
    
    if rider_id > 2:
        task_result.add_output_data('payment_status', 'FAILED')
        task_result.status = TaskResultStatus.FAILED_WITH_TERMINAL_ERROR
    else:
        task_result.add_output_data('payment_status', 'COMPLETED')
        task_result.status = TaskResultStatus.COMPLETED

    return task_result

@worker_task(task_definition_name='cancel_payment')
def cancel_payment(booking_id: str) -> object:
    return { 'payment_status' : 'CANCELLED' }
    
if __name__ == '__main__':
    api_config = Configuration()

    task_handler = TaskHandler(
        workers=[],
        configuration=api_config,
        scan_for_annotated_workers=True
    )
    task_handler.start_processes()
    task_handler.join_processes()