from dataclasses import dataclass
from datetime import datetime
from collections import defaultdict
# ============================================================
# ORDER BOOK
# ============================================================

class OrderBook:

    def __init__(self):

        # price -> list[Order]
        self.bids = defaultdict(list)
        self.asks = defaultdict(list)

        # order_id -> Order
        self.order_registry = {}

# These are the data members of the class Order book.
# bids and ask map prices to the list of Orders and order_registry maps the order_id to order.

    # --------------------------------------------------------

    def add_order(self, order):

        self.order_registry[order.order_id] = order  # STORES THE ORDER IN ORDER REGISTERY.

        if order.side == "BUY":
            self.bids[order.price].append(order)     # ADDS THE ORDER TO THE BIDS LIST AT THE GIVEN PRICE TAG IF IT IS A BUY ORDER.

        else:
            self.asks[order.price].append(order)     # ADDS THE ORDER TO THE ASKS LIST AT THE GIVEN PRICE TAG IF IT IS A SELL ORDER.

# This member function adds the order at the end of list in bids/asks list.
# If there is no price equal to the order.price it creates a new list for that price.

    # --------------------------------------------------------

    def remove_order(self, order):

        side_book = self.bids if order.side == "BUY" else self.asks

        if order.price not in side_book:
            return                                   

        level = side_book[order.price]

        if order in level:
            level.remove(order)

        if len(level) == 0:                              # REMOVES THE LIST IF THERE IS NO ORDER AT THAT PRICE.
            del side_book[order.price]

        self.order_registry.pop(order.order_id, None)    # REMOVES ORDER FROM THE ORDER REGISTERY.

# This member function removes an order from the order book.

    # --------------------------------------------------------

    def cancel_order(self, order_id):

        order = self.order_registry.get(order_id)         

        if not order:
            print(f"Order {order_id} not found")
            return False

        self.remove_order(order)

        print(f"Cancelled Order {order_id}")

        return True
    
# This member function is used to cancel an order.

    # --------------------------------------------------------

    def best_bid(self):
                                         
        if not self.bids:
            return None

        return max(self.bids.keys())
    
# This member function returns the maximum bid in the bid list.

    # --------------------------------------------------------

    def best_ask(self):

        if not self.asks:
            return None

        return min(self.asks.keys())
    
# This member function returns the minimum ask in the ask list.

    # --------------------------------------------------------

    def display(self):

        print("\n")
        print("=" * 40)
        print("ASK SIDE")

        for price in sorted(self.asks.keys(), reverse=True):   # PRINTS ASKS IN INCREASING ORDER.

            total_qty = sum(
                order.quantity
                for order in self.asks[price]           
            )

            print(f"{price:>8} | {total_qty}")

        print("-" * 40)

        for price in sorted(self.bids.keys(), reverse=True):   # PRINTS BIDS IN DECREASING ORDER.

            total_qty = sum(
                order.quantity
                for order in self.bids[price]
            )

            print(f"{price:>8} | {total_qty}")

        print("BID SIDE")
        print("=" * 40)

        print()

# this member function prints the limit order book.

    # --------------------------------------------------------

    def display_top_of_book(self):

        print("\nTOP OF BOOK")                                

        print("Best Bid :", self.best_bid())                     # PRINTS BEST BID.
        print("Best Ask :", self.best_ask())                     # PRINTS BEST ASK.

        if self.best_bid() is not None and self.best_ask() is not None:

            spread = self.best_ask() - self.best_bid()

            print("Spread   :", spread)                          # PRINTS SPREAD.

        print()

# This member function prints the best bid, the best ask and also spread.
