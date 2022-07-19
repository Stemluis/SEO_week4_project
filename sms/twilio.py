from twilio.rest import Client

account_sid = "AC4cc08179533042f69e03ae5520dd96df"
auth_token  = "0684ea27ebdc1a160668c2d09d988757"

def sendMessage(food_list):
    """Sends an SMS message containing food about to expire"""
    client = Client(account_sid, auth_token)

    if len(food_list) > 0:
        messageStr = ""
        for food_item in food_list:
            messageStr += f"""
                The item {food_item[1]} is about to expire 
                in {food_item[2]} days ({food_item[3]})\n
            """

        message = client.messages.create(
            to = f"{food_list[0][0]}",
            from_ = "+19707164530",
            body = f"{messageStr}")
        
        print(message.sid)