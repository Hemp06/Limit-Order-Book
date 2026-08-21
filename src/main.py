import numpy as np
from random import randint, lognormvariate, choice
from Exchange_Engine import Side, Order, OrderBook
from time import time_ns

def calculate_quantity(price, budget) -> int:
  mu = log(budget/price)
  sigma = 0.5
  quantity = lognormvariate(mu, sigma)

  return max(1, round(quantity))

def main():
  order_book = OrderBook()
  trials = 10000
  lambda_ = randint(400, 600)
  rng = np.random.default_rng(42)
  for i in range(trials):
    k = rng.poisson(lam = lambda_)
    #Gives the actual market maker bot an arbitrary position in line (Currently a placeholder)
    market_maker_bot_position = randint(0, k)
    for j in range(k):
      budget = randint(200, 400)
      price = randint(90, 110)
      order = Order(time_ns(), price, calculate_quantity(price, budget), choice(Side.BID, Side.ASK))
      order_book.add_to_queue(order)