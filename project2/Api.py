from twilio.rest import Client

account_sid = "AC8024bc8fe84f1d7c1a2adf1fb26b9d82"
auth_token  = "80f170a47c6ee1260f014b97a2017325"

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
