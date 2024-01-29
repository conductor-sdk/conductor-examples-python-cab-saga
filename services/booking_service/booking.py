from conductor.client.worker.worker_task import worker_task
from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.models.task_result import TaskResult
from uuid import uuid4

@worker_task(task_definition_name='book_ride')
def book_ride(pick_up_location: str, drop_off_location: str, rider_id: str) -> object:
    return { 'booking_id': '1234' }

@worker_task(task_definition_name='confirm_booking')
def confirm_booking(booking_id: str, driver_id: str) -> object:
    return { 'booking_status': 'CONFIRMED' }

@worker_task(task_definition_name='cancel_booking')
def cancel_booking(booking_id: str) -> object:
    return { 'booking_status': 'CANCELLED' }

def main():
    api_config = Configuration()

    task_handler = TaskHandler(
        workers=[],
        configuration=api_config,
        scan_for_annotated_workers=True
    )
    task_handler.start_processes()
    task_handler.join_processes()

if __name__ == '__main__':
    main()