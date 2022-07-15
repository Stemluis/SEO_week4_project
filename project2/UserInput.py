import re
import phonenumbers as ph
from PyInquirer import prompt
from examples import custom_style_2
from prompt_toolkit.validation import Validator, ValidationError


class DateValidator(Validator):
    def validate(self, document):
        if not re.match("\d{4}-\d{1,2}-\d{1,2}", document.text):
            raise ValidationError(
                message="Please enter a valid date (yyyy-mm-dd)",
                cursor_position=len(document.text)
            )


class PhoneValidator(Validator):
    def validate(self, document):
        try:
            if not ph.is_valid_number(ph.parse(document.text, 'IN')):
                raise Exception
        except Exception as e:
            raise ValidationError(
                message="Please enter a valid phone number",
                cursor_position=len(document.text)
            )
        

phone_number = [
    {
        'type': 'input',
        'name': 'phone_number',
        'message': 'Please enter your phone number:',
        'validate': PhoneValidator
    }
]

program_options = [
    {
        'type': 'list',
        'name': 'program',
        'message': 'Select program action',
        'choices': [
            "Add item",
            "Remove item", 
            "List items",
            "Exit"
        ]
    }
]

add_options = [
    {
        'type': 'input',
        'name': 'item_name',
        'message': 'Enter item name:',
    },
    {
        'type': 'list',
        'name': 'item_category',
        'message': 'Please select a food category:',
        'choices': [
            "Grocery",
            "Fruits",
            "Vegetables",
            "Canned Goods",
            "Dairy",
            "Meat",
            "Seafood",
            "Deli",
            "Condiments/Spices",
            "Snacks",
            "Bread/Baked Goods",
            "Beverages",
            "Pasta/Rice/Cereal",
            "Baking",
            "Frozen Foods"
        ]
    },
    {
        'type': "input",
        "name": "purchase_date",
        "message": "Enter the date purchased",
        "validate": DateValidator
    },
    {
        'type': "input",
        "name": "expiration_date",
        "message": "Enter the expiration date",
        "validate": DateValidator
    }
]

remove_options = [
    {
        'type': 'input',
        'name': 'item_name',
        'message': 'Enter item to remove:',
    }
]
