import datetime
import time
import ephem
from binance import Client
import parameters
from dotenv import load_dotenv
import os

if __name__ == '__main__':

    def moon_phase_flag(today_date):
        # Full Moon -> Buy Signal
        # New Moon -> Sell Signal
        # Other -> No action

        # Calculate the dates of the upcoming major moon phases.
        next_full_moon = ephem.next_full_moon(today_date).datetime().date()
        next_new_moon = ephem.next_new_moon(today_date).datetime().date()
        
        # Calculate Flag
        if next_full_moon == today_date:
            return True
        elif next_new_moon == today_date:
            return False
        else:
            return None
        #endIf
    #endDef

    def buy_quantity(client, buy_fraction):
        busd_amount = float(client.get_asset_balance(asset = 'BUSD')['free'])
        btc_to_busd = float(client.get_symbol_ticker(symbol="BTCBUSD")['price'])
        quantity = buy_fraction * busd_amount / btc_to_busd
        return quantity
    #endDef

    def sell_quantity(client, sell_fraction):
        btc_amount = float(client.get_asset_balance(asset = 'BTC')['free'])
        quantity = sell_fraction * btc_amount
        return quantity
    #endDef

    def buy_action(client, pair_symbol, order_quantity):
        order = client.order_market_buy(symbol = pair_symbol, quantity = order_quantity)
        print(order)
        return order
    #endDef

    def sell_action(client, pair_symbol, order_quantity):
        order = client.order_market_sell(symbol = pair_symbol, quantity = order_quantity)
        print(order)
        return order
    #endDef

    def configure():
        load_dotenv()
    #endDef

    ## Grab API data from .env file.
    configure()
    api_key = os.getenv('api_key')
    api_secret = os.getenv('api_secret')
    # For the Binance Client
    ## Add  tld='us' as an argument if using binance.us instead of binance.com .
    ## Add testnet=True  as an argument if working with testnet.
    client = Client(api_key, api_secret)

    # Grab trading infromation.
    symbol = parameters.symbol
    buy_fraction = parameters.buy_fraction
    sell_fraction = parameters.sell_fraction

    while True:
        today_date = datetime.date.today()
        flag = moon_phase_flag(today_date)
        print('The flag is '+flag+'.')
        if flag is None:
            print('No action taken today.')
            try:
                print(client.get_account())
            except:
                print("Error retrieving account information. Retrying now.")
                time.sleep(60)
                continue
            # sleep for 13 hours and try again.
            time.sleep(13*60*60)
        elif flag is False:
            try:
                sell_quantity = sell_quantity(client, sell_fraction)
                sell_action(client = client, pair_symbol = symbol, order_quantity = sell_quantity)
            except:
                print('Something went wrong, retrying now.')
                continue
            btc_price = client.get_symbol_ticker(symbol="BTCBUSD")['price']
            print('Sold '+sell_quantity+' BTC at '+btc_price+' BUSD.')
            # sleep for 24 hours and try again.
            time.sleep(24*60*60)
        elif flag is True:
            try:
                buy_quantity = buy_quantity(client, buy_fraction)
                buy_action(client = client, pair_symbol = symbol, order_quantity = buy_quantity)
            except:
                print('Something went wrong, retrying now.')
                continue
            btc_price = client.get_symbol_ticker(symbol="BTCBUSD")['price']
            print('Sold '+sell_quantity+' BTC at '+btc_price+' BUSD.')
            # sleep for 24 hours and try again.
            time.sleep(24*60*60)
        #endIf
    #endWhile
#endIf