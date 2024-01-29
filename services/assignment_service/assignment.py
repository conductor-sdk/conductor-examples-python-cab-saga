from conductor.client.worker.worker_task import worker_task

@worker_task(task_definition_name='assign_driver')
def assign_driver(booking_id: str) -> object:
    return { 'driver_id': '7652' }

@worker_task(task_definition_name='cancel_driver_assignment')
def cancel_driver_assignment(booking_id: str) -> object:
    return { 'DRIVER_ASSIGNMENT_STATUS': 'CANCELLED' }