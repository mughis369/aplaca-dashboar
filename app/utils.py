from app import api, config, record
import os
from werkzeug.datastructures import ImmutableMultiDict
import json

def get_last_update():
    if os.path.isfile('.check'):
        with open('.check', 'r') as fp:
            return fp.read()
    return "Not Available"

def set_last_update(updated_at=None):
    with open('.check', 'w') as fp:
        fp.write(updated_at)

def get_records(form):
    limit = int(form.get('limit', 20))
    sort = form.get('sort', 'latest')
    return record.read(limit=limit, sort=sort)


def get_account():
    res = api.get_account()
    return {
        'Account Number'         : res['account_number'],
        'Status'                 : res['status'],
        'Currency'               : res['currency'],
        'Buying Power'           : res['buying_power'],
        'Daytrading Buying Power': res['daytrading_buying_power'],
        'Portfolio Value'        : res['portfolio_value'],
        'Last Equity'            : res['last_equity'],
        'User since'             : res['created_at'][:19].replace('T', ' ')
    }

def handle_order_query(method, order_id=None, form=None):
    msg = ""
    tables = []
    
    methods = {
        'POST': {"func": create_order, "args": form    , "msg": "Order placed successfully!" },
        'PUT':  {"func": cancel_orders,"args": order_id, "msg": f"Order# {order_id} canceled"},
        'GET':  {"msg": ""}
    }

    if method in methods.keys():
        handler = methods[method]

        if method != 'GET':
            handler['func'](handler['args'])
        
        msg = handler['msg']
        tables = get_orders()

    else:
        return f"Request type {method} not acceptable!"
    
    print(msg, tables)
    return msg, tables

def get_orders(order_id=''):
    res = api.get_orders(order_id=order_id)
    
    if type(res) is not list:
        res = list(res)

    orders = []
    for item in res:

        order = [
            dict(key='ID'           , value=item['id']),
            dict(key='Symbol'       , value=item['symbol']),
            dict(key='Quantity'     , value=item['qty']),
            dict(key='Created on'   , value=item['created_at'][:19].replace('T', ' ')),
            dict(key='Last Updated' , value=item['updated_at'][:19].replace('T', ' ')),
            dict(key='Order Type'   , value=item['order_type']),
            dict(key='Status'       , value=item['status']),
            dict(key='Time in Force', value=item['time_in_force'])
        ]
        orders.append(order)
    return orders

def cancel_orders(order_id=''):
    return api.cancel_orders(order_id=order_id)

def create_order(form):
    api.create_order(
        symbol=form.get('symbol', 'MSFT'),
        qty=form.get('qty', '10'),
        side=form.get('side', 'buy'),
        type=form.get('type', 'market'),
        time_in_force=form.get('time_in_force', 'gtc')
    )
    # api.create_order('BABA', 97)
    # api.create_order('MSFT', 36)
    # api.create_order('NSYE', 93)
    # api.create_order('NASDAQ', 39)
    # api.create_order('TSLA', 69)
    # api.create_order('ALB', 96)
    # api.create_order('NSYE', 95)

    
if __name__ == '__main__':

    # create_order(form={})
    # print(get_orders())
    # print(cancel_orders())
    print(get_orders())