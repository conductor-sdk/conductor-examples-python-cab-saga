# conductor-examples-python-cab-saga
Cab Booking Distributed Python Service

## Installation

### Install Docker
https://docs.docker.com/engine/install/

### Install Python
https://www.python.org/downloads/

### Install Modules
```shell
pip3 install -r requirements.txt
```

## Setup
Setup authentication using the below link and store environment variables in a .env file.

https://github.com/conductor-sdk/conductor-python?tab=readme-ov-file#setup-sdk

## App Structure

This app has 6 components:
1. Flask server that servers the booking endpoint to trigger booking workflow
2. Booking Service
3. Assignment Service
4. Payment Service
5. Notification Service
6. Workflow definition creation script

## Create Workflow
```shell
python3 workflows.py
```

## Run Cab Booking Server
```shell
python3 main.py
```

# Run microservice based workers
```shell
docker compose up
```

## Trigger Booking Creation

### Booking Creation Success: Happy Path

```curl
curl --location 'http://127.0.0.1:5000/booking' \
--header 'Content-Type: application/json' \
--data '{
    "pickUpLocation": "15 Mark Chester Pl, Chicago, IL 12045",
    "dropOffLocation": "64 West 21st Street, Chicago, IL 13012",
    "riderId": 1
}'
```

### Booking Creation Failure: Distributed Rollback

To simulate a distributed rollback in a Saga based microservice architecture, we make the payment fail for all riders with id > 2 which leads to terminate the main workflow and trigger a failure workflow.

```curl
curl --location 'http://127.0.0.1:5000/booking' \
--header 'Content-Type: application/json' \
--data '{
    "pickUpLocation": "15 Mark Chester Pl, Chicago, IL 12045",
    "dropOffLocation": "64 West 21st Street, Chicago, IL 13012",
    "riderId": 3
}'
```