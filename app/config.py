class Config(object):
    JOBS = [
        {
            'id': 'job-1',
            'func': 'jobs:streamer'
        }
    ]

    SCHEDULER_API_ELABLED=True

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class DebugConfig(Config):
    DEBUG = True
    TESTING = True

class TestingConfig(Config):
    TESTING = True

PRODUCTION_CONFIG=ProductionConfig()
DEBUG_CONFIG=DebugConfig()
TESTING_CONFIG=TestingConfig()


WS_ENDPOINT="wss://data.alpaca.markets/stream"
BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = f"{BASE_URL}/v2/account"
ORDERS_URL = f"{BASE_URL}/v2/orders"


API_KEY="PKQME4JPS6TC13GZEMYF"
SECRET="sgq7UQh51RGj5Vdvfr6KhAnDceVKFc9guzHAWknn"
HEADERS = {
    "APCA-API-KEY-ID":     API_KEY, 
    "APCA-API-SECRET-KEY": SECRET
}



WS_AUTH={
    "action": "authenticate",
    "data": {
        "key_id": API_KEY,
        "secret_key": SECRET
    }
}

WS_LISTEN={
    "action": "listen", 
    "data": {
        "streams": ["AM.*"]
    }
}
