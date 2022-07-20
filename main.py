from flask import Flask, render_template, url_for, flash, redirect, make_response, request, session
from forms import AddUser, AddItemForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash as idHash 

app = Flask(__name__)
proxied = FlaskBehindProxy(app)  ## add this line
app.config['SECRET_KEY'] = 'ea7c8cf166ec194d38b0cfd171d58bc0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class food_item(db.Model):
    __tablename__ = 'food_items'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(64), nullable=False)
    purchase_date = db.Column(db.Date(), nullable=False)
    expiration_date = db.Column(db.Date(), nullable=False)
    item_name = db.Column(db.String(40), nullable=False)
    item_category = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return f"Food({self.item_name}, {self.expiration_date})"

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return f"Food({self.name}, {self.phone_number})"

db.create_all()

@app.route("/")
@app.route("/home")
def home():
    if not session.get("uuid"):
        return redirect(url_for('about'))
    else:
        return render_template('home.html', subtitle='Home')


@app.route("/show")
def show():
    if not session.get("uuid"):
        return render_template('show.html', subtitle='Items', food_items=food_item.query.all())
    else:
        return render_template('show.html', subtitle='Items', food_items=food_item.query.filter_by(uuid=session.get("uuid")))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if session.get("uuid"):
        return redirect(url_for("home"))

    form = AddUser()
    if form.validate_on_submit(): # checks if entries are valid
        check_user = User.query.filter_by(phone_number=form.phone_number.data)

        if check_user.count() == 0:
            user = User(
                        name=form.name.data,
                        phone_number=form.phone_number.data,
                        uuid = idHash(form.phone_number.data + form.name.data).decode('utf-8')
                    )
            db.session.add(user)
            db.session.commit()
            session["uuid"] = user.uuid
            session["name"] = user.name
        else:
            session["uuid"] = check_user[0].uuid
            session["name"] = check_user[0].name

        return redirect(url_for("home"))
    return render_template('login.html', title='Add user', form=form)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for("about"))    

@app.route("/add", methods=['GET', 'POST'])
def add():
    if not session.get("uuid"):
        return redirect(url_for('login'))

    form = AddItemForm()
    if form.validate_on_submit(): # checks if entries are valid
        item = food_item(
                        uuid = session.get("uuid"),
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

@app.route("/about", methods=['GET'])
def about():
    return render_template('about.html', title='About')

@app.route("/support", methods=['GET'])
def support():
    return render_template('support.html', title='Support')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
