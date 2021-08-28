
from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

#works

CLOUDAMQP_URL = os.environ.get('CLOUDAMQP_URL')

celery = Celery('tasks', broker=CLOUDAMQP_URL)

