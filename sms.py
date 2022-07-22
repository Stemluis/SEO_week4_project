from twilio.rest import Client

account_sid = "AC4cc08179533042f69e03ae5520dd96df"
auth_token  = "8582ec59b682cfb80fa8149f183a0a00"

def sendMessage(number, message):
    """Sends an SMS message containing food about to expire"""
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to = f"{number}",
        from_ = "+15087383072",
        body = message
    )
    
    print(message.sid)