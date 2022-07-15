import phonenumbers
from phonenumbers import timezone
#install the phone number module first
# This is used to accept the user inputs and will be eventually stored in a database.
# Save name and phone number once. It'll be used for notifications for the user.
# Inputs needed: Name, Phone number, email(optional), food items bought.
# Automatically note the dates for the food items input. 

#Notifood UI 
 

name = input("Enter your full name: ")

# Program to convert input to
# phonenumber format
  
# Parsing String to Phone number
# Phone number format: (+Countrycode)xxxxxxxxxx
digit = input("Enter your digits in the format (+Countrycode)xxxxxxxxxx: ")
phoneNumber = phonenumbers.parse(digit)
# Pass the parsed phone number in below function
timeZone = timezone.time_zones_for_number(phoneNumber)
# This will print the phone number and 
# it's basic details.
print(phoneNumber)
print(timeZone)


text = """ Available categories of food items are:
    Fruits — Apples, bananas, etc. 
    Vegetables - Potatoes, onions, carrots, etc. 
    Canned goods — Soup, tuna, fruit, beans, etc. 
    Dairy — Butter, cheese, eggs, milk,etc. 
    Meat — Chicken, beef, pork, sausage, bacon etc. 
    Fish and Seafood— Shrimp, crab, cod, tuna, etc. 
    Deli— Cheese, salami, etc.
    Condiments and Spices— Black pepper, oregano, etc.
    Snacks— Chips, pretzels, popcorn, crackers, nuts, etc.
    Bread and Bakery— Bread, tortillas, pies, muffins, bagels, cookies, etc.
    Beverages — Coffee, teabags, milk, juice, soda, beer, wine, etc.
    Pasta, Rice and Cereal — Oats, granola, brown rice, etc. 
    Baking — Flour, powdered sugar, baking powder, etc. 
    Frozen Foods — Pizza, ready meals, ice cream, etc. 
    
    TAKE NOTE OF THE CATEGORIES FOR YOUR FOOD ITEMS."""

def format_sentence(sentence):
    print(sentence.replace('. ', '.\n'))
format_sentence(text)


Grocery = []
Fruits = []
Vegetables = []
Canned_Goods = []
Dairy = []
Meat = []
Fish_and_Seafood = []
Deli = []
Condiments_and_Spices = []
Snacks = []
Bread_and_Bakery = []
Beverages = []
Pasta_Rice_Cereal = []
Baking = []
Frozen_Foods = []

#Create a list to store the user's input individually
item = []
item.append([])
item.append([])
item.append([])
item.append([])
item.append([])
item.append([])
item.append([])
item.append([])
item.append([])
item.append([])
item.append([])
item.append([])
item.append([])
item.append([])

i = 0
while True:
    Name = input("Name of item: ")
    if Name == "":
        break
    else:
        category = input("Category: ")
        Purchase_date = input("Date purchased(Year-month-date): ")
        Expiration_date = input("Expiration date(Year-month-date): ")
        item[i].append(Name)
        item[i].append(category)
        item[i].append(Purchase_date)
        item[i].append(Expiration_date)
        
        if item[i][1].capitalize() == 'Fruits':
            Fruits.append(item[i])
        if item[i][1].capitalize() == 'Vegetables':
            Vegetables.append(item[i])
        elif item[i][1].capitalize() == 'Canned goods':
            Canned_Goods.append(item[i])
        elif item[i][1].capitalize() == 'Dairy':
            Dairy.append(item[i])
        elif item[i][1].capitalize() == 'Meat':
            Meat.append(item[i])
        elif item[i][1].capitalize() == 'Fish and Seafood':
            Fish_and_Seafood.append(item[i])
        elif item[i][1].capitalize() == 'Deli':
            Deli.append(item[i])
        elif item[i][1].capitalize() == 'Condiments and Spices':
            Condiments_and_Spices.append(item[i])
        elif item[i][1].capitalize() == 'Snacks':
            Snacks.append(item[i])
        elif item[i][1].capitalize() == 'Bread and Bakery':
            Bread_and_Bakery.append(item[i])
        elif item[i][1].capitalize() == 'Beverages':
            Beverages.append(item[i])
        elif item[i][1].capitalize() == 'Pasta, Rice, and Cereal':
            Pasta_Rice_Cereal.append(item[i])
        elif item[i][1].capitalize() == 'Baking':
            Baking.append(item[i])
        elif item[i][1].capitalize() == 'Frozen foods':
            Frozen_Foods.append(item[i])
        
        i+=1

print("Fruits available are: " Fruits)
print("Vegetables available are: " Vegetables)
print("Canned goods available are: " Canned_Goods)
print("Dairy products available are: " Dairy)
print("Meat products available are: " Meat)
print("Fish and Seafood items available are: " Fish_and_Seafood)
print("Deli products available are: " Deli)
print("Condiments and Spices available are: " Condiments_and_Spices)
print("Snacks available are: " Snacks)
print("Bread and Bakery items available are: " Bread_and_Bakery)
print("Beverages available are: " Beverages)
print("Pasta, Rice, and Ceral items available are: " Pasta_Rice_Cereal)
print("Baking items available are: " Baking)
print("Frozen foods available are: " Frozen_Foods)
