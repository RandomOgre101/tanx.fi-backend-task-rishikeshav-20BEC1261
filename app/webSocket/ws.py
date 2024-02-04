import websocket, json, threading
from ..controllers.rabbitmq import enqueue_email_task


# OOP Based solution to run threads and continuously check prices in real time with the Binance websocket
class PriceChecker:
    def __init__(self, data, email):
        self.data = data
        self.email = email

    def on_message(self, ws, message):
        json_msg = json.loads(message)
        symbol = json_msg['s']
        price = json_msg['p']


        for symbol_data in self.data:
            if symbol_data[0].upper()+'USDT' == symbol and float(symbol_data[1]) == float(price):
                enqueue_email_task(
                    {
                        "to_address": self.email,
                        "subject": f"{symbol} HAS REACHED ${price}",
                        "message": f"Alert Activated: {symbol} HAS REACHED ${price}"
                        }
                    )

    def on_close(self, ws):
        print("Closed Connection")

    # Function so as to run multithreading
    def run_websocket(self, url):
        ws = websocket.WebSocketApp(url=url, on_message=self.on_message, on_close=self.on_close)
        ws.run_forever()


def run_threads(data, email):
    price_checker = PriceChecker(data, email)

    symbols = [tup[0] for tup in data]

    # Creating socket URLs using the crypto names that are passed in through data
    sockets = [f"wss://stream.binance.com:9443/ws/{symbol+'usdt'}@aggTrade" for symbol in symbols]

    threads = [threading.Thread(target=price_checker.run_websocket, args=(socket,)) for socket in sockets]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()





