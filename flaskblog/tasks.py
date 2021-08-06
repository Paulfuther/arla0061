
from celery import Celery
import os
from dotenv import load_dotenv

CELERY_BROKER_URL= os.environ.get('CELERY_BROKER_URL')

celery = Celery('tasks', broker=['CELERY_BROKER_URL'])

