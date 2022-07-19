from flask import Flask, render_template, url_for, flash, redirect
from forms import AddUser, AddItemForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash as idHash

app = Flask(__name__)
proxied = FlaskBehindProxy(app)  ## add this line
app.config['SECRET_KEY'] = 'ea7c8cf166ec194d38b0cfd171d58bc0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class food_item(db.Model):
  id = db.Column(db.String(64), nullable=False)
  purchase_date = db.Column(db.Date(), nullable=False)
  expiration_date = db.Column(db.Date(), nullable=False)
  item_name = db.Column(db.String(40), nullable=False)
  item_category = db.Column(db.String(40), nullable=False)

  def __repr__(self):
    return f"Food({self.item_name}, {self.expiration_date})"

class User(db.Model):
    id = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    phone_number = db.Column(sb.String(15), nullable=False)

    def __repr__(self):
        return f"Food({self.name}, {self.phone_number})"

@app.route("/")
@app.route("/home")
def home():
    if len(db.engine.table_names()) < 1:
        db.create_all()
        return redirect(url_for('new'))
    else:
        return render_template('home.html', subtitle='Home', food_items=food_item.query.all())

@app.route("/new", methods=['GET', 'POST'])
def new():
    form = AddUser()
    if form.validate_on_submit(): # checks if entries are valid
        user = User(
                    name=form.name.data
                    phone_number=form.phone_number.data
                    id = idHash(phone_number)
                )
        return render_template('home.html', title="Home")
    return render_template('new.html', title='Add Phone', form=form)

@app.route("/add", methods=['GET', 'POST'])
def add():
    form = AddItemForm()
    if form.validate_on_submit(): # checks if entries are valid
        item = food_item(
                        purchase_date=form.purchase_date.data,
                        expiration_date=form.expiration_date.data,
                        item_name=form.item_name.data,
                        item_category=form.item_category.data
                    )
        db.session.add(item)
        db.session.commit()
        flash(f'{form.item_name.data} added!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('add.html', title='Add Item', form=form)

# @app.route("/show", methods=['GET', 'POST'])
# def show():
#     return render_template('show.html', title='Show', food_items=food_item.query.all())

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
