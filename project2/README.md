# project2

|    | Usefulness |
|:----:| :--------: |
|**What problem is your project solving?**|Food Waste|
|**Who would use your finished product?**|General consumer|
|**What is the smallest piece you can build that would be useful?**|Notification reminders for food expiration|
|**What are other aspects you can build that add value?**|Recipe recommendations based on available ingredients|

|    | Technology |
|:----:| :--------: |
|**What data or inputs do you need?**|Food name, category, purchase date, expiration date|
|**What will be outputted for the user?**|A SMS text message containing food items about to expire|
|**How do the inputs become outputs?**|Food item added to database -> Database returns list of food nearing expiration -> List gets sent to user via Twilio API|
|**What pieces of technology will your project use (API, database, etc)?**|Notification API to send reminders, possible API to generate recipes|