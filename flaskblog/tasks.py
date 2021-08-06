
from celery import Celery


celery = Celery('tasks', broker='amqps://ftrhyovk:L-8g5-R5eGgBOzBPYAgKG1axKplnz4yy@codfish.rmq.cloudamqp.com/ftrhyovk')

