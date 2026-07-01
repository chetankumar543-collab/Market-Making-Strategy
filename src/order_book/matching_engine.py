from dataclasses import dataclass
from datetime import datetime
from collections import defaultdict
# ============================================================
# MATCHING ENGINE
# ============================================================

class MatchingEngine:

    def __init__(self):

        self.book = OrderBook()                               

        self.trade_id_counter = 1

        self.trades = []

# The book data member is an object of the class Order book.
# The trade_id_counter keeeps track of the number of trades that happened.
#  Trade is a list of all trades which have occured.

    # --------------------------------------------------------

    def process_order(self, order):

        print(
            f"\nNEW ORDER -> "                         # PRINTS THE INFO OF THE NEW ORDER.
            f"{order.side} "
            f"{order.quantity} "
            f"@ {order.price}"
        )

        if order.side == "BUY":
            self._match_buy(order)                     # ASSIGNS THE ORDER TO BUY MATCH OR SELL MATCH.

        elif order.side == "SELL":
            self._match_sell(order)

        else:
            raise ValueError("Order side must be BUY or SELL")
        
# This member function calls the matching functions _match_buy and _match_sell based on the order.

    # --------------------------------------------------------
    # BUY MATCHING
    # --------------------------------------------------------

    def _match_buy(self, incoming):

        while incoming.quantity > 0:

            best_ask = self.book.best_ask()

            if best_ask is None:                               # BREAKS IF ASKS IS EMPTY..
                break

            if incoming.price < best_ask:                      # BREAKS IF BEST ASK IS GREATER THAN THE BID.
                break

            resting_order = self.book.asks[best_ask][0]        # RESTING ORDER IS THE ORDER OF THE BEST ASK.

            fill_qty = min(                                    # FILL QTY IS THE QUANTITY OF THE TRADE.
                incoming.quantity,                              
                resting_order.quantity
            )

            trade = Trade(                                     # CREATES A TRADE OBJECT TO RECORD ALL THE INFO.
                trade_id=self.trade_id_counter,
                buy_order_id=incoming.order_id,
                sell_order_id=resting_order.order_id,
                execution_price=best_ask,
                quantity=fill_qty,
                timestamp=datetime.now()
            )

            self.trade_id_counter += 1                        # INCREMENTS TRADE COUNTER ID BY 1.

            self.trades.append(trade)                         # UPDATES THE TRADE HISTORY.
    
            print(
                f"TRADE -> "                                  # PRINTS THE TRADE OCCURED.
                f"{fill_qty} "
                f"@ {best_ask}"
            )

            incoming.quantity -= fill_qty                     # UPDATES THE LIMIT ORDER BOOK AFTER THE TRADE.
            resting_order.quantity -= fill_qty

            if resting_order.quantity == 0:

                self.book.asks[best_ask].pop(0)

                self.book.order_registry.pop(
                    resting_order.order_id,
                    None
                )

                if len(self.book.asks[best_ask]) == 0:
                    del self.book.asks[best_ask]

        if incoming.quantity > 0:

            self.book.add_order(incoming)                   
                                      
            print(
                f"RESTING BUY -> "        
                f"{incoming.quantity} "
                f"@ {incoming.price}"
            )

# _match_buy is called when a new order(bid) is made and it checks whether a trade can happen or not.
# if a trade can happen, it updates the limit order book after the trade.

    # --------------------------------------------------------
    # SELL MATCHING
    # --------------------------------------------------------

    def _match_sell(self, incoming):

        while incoming.quantity > 0:

            best_bid = self.book.best_bid()

            if best_bid is None:                          # BREAKS IF BIDS IS EMPTY.
                break                 
 
            if incoming.price > best_bid:                 # BREAKS IF BEST BID IS LESS THAN THE ORDER PRICE.
                break

            resting_order = self.book.bids[best_bid][0]   # RESTING ORDER IS THE ORDER OF THE BEST BID.

            fill_qty = min(                               # FILL QTY IS THE QUANTITY BEING TRADED.
                incoming.quantity,
                resting_order.quantity
            )

            trade = Trade(
                trade_id=self.trade_id_counter,           # CREATES A TRADE OBJECT DENOTING THE TRADE OCCURED.
                buy_order_id=resting_order.order_id,
                sell_order_id=incoming.order_id,
                execution_price=best_bid,
                quantity=fill_qty,
                timestamp=datetime.now()
            )

            self.trade_id_counter += 1                  # INCREMENTS TRADE COUNTER ID BY 1.
          
            self.trades.append(trade)                   # ADDS THIS TRADE TO THE TRADE HISTORY.

            print(
                f"TRADE -> "                            # PRINTS THE INFO OF THE TRADE OCCURED. 
                f"{fill_qty} "
                f"@ {best_bid}"
            )

            incoming.quantity -= fill_qty               # UPDATES THE LIMIT ORDER BOOK AFTER THE TRADE.
            resting_order.quantity -= fill_qty

            if resting_order.quantity == 0:

                self.book.bids[best_bid].pop(0)

                self.book.order_registry.pop(
                    resting_order.order_id,
                    None
                )

                if len(self.book.bids[best_bid]) == 0:
                    del self.book.bids[best_bid]

        if incoming.quantity > 0:

            self.book.add_order(incoming)

            print(
                f"RESTING SELL -> "
                f"{incoming.quantity} "
                f"@ {incoming.price}"
            )
# _match_sell is called when a new order(ask) is made and it checks whether a trade can happen or not.
# if a trade can happen, it updates the limit order book after the trade.

    # --------------------------------------------------------

    def cancel_order(self, order_id):

        self.book.cancel_order(order_id)

# this cancels an order.

    # --------------------------------------------------------

    def show_trades(self):

        print("\nTRADE HISTORY")
        print("=" * 60)
                                                    
        for trade in self.trades:                         # PRINTS THE TRADE HISTORY.

            print(
                f"TradeID={trade.trade_id} "
                f"BUY={trade.buy_order_id} "
                f"SELL={trade.sell_order_id} "
                f"PRICE={trade.execution_price} "
                f"QTY={trade.quantity}"
            )

        print("=" * 60)

# this prints all the trade history.

    # --------------------------------------------------------

    def show_book(self):                                  # PRINTS THE LIMIT ORDER BOOK.

        self.book.display()

# this displays the limit order book.
    # --------------------------------------------------------

    def show_top_of_book(self):                          # PRINTS THE CURRENT BEST ASK AND BID OF THE LIMIT ORDER BOOK.
 
        self.book.display_top_of_book()

# this displays the best bid and ask in the current limit order book.


