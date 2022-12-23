from binance.spot import Spot
from datetime import datetime
import time

class Analyst:

    def __init__(self):
        """
        The order of keys are in descending order of Market Cap
        Valuation needs to be refreshed every week
            ===> Last refresh date:16 Apr 2022
            ===> Need to add: ADAUSDT, ETCUSDT
        """
        self.MonitorCoinpairValuation = {
            "BTCUSDT": 39970,
            "ETHUSDT": 3000,
            "BNBUSDT": 412,
            "XRPUSDT": 0.7,
            "SOLUSDT": 99,
            "LUNAUSDT": 79.5,
            "APEUSDT": 12.1
        }

        """
        in %
        """
        self.ProfitRoom = 2
        self.DownSideCheck = -1
        #check there is no crazy price movement
        self.PriceChangeCheck = 6

    """
    return undervalued currency pair with largest priority to trade
    return result: {'symbol': 'ETCUSDT', 'price': '38.40000000'}
    """
    def checkTradableUnderValued(self, client):
        for name in self.MonitorCoinpairValuation.keys():
            spotprice = client.ticker_price(name)
            if float(spotprice['price']) <= self.MonitorCoinpairValuation[name]:
                #check if there is enough profit room and crazy price movement & money inflow to coin
                if self.checkEnoughProfitRoom(client, spotprice) and self.checkMoneyInFlow(client, name):
                    return spotprice
        return {}


    """
    check if there is enough upside to catch and no crazy price movement
    """
    def checkEnoughProfitRoom(self, client, spotprice):
        priceChangeStat_24hr = client.ticker_24hr(spotprice['symbol'])
        priceChange = float(priceChangeStat_24hr["priceChangePercent"])
        spotprice = float(spotprice['price'])
        highPrice = float(priceChangeStat_24hr["highPrice"])
        lowPrice = float(priceChangeStat_24hr["lowPrice"])
        profitRoom = (highPrice/spotprice-1)*100
        downSideCheck = (lowPrice/spotprice-1)*100
        return (profitRoom >= self.ProfitRoom and downSideCheck >= self.DownSideCheck and abs(priceChange)<self.PriceChangeCheck)

    """
    check if buy order > sell order in 10 mins
    """
    def checkMoneyInFlow(self,client,symbol):
        recentTrades = client.agg_trades(symbol)
        buy = 0
        sell = 0
        for trade in recentTrades:
            if trade['m']:
                sell = sell + float(trade['q']) * float(trade['p'])
            else:
                buy = buy + float(trade['q']) * float(trade['p'])
        return buy>sell

    """
    TODO:
    check golden ratio check for valuation
    """
    def checkGoldenRatio(self):
        pass


