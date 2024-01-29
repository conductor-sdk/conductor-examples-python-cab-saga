from conductor.client.worker.worker_task import worker_task

@worker_task(task_definition_name='book_ride')
def book_ride(pick_up_location: str, drop_off_location: str, rider_id: str) -> object:
    return { 'booking_id': '1234' }

@worker_task(task_definition_name='confirm_booking')
def confirm_booking(booking_id: str, driver_id: str) -> object:
    return { 'booking_status': 'CONFIRMED' }

@worker_task(task_definition_name='cancel_booking')
def cancel_booking(booking_id: str) -> object:
    return { 'booking_status': 'CANCELLED' }
