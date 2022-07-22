from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN

account_sid = TWILIO_ACCOUNT_SID
auth_token  = TWILIO_AUTH_TOKEN

def sendMessage(number, message):
    """Sends an SMS message containing food about to expire"""
    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            to = f"{number}",
            from_ = "+15087383072",
            body = message
        )
        
        print(message.sid)
    except Exception as e:
        print("Twilio verified numbers only")
    