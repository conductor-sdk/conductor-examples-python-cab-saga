from flask import Flask, request
from flask_restful import Api
from workflow import register_cab_booking_workflow
from conductor.client.configuration.configuration import Configuration
from conductor.client.orkes.orkes_workflow_client import OrkesWorkflowClient

app = Flask(__name__)
api = Api(app)

@app.route('/', methods=['GET'])
def hello():
    return "Hello from Orkes' Cab Booking App!"

@app.route('/booking', methods=['POST'])
def booking():
    request_data = request.get_json()
        
    workflow_client = OrkesWorkflowClient(Configuration())
    
    # In case workflow definition is not created from before
    workflow = register_cab_booking_workflow()
    
    workflow_input = {
        'pick_up_location': request_data['pickUpLocation'],
        'drop_off_location': request_data['dropOffLocation'],
        'rider_id': request_data['riderId']
    }
    workflow_id = workflow_client.start_workflow_by_name(workflow.name, workflow_input)
    
    return { 'created_workflow_id' : workflow_id }

if __name__ == '__main__':
    # Run app
    app.run(host='0.0.0.0', port=5000)