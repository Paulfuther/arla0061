
from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

#CELERY_BROKER_URL= os.environ.get('CELERY_BROKER_URL')
#USR='codfish.rmq.cloudamqp.com'
AMPUSER='ftrhyovk'
AMPPASSWORD='L-8g5-R5eGgBOzBPYAgKG1axKplnz4yy'

CLOUDAMQP_URL = os.environ.get('CLOUDAMQP_URL')

#amp_authority = '(ampq_userinfo)@codfish.rmq.cloudamqp.com:5671/ftrnhyovk'
#amp_userinfo = 'ftrhyovk:L-8g5-R5eGgBOzBPYAgKG1axKplnz4yy'
#amqps_URI = 'ampqs://(amp_authority)'

celery = Celery('tasks', broker=CLOUDAMQP_URL)

#celery = Celery('tasks', broker='amqps://[USR]/ftrhyovk') 

#celery = Celery('tasks', broker= 'amqps://ftrhyovk:L-8g5-R5eGgBOzBPYAgKG1axKplnz4yy@codfish.rmq.cloudamqp.com/ftrhyovk')

#celery = Celery('tasks',broker= 'amqps://'AMPUSER:AMPPASSWORD'@codfish.rmq.cloudamqp.com/ftrhyovk')

#celery = Celery('tasks', amqps_URI)