from binance.spot import Spot
from datetime import datetime

class Trader:
    def __init__(self):
        self.key = ''
        self.secret = ''
        self.testkey = ''
        self.testsecret = ''

    """
    return if needs to call Analyst to check quote of coin lists
    """
    def checkNeedQuote(self, client):
        # Get current open order
        OpenOrder = client.get_open_orders()

        if len(OpenOrder) == 1:
            if OpenOrder[0]['side'] == "SELL":
                print("Open order need to be filled on " + OpenOrder[0]['symbol'] + " @ " + OpenOrder[0]['price'])
                return False
            else:
                print("Error!!: there is a BUY order not filled")
                return False
        elif len(OpenOrder) == 0:
            print("Calling Analyst to get quote now ...")
            return True
        else:
            print("Error!!: more than 1 open order")
            return False






