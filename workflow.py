from conductor.client.configuration.configuration import Configuration
from conductor.client.orkes.orkes_metadata_client import OrkesMetadataClient
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.workflow.task.simple_task import SimpleTask
from conductor.client.workflow.task.fork_task import ForkTask
from conductor.client.workflow.task.fork_task import JoinTask

def register_cab_booking_workflow() -> ConductorWorkflow:
    configuration = Configuration()
        
    workflow_executor = WorkflowExecutor(configuration=configuration)

    book_ride = SimpleTask(task_def_name='book_ride', task_reference_name='book_ride_ref')
    book_ride.input_parameters = {
        'rider_id' : '${workflow.input.rider_id}',
        'pick_up_location' : '${workflow.input.pick_up_location}',
        'drop_off_location' : '${workflow.input.drop_off_location}'
    }
    
    assign_driver = SimpleTask(task_def_name='assign_driver', task_reference_name='assign_driver_ref')
    assign_driver.input_parameters = {
        'booking_id': '${book_ride_ref.output.booking_id}'
    }
    
    make_payment = SimpleTask(task_def_name='make_payment', task_reference_name='make_payment_ref')
    make_payment.input_parameters = {
        'rider_id' : '${workflow.input.rider_id}',
        'booking_id': '${book_ride_ref.output.booking_id}'
    }
    
    confirm_booking = SimpleTask(task_def_name='confirm_booking', task_reference_name='confirm_booking_ref')
    confirm_booking.input_parameters = {
        'booking_id': '${book_ride_ref.output.booking_id}',
        'driver_id': '${assign_driver_ref.output.driver_id}'
    }

    notification_input_parameters = {
        'booking_id': '${book_ride_ref.output.booking_id}',
        'driver_id': '${assign_driver_ref.output.driver_id}',
        'rider_id' : '${workflow.input.rider_id}',
        'from' : '${workflow.input.pick_up_location}',
        'to' : '${workflow.input.drop_off_location}'
    }

    notify_driver = SimpleTask(task_def_name='notify_driver', task_reference_name='notify_driver')
    notify_driver.input_parameters = notification_input_parameters
    notify_driver.optional = True
    
    notify_customer = SimpleTask(task_def_name='notify_customer', task_reference_name='notify_customer')
    notify_customer.input_parameters = notification_input_parameters
    notify_customer.optional = True
    
    send_notifications = ForkTask(
        task_ref_name='send_notifications',
        forked_tasks=[[notify_driver], [notify_customer]],
        join_on=[]
    )

    workflow = ConductorWorkflow(
        name='cab_service_saga_demo', description="Cab Service Saga Demo", executor=workflow_executor
    )
        
    workflow >> book_ride >> assign_driver  >> make_payment  >> confirm_booking >> send_notifications
    
    workflow.input_parameters(['pick_up_location', 'drop_off_location', 'rider_id'])
    workflow.output_parameters({'booking_id': '${book_ride_ref.output.booking_id}'})
    
    metadata_client = OrkesMetadataClient(configuration)
    workflowDef = workflow.to_workflow_def()
    workflowDef.failure_workflow = 'cab_service_saga_cancellation_wf'
    metadata_client.register_workflow_def(workflowDef, overwrite=True)
    
    return workflow

def main():
    workflow = register_cab_booking_workflow()
    print("Successfully created the workflow", workflow.name)

if __name__ == '__main__':
    main()