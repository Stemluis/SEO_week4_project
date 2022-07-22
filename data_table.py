from flask import request
from datetime import *
from sms import *

def filterTable(food_item, uuid):
    query = food_item.query.filter_by(uuid=uuid)

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(food_item.item_name.like(f'%{search}%'))
    total_filtered = query.count()

    return (query, total_filtered)


def sortQuery(food_item, query):
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['id', 'item_name', 'item_category', "purchase_date", "expiration_date"]:
            col_name = 'item_name'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(food_item, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    return query


def queryResponse(food_item, uuid, query, total_filtered):
    return {
        'data': [item.to_dict() for item in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': food_item.query.filter_by(uuid=uuid).count(),
        'draw': request.args.get('draw', type=int),
    }


def removeItem(db, model, uuid, items):
    for item in items:
        model.query.filter_by(uuid=uuid, item_name=item).delete()
    db.session.commit()


def updateItem(db, model, uuid, items):
    for item in items:
        old_item = model.query.filter_by(uuid=uuid, id=item.id).first()
        new_item = food_item(
            uuid = uuid,
            purchase_date=item.purchase_date,
            expiration_date=item.expiration_date,
            item_name=item.item_name,
            item_category=item.item_category
        )
        removeItem(db, model, uuid, [old_item.item_name])
        db.session.add(new_item)
    db.session.commit()


def checkForExpired(food_item, User, user_uuid):
    today = datetime.now()
    query = food_item.query.filter(food_item.expiration_date < today).all()
    if len(query) > 0:
        message = ""
        for item in query:
            message += f'{item.item_name} expired {item.expiration_date}\n'
        
        number = User.query.filter_by(uuid=user_uuid).first().phone_number
        if False:
            sendMessage(number, message)
        return message
    else:
        return None


