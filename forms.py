from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, TelField, SubmitField
from wtforms.validators import DataRequired, Length
import phonenumbers as ph

choices = [
            ("Grocery", "Grocery"),
            ("Fruits", "Fruits"),
            ("Vegetables", "Vegetables"),
            ("Canned Goods", "Canned Goods"),
            ("Dairy", "Dairy"),
            ("Meat", "Meat"),
            ("Seafood", "Seafood"),
            ("Deli", "Deli"),
            ("Condiments/Spices", "Condiments/Spices"),
            ("Snacks", "Snacks"),
            ("Bread/Baked Goods", "Bread/Baked Goods"),
            ("Beverages", "Beverages"),
            ("Pasta/Rice/Cereal", "Pasta/Rice/Cereal"),
            ("Baking", "Baking"),
            ("Frozen Foods", "Frozen Foods")
        ]

class AddPhone(FlaskForm):
    phone_number = TelField('Telephone #',
                            validators=[DataRequired()])
    submit = SubmitField("Add phone number")

    def validate_phone(form, field):
        try:
            if not ph.is_valid_number(ph.parse(field.data, 'IN')):
                raise ValidationError("Please enter a valid phone number")
        except Exception as e:
            raise ValidationError("Please enter a valid phone number")

class AddItemForm(FlaskForm):
    item_name = StringField('Item name',
                           validators=[DataRequired(), Length(min=2, max=40)])
    item_category = SelectField('Item Category', choices=choices,
                        validators=[DataRequired()])
    purchase_date = DateField('Purchase Date', format='%Y-%m-%d',
                                    validators=[DataRequired()])
    expiration_date = DateField('Expiration Date', format='%Y-%m-%d',
                                    validators=[DataRequired()])
    submit = SubmitField('Add Item')

    def validate_expiration_date(form, field):
        if field.data < form.purchase_date.data:
            raise ValidationError("End date must not be earlier than start date.")