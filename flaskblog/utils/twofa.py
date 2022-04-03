import os
import json
from twilio.rest import Client, TwilioException
from flask import app

ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_VERIFY_SID = os.getenv('TWILIO_VERIFY_SID')

client = Client(ACCOUNT_SID, AUTH_TOKEN)
  

def _get_twilio_verify_client():
    return Client(
        ACCOUNT_SID, AUTH_TOKEN
        ).verify.services(TWILIO_VERIFY_SID)
    
def request_verification_token(phone):
    verify = _get_twilio_verify_client()
    try:
        verify.verifications.create(to=phone, channel='sms')
    except TwilioException:
        verify.verifications.create(to=phone, channel='call')


def check_verification_token(phone, token):
    verify = _get_twilio_verify_client()
    try:
        result = verify.verification_checks.create(to=phone, code=token)
    except TwilioException:
        return False
    return result.status == 'approved'