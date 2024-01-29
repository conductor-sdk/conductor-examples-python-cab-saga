from conductor.client.configuration.configuration import Configuration
from conductor.client.orkes.orkes_metadata_client import OrkesMetadataClient
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.workflow.task.simple_task import SimpleTask
from conductor.client.workflow.task.fork_task import ForkTask
from services.booking_service.booking import book_ride, confirm_booking
from services.assignment_service.assignment import assign_driver
from services.payment_service.payments import make_payment
from services.notification_service.notification import notify_customer, notify_driver

def register_cab_booking_workflow() -> ConductorWorkflow:
    configuration = Configuration()
        
    workflow_executor = WorkflowExecutor(configuration=configuration)

    workflow = ConductorWorkflow(
        name='cab_service_saga_demo_3', description="Cab Service Saga Demo", executor=workflow_executor
    )

    book = book_ride(
        task_ref_name='book_ride_ref',
        pick_up_location=workflow.input('pick_up_location'),
        drop_off_location=workflow.input('drop_off_location'),
        rider_id=workflow.input('rider_id'),
    )
    
    assign = assign_driver(task_ref_name='assign_driver_ref', booking_id=book.output('booking_id'))
    
    pay = make_payment(
        task_ref_name='make_payment_ref',
        rider_id=workflow.input('rider_id'),
        booking_id=book.output('booking_id')
    )
    
    confirm = confirm_booking(
        task_ref_name='confirm_booking_ref',
        booking_id=book.output('booking_id'),
        driver_id=assign.output('driver_id')
    )

    notification_input_params = {
        'booking_id': book.output('booking_id'),
        'driver_id': assign.output('driver_id'),
        'rider_id' : workflow.input('rider_id'),
        'from' : workflow.input('pick_up_location'),
        'to' : workflow.input('drop_off_location')
    }

    notify_d = notify_driver(task_ref_name='notify_driver_ref', **notification_input_params)
    notify_d.optional = True
    
    notify_c = notify_customer(task_ref_name='notify_customer_ref', **notification_input_params)
    notify_c.optional = True
    
    notify = ForkTask(
        task_ref_name='send_notifications',
        forked_tasks=[[notify_d], [notify_c]],
        join_on=[]
    )

    workflow >> book >> assign  >> pay  >> confirm >> notify
    
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