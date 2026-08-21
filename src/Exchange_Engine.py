from enum import IntEnum
from collections import deque
from sortedcontainers import SortedDict

class Side(IntEnum):
  BID = 0
  ASK = 1

class OrderType(IntEnum):
  GoodTilCancel = 0
  FillAndKIll = 1

#Creates the Order class for the queue data structure
class Order:
  def __init__(self, time_stamp: float, price: int, quantity: int, side: Side, id: int = 0, order_type: OrderType = OrderType.GoodTilCancel):
    self.time_stamp = time_stamp
    self.price = price
    self.quantity = quantity
    self.id = id
    self.order_type = order_type
    self.side = side
    self.global_id = 0

class OrderBook:
  def __init__(self):
    self.bid_stream = SortedDict()
    self.ask_stream = SortedDict()
    self.id_tracker = {}

  def add_to_queue(self, order: Order) -> int:
    order.id = self.global_id
    self.global_id += 1
    """Adds to bid_stream or ask_stream based on the order's side argument

      Args:
        order: the order we want to add

      Return:
        returns the order id of that order
    """
    if order.side == Side.BID:
      if (-1 * order.price) in self.bid_stream:
        self.bid_stream[-1 * order.price].append(order)
      else:
        self.bid_stream[-1 * order.price] = deque()
        self.bid_stream[-1 * order.price].append(order)
    else:
      if order in self.ask_stream:
        self.ask_stream[order.price].append(order)
      else:
        self.ask_stream[order.price] = deque()
        self.ask_stream[order.price].append(order)
    self.id_tracker[order.id] = order

    return self.global_id

  # A helper function to help the modify_order function
  # Soft cancels orders by setting order quantity to 0 when prices are different
  def _soft_cancel(self, order: Order) -> None:
    order.quantity = 0

  def modify_order(self, id: int, order: Order) -> int:
    """Modifies orders within a bid or ask stream

    Args:
      id: the order we want to modify
      order: the details of the new order we want

    Return:
      returns the order id of the order (either its new id, or its old id)
    """
    current_order = self.id_tracker[id]
    if current_order.price != order.price or order.quantity > current_order.quantity:
      self._soft_cancel(current_order)
      self.global_id += 1
      order.id = self.global_id
      self.add_to_queue(order)
      return self.global_id
    elif order.quantity < current_order.quantity:
      current_order.quantity = order.quantity
      return current_order.id