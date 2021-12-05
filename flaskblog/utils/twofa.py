import os
import json
from twilio.rest import Client

ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_VERIFY_SID = os.getenv('TWILIO_VERIFY_SID')

client = Client(ACCOUNT_SID, AUTH_TOKEN)


def twofa(number):
    verification = client.verify\
        .services(TWILIO_VERIFY_SID)\
            .verifications\
                .create(to=number, channel='sms')
  
    