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
client = Spot(key=trader.key, secret=trader.secret)


if trader.checkNeedQuote(client):
    order = analyst.checkTradableUnderValued(client)
    if order == {}:
        print("No signal")
    else:
        print(order)















