from celery import Celery


celery = Celery('tasks', broker='amqp://guest:guest@localhost')

