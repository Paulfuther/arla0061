
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

#works

CLOUDAMQP_URL = os.environ.get('CLOUDAMQP_URL')

celery = Celery('tasks', broker=CLOUDAMQP_URL)

