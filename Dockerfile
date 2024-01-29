FROM python:3.11-alpine

RUN pip3 install flask flask_restful
RUN pip3 install conductor-python

WORKDIR /app

COPY main.py /app

EXPOSE 5000

CMD ["python3", "main.py"]
