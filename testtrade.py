from Analyst import Analyst
from Trader import Trader
from binance.spot import Spot
import logging
from binance.lib.utils import config_logging
from binance.error import ClientError
import time



logger = logging.getLogger()
handler = logging.FileHandler('logfile.log')
logger.addHandler(handler)

trader = Trader()
analyst = Analyst()
######test order
client = Spot(key=trader.testkey, secret=trader.testsecret, base_url="https://testnet.binance.vision")
print(client.account()["balances"])
OpenOrder = client.get_open_orders()
print(OpenOrder[1])
OldOrder = client.my_trades("BTCUSDT")

##### get USDT
"""
for filter in client.exchange_info(symbol="BNBUSDT")['symbols'][0]['filters']:
    if filter['filterType'] == 'LOT_SIZE':
        print(filter)
        orderFilter = filter
        break
print(client.ticker_price("BNBUSDT"))
print("{:0.0{}f}".format(0.5, 2))
params = {
    "symbol": "BNBUSDT",
    "side": "SELL",
    "type": "LIMIT",
    "timeInForce": "GTC",
    "quantity": 100,
    "price": 410,
}



try:
    response = client.new_order(**params)
    logger.error(response)
except ClientError as error:
    logger.error(
        "Found error. status: {}, error code: {}, error message: {}".format(
            error.status_code, error.error_code, error.error_message
        )
    )

print("BNBBUSD SOLD")

OpenOrder = client.get_open_orders()
print(OpenOrder)
"""
##### full process

"""
BuyTicker = "BTCUSDT"
BTC = 0.0
symbolPrice = 0.0
print(client.ticker_price(BuyTicker))
TickerPrice = client.ticker_price(BuyTicker)
symbolPrice = float(TickerPrice['price'])
print(client.account()["balances"])
for asset in client.account()["balances"]:
    if asset['asset'] == 'USDT':
        USDT = float(asset['free'])
        break


quantity = USDT/symbolPrice
"""
#price precision fixed to 4 to save time
#quantity precision fixed to 2 to save time
"""
pricePrecision = 4
quantityPrecision = 2
print("{:0.0{}f}".format(quantity, quantityPrecision))

params = {
    "symbol": BuyTicker,
    "side": "BUY",
    "type": "MARKET",
    # precision is determined by lot size, minQty 0.000001 which has 6 decimials
    "quantity": "{:0.0{}f}".format(quantity, quantityPrecision)
}

"""
#response sample
#{'symbol': 'BTCBUSD', 'orderId': 2008429, 'orderListId': -1, 'clientOrderId': 'qerbZbDHjuIPWkGBNlTtO6', 'transactTime': 1650206144116, 'price': '0.00000000', 'origQty': '0.24867700', 'executedQty': '0.24867700', 'cummulativeQuoteQty': '9999.99597883', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'BUY', 'fills': [{'price': '40212.79000000', 'qty': '0.24867700', 'commission': '0.00000000', 'commissionAsset': 'BTC', 'tradeId': 519304}]}
"""
try:
    response = client.new_order(**params)
    if len(response['fills'])>0:

        print("filledPrice: " + response['fills'][0]['price'])
        logger.error(response)

        filledPrice = float(response['fills'][0]['price'])
        # Place Limit Order to take Profit
        targetPrice = filledPrice * 1.2
        BTC = 0
        for asset in client.account()["balances"]:
            if asset['asset'] == BuyTicker.replace("USDT",""):
                BTC = float(asset['free'])
                break

        # quantity = BNB * targetPrice
        #
        quantity = BTC
        params = {
            "symbol": "BuyTicker",
            "side": "SELL",
            "type": "LIMIT",
            "timeInForce": "GTC",
            "quantity": "{:0.0{}f}".format(quantity, quantityPrecision),
            "price": "{:0.0{}f}".format(targetPrice, pricePrecision)
        }

        try:
            response = client.new_order(**params)
            print(response)
            logging.error(response)
        except ClientError as error:
            logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )
        OpenOrder = client.get_open_orders()
        print(OpenOrder)

except ClientError as error:
    logger.error(
        "Found error. status: {}, error code: {}, error message: {}".format(
            error.status_code, error.error_code, error.error_message
        )
    )


"""









###### tedious quantity calculation
"""
orderFilter = None
#find lot size
for filter in client.exchange_info(symbol=BuyTicker)['symbols'][0]['filters']:
    print(client.exchange_info(symbol=BuyTicker)['symbols'][0]['baseAssetPrecision'])
    if filter['filterType'] == 'LOT_SIZE':
        print(filter)
        orderFilter = filter
        break

#compute quantity, format to precision

minQty = float(orderFilter['minQty'])
precision = 0

if 'e' in str(minQty):
    precision = int(str(minQty).split('e')[1])
    if precision >= 0:
        precision = 0
    else:
        precision = -precision
"""












