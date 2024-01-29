from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration

if __name__ == '__main__':
    api_config = Configuration()

    task_handler = TaskHandler(
        workers=[],
        configuration=api_config,
        scan_for_annotated_workers=True,
        import_modules=['payments']
    )

    task_handler.start_processes()
    task_handler.join_processes()