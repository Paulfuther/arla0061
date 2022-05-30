import os
import json
from twilio.rest import Client

ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
NOTIFY_SERVICE_SID = os.getenv('TWILIO_NOTIFY_SERVICE_SID')

client = Client(ACCOUNT_SID, AUTH_TOKEN)


def send_bulk_sms(numbers, body):
    bindings = list(map(lambda number: json.dumps({"binding_type":"sms","address": number}), numbers))
    print("=====> To Bindings :>", bindings, "<: =====")
    notification = client.notify.services(NOTIFY_SERVICE_SID)\
        .notifications.create(
            to_binding=bindings,
        body=body)
  
    