import os
import json, base64
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
  


def send_bulk_sms_with_attachment(numbers, body, pdf_url):
    account_sid = ACCOUNT_SID
    auth_token = AUTH_TOKEN
    client = Client(account_sid, auth_token)

    for number in numbers:
        message = client.messages.create(
            body=body,
            from_='+15484890144',  # Replace with your Twilio phone number
            to=number,
            media_url=[pdf_url]
        )
