from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, TelField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
import phonenumbers as ph
from datetime import datetime

today = datetime.now().date()

choices = [
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
            "Frozen Foods",
            "Other"
        ]

class AddUser(FlaskForm):
    name = StringField('Name',
                            validators=[DataRequired(), Length(min=2, max=40)])
    phone_number = TelField('Telephone #',
                            validators=[DataRequired()])
    submit = SubmitField("Add user")

    def validate_phone(form, field):
        try:
            if not ph.is_valid_number(ph.parse(field.data, 'IN')):
                raise ValidationError("Please enter a valid phone number")
        except Exception as e:
            raise ValidationError("Please enter a valid phone number")

class AddItemForm(FlaskForm):
    item_name = StringField('Item name',
                           validators=[DataRequired(), Length(min=2, max=40)])
    purchase_date = DateField('Purchase Date', format='%Y-%m-%d',
                                    validators=[DataRequired()])
    expiration_date = DateField('Expiration Date', format='%Y-%m-%d',
                                    validators=[DataRequired()])
    submit = SubmitField('Add Item')

    def validate_purchase_date(form, field):
        if (abs(field.data - today).days) / 365 > 1:
            raise ValidationError("Please enter a purchase date within the last year")
        if field.data > today:
            raise ValidationError("Cannot input a future date")

    def validate_expiration_date(form, field):
        if field.data < today:
            raise ValidationError("Expiration date has passed.")
        if field.data < form.purchase_date.data:
            raise ValidationError("Expiration date must not be earlier than purchase date.")