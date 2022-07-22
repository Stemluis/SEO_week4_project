from twilio.rest import Client

account_sid = "AC4cc08179533042f69e03ae5520dd96df"
auth_token  = "49a8279d546bfd73b7ef09fa9b447e97"

def sendMessage(number, message):
    """Sends an SMS message containing food about to expire"""
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to = f"{number}",
        from_ = "+15087383072",
        body = message
    )
    
    print(message.sid)