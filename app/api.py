import requests
import json
from config import ORDERS_URL, HEADERS, ACCOUNT_URL


def create_order(symbol, qty, side='buy', type='market', time_in_force='gtc'):
    """
    Places a new order for the given key and secret against provided parameters.
    str ->  symbol       := asset ID to identify the asset to trade ex:MSFT
    int ->  qty          := asset ID to identify the asset to trade
    str ->  side         := 'buy' or 'sell'
    str ->  type         := 'market', 'limit', 'stop', 'stop_limit', or 'trailing_stop'
    str ->  time_in_foce := day, gtc, opg, cls, ioc, fok.
    """
    data = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": type,
        "time_in_force": time_in_force
    }
    r = requests.post(ORDERS_URL, headers=HEADERS, json=data)
    return json.loads(r.content)

def get_orders(order_id=None):
    """
    Retrieves a list of orders for the account, filtered by the supplied id.
    returns all orders if order_id is None
    """
    URL = ORDERS_URL

    if order_id:
        URL = f"{ORDERS_URL}/{order_id}"

    r = requests.get(f"{URL}", headers=HEADERS)
    return json.loads(r.content)

def cancel_orders(order_id=None):
    """
    Attempts to cancel all open orders or a specific if order_id is provided.
    """
    URL = ORDERS_URL

    if order_id:
        URL = f"{ORDERS_URL}/{order_id}"

    r = requests.delete(f"{URL}", headers=HEADERS)
    return r.content


def get_account():
    """ Returns the account associated with the API key."""
    r = requests.get(ACCOUNT_URL, headers=HEADERS)
    return json.loads(r.content)



if __name__ == '__main__':

#     print(create_order('BABA', 97))
#     print(create_order('MSFT', 36))
#     print(create_order('NSYE', 93))
#     print(create_order('NASDAQ', 39))
#     print(create_order('TSLA', 69))
#     print(create_order('ALB', 96))
#     print(create_order('NSYE', 95))

    print(get_orders())