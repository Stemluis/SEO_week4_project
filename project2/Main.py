from Database import *
from UserInput import *
from Api import *

def main():
    database = connectDatabase()

    if not checkDatabase(database):
        print("No previous database detected, creating new database...")
        num = prompt(phone_number, style=custom_style_2).get("phone_number")
        createTable(database, num)
    else:
        print("Existed database detectesd, using existing database...")
    
    while(True):
        next_job = prompt(program_options, style=custom_style_2).get("program")

        if next_job == "Add item":
            new_item = prompt(add_options, style=custom_style_2)
            addFoodItem(
                database,
                new_item.get("item_name"),
                new_item.get("item_category"),
                new_item.get("purchase_date"),
                new_item.get("expiration_date")
            )
        elif next_job == "Remove item":
            remove_item = prompt(remove_options, style=custom_style_2)
            removeFoodItem(database, remove_item.get("item_name"))
        elif next_job == "List items":
            printDatabase(database)
        else:
            break
    
    food = getFoodToExpire(database)
    sendMessage(food)

if __name__ == "__main__":
    main()