from alpaca.data.live.crypto import CryptoDataStream
from config import API_KEY, API_SECRET
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest, MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce, AssetClass
import datetime
import random
import time
import json

#TRADER_API_KEY = 'PK4AZDP245Z3OQ8MMAPB'
#TRADER_SECRET_KEY = '9D3rGxqT2FZkrR4JKxp7YAJqcp2EvGdcp8XNb6VC'

class Trade:
    """ THis Class encapsulates all user Trade logic
    """
    
    trading_client = TradingClient(
                    api_key=API_KEY,
                    secret_key=API_SECRET,
                    paper=True,
                )
    search_params = GetAssetsRequest(asset_class=AssetClass.CRYPTO)

    assets = trading_client.get_all_assets(search_params)
    
    def __init__(self) -> None:
        pass


    def place_order(self, symbol: str, quantity: int, stop_loss: int, take_profit: int, Condition: str, time_frame: str):
        """ This  Method handles user trades Buy/Sell
            Example symbol = "BTC/USD", quantity = 0.023, Condition = client_func["BUY"]
        """
        
        user_trade = {
            "symbol": symbol,
            "quantity": quantity,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "condition": Condition,
            "time_frame": time_frame
        }
        return user_trade



#trade = Trade()

#market_order = trade.place_order("BTC/USD", 0.4, "BUY")
#print(market_order)


#assets = Trade.assets
#print("Saving assets")
#print(f"{assets}")
#a_dict = {}
#for asset in assets:
#    a_dict[f"{asset.id}"] = { asset.symbol: asset.price_increment}
    
#json_string = json.dumps()

#with open('assets.json', 'w') as file:
#    json.dump(a_dict, file, indent=2)



# keys are required for live data
#crypto_stream = CryptoDataStream(API_KEY, API_SECRET)

#wss_client = CryptoDataStream(TRADER_API_KEY, TRADER_SECRET_KEY)

# async handler
#async def quote_data_handler(data):
    # quote data will arrive here
#    print(data)

#wss_client.subscribe_quotes(quote_data_handler, "SPY")

#wss_client.run()

#accounts = get_all_accounts()
#rint(accounts)
#achrelationship = create_trading_account("Og@gmail.com", "OGT", "08025415081")
#fund_account(achrelationship)
#print(f"Account id is {account.id}\n Account name is {account.identity.given_name} \n Account Number is {account.account_number}\n")


