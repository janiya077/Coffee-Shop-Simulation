#Going to make simulation for a coffee shop using python and SimPy library
import simpy
import random
import statistics

RANDOM_SEED = 42
SIM_TIME = 60
CUSTOMER_ARRIVAL_INTERVAL = (2, 5)
ORDER_TAKING_TIME = (1, 2)
COFFEE_MAKING_TIME = (5, 8)

wait_times = []
queue_lengths_order_taker = []
queue_lengths_coffee_maker = []