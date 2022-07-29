# Moon Phase Trading Algorithm
## version 1.0

Naive day trading is a fast way to lose money, but it's a fun way to test out different strategies and learn from them. A lot of day traders use technical analysis to inform their trades, however, it holds about as much weight as astrology does. 

This inspired me to make a very simple algorithm based on the lunar (moon) phases, trading BTCUSD on [binance.com](https://binance.com/). 

The trade logic is to buy on a full moon, sell on a new moon, and hold in-between. The fraction of your BTC that you buy / sell is defined in `parameters.py`. They are both currently set to 0.3 . The asset pair that you trade is also defined in `BTCBUSD`. You can change both at your leisure, but will need to change some labels in `main.py`.

The trading logic can be improved quite easily, just remember to treat this as a finite state machine.

This project was inspired by [ibeandyy](https://github.com/ibeandyy/lunar_binance_bot).