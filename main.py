from flask import Flask, render_template, url_for, flash, redirect, make_response, request, session
from forms import AddUser, AddItemForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash as idHash 
from data_table import *
from config import SECRET_KEY
from ics import Calendar, Event
from datetime import *
import re
import json


app = Flask(__name__)
proxied = FlaskBehindProxy(app)  ## add this line
app.config['SECRET_KEY'] = SECRET_KEY
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

    def to_dict(self):
        return {
            'id':self.id,
            'item_name': self.item_name,
            'item_category': self.item_category,
            'purchase_date': self.purchase_date.strftime("%m/%d/%Y"),
            'expiration_date': self.expiration_date.strftime("%m/%d/%Y"),
        }

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return f"User({self.name}, {self.phone_number})"

db.create_all()

@app.route("/")
@app.route("/home")
def home():
    if not session.get("uuid"):
        return redirect(url_for('about'))
    else:
        if not session.get("announced"):
            message = checkForExpired(food_item, User, session.get("uuid"))
            session['announced'] = True
            return render_template('home.html', subtitle='Home', message=message)
        else:
            return render_template('home.html', subtitle='Home', message="")


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


@app.route("/add/<string:category>", methods=['GET', 'POST'])
def add(category):
    if not session.get("uuid"):
        return redirect(url_for('login'))
    
    category = re.sub("-", " ", category)
    category = re.sub("_", "/", category)

    form = AddItemForm()
    if form.validate_on_submit(): # checks if entries are valid
        item = food_item(
                        uuid = session.get("uuid"),
                        purchase_date=form.purchase_date.data,
                        expiration_date=form.expiration_date.data,
                        item_name=form.item_name.data,
                        item_category=category
                    )
        db.session.add(item)
        db.session.commit()
        # flash(f'{form.item_name.data} added!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('add.html', title='Add Item', form=form, category=category)


@app.route("/show")
def show():
    # return render_template('test_test_table.html', subtitle="Test Table")
    # if not session.get("uuid"):
    #     return render_template('show.html', subtitle='Items', food_items=food_item.query.all(), today=datetime.datetime.now())
    # else:
    return render_template('show.html', subtitle='Items', food_items=food_item.query.filter_by(uuid=session.get("uuid")), today=datetime.now().date())


@app.route('/api/data')
def data():
    uuid = session.get("uuid")
    (query, total_filtered) = filterTable(food_item, uuid)
    query = sortQuery(food_item, query)
    return queryResponse(food_item, uuid, query, total_filtered)


@app.route('/api/remove/<string:item_name>', methods=['POST'])
def remove(item_name):
    uuid = session.get("uuid")
    removeItem(db, food_item, uuid, [item_name])
    return redirect(url_for("show"))

@app.route('/api/update', methods=['POST'])
def update():
    uuid = session.get("uuid")
    data = request.json
    # print(data)
    new_item = {
        "id": data["id"],
        "item_name": data["item_name"],
        "item_category": data["item_category"],
        "purchase_date": data["purchase_date"],
        "expiration_date": data["expiration_date"]
    }
    updateItem(db, food_item, uuid, [item_name])
    return redirect(url_for("show"))

@app.route('/export', methods=['POST', 'GET'])
def export():
    uuid = session.get("uuid")
    _calendar = createCalendar(uuid, datetime.now().date())
    data = open('calendar.ics', 'r').read()
    response = make_response(data)
    response.headers["Content-Disposition"] = "attachment; filename=calendar.ics"
    return response
    # return redirect(url_for("show"))

@app.route("/about", methods=['GET'])
def about():
    return render_template('about.html', title='About')


@app.route("/support", methods=['GET'])
def support():
    return render_template('support.html', title='Support')

def createCalendar(uuid, today):
    cal = Calendar()

    query = food_item.query.filter(food_item.expiration_date > today).all()
    for item in query:
        e = Event()
        e.name = f'{item.item_name} expires'
        e.begin = item.expiration_date.strftime("%Y-%m-%d %X")
        cal.events.add(e)

    with open('calendar.ics', 'w') as f:
        f.writelines(cal.serialize_iter())

    return cal


def createFakeData():
    try:
        file = open('MOCK_DATA.json')
    except Exception as e:
        print("File not found")
    
    data = json.load(file)
    for item in data:
        newItem = food_item(
            uuid = item['uuid'],
            purchase_date=datetime.strptime(item['purchase_date'], '%Y/%m/%d'),
            expiration_date=datetime.strptime(item['expiration_date'], '%Y/%m/%d'),
            item_name=item['item_name'],
            item_category=item['item_category']
        )
        db.session.add(newItem)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
