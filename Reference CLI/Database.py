import os
import json
import sqlalchemy as db
import pandas as pd

def deleteExistingDatabase():
    myfile = "Notifood.db"
    if os.path.isfile(myfile):
        os.remove(myfile)


def connectDatabase():
    """Connects to the SQL database"""
    return db.create_engine('sqlite:///Notifood.db')

def checkDatabase(database):
    """Checks for existing data in database"""
    if len(database.table_names()) < 2:
        return False
    return True

def createTable(engine, phone_number):
    """Creates a table for food items"""
    engine.execute( 
        f"""
            CREATE TABLE food_items(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number VARCHAR(15) DEFAULT {phone_number} NOT NULL,
                purchase_date DATE,
                expiration_date DATE,
                item_name VARCHAR(100),
                item_category VARCHAR(40)
            );
        """
    )


def addFoodItem(engine, name, category, purchase_date, expiration_date):
    """Adds a food item to the database"""
    engine.execute(
        f"""
            INSERT INTO food_items(
                purchase_date,
                expiration_date,
                item_name,
                item_category)
            VALUES(
                \'{purchase_date}\',
                \'{expiration_date}\',
                \'{name}\',
                \'{category}\'
            );
        """
    )


def removeFoodItem(engine, name):
    """Removes a food item from the database"""
    try:
        engine.execute(
            f"""
                DELETE FROM food_items
                WHERE item_name = \"{name}\"
            """
        )
    except Exception as e:
        print("Item doesn't exist!")


def printDatabase(engine):
    """Prints the query table from the database"""
    query_result = engine.execute(f"SELECT * FROM food_items;").fetchall()
    print(pd.DataFrame(query_result))


def getFoodToExpire(engine):
    """Searches database and returns items set to expire within a week"""
    query = engine.execute(
        """
            SELECT 
                phone_number,
                item_name,
                CAST(julianday(expiration_date) - julianday('now') AS INTEGER),
                expiration_date FROM food_items
            WHERE julianday(expiration_date) - julianday('now') < 7;
        """
    )
    return pd.DataFrame(query).values
