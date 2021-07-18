from celery import Celery


celery = Celery('tasks', broker='amqp://paul:paul@localhost', backend= 'db+sqlite:///db.rabbit')


