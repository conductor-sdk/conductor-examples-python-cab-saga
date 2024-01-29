FROM python:3.11-alpine

RUN pip3 install conductor-python

WORKDIR /app

COPY assignment.py /app/assignment.py
COPY main.py /app/main.py

EXPOSE 5000

CMD ["python3", "main.py"]