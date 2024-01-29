from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration

if __name__ == '__main__':
    api_config = Configuration()
    
    import_modules = [
        'services.booking_service.booking',
        'services.assignment_service.assignment',
        'services.payment_service.payments',
        'services.notification_service.notification'
    ]

    task_handler = TaskHandler(
        workers=[],
        configuration=api_config,
        scan_for_annotated_workers=True,
        import_modules=import_modules
    )

    task_handler.start_processes()
    task_handler.join_processes()