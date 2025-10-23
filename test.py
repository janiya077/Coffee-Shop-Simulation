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

def customer(env, name, order_taker, coffee_maker):
    arrival_time = env.now
    print(f"{name} arrives at {arrival_time:.2f}")

    with order_taker.request() as req:
        yield req
        queue_lengths_order_taker.append(len(order_taker.queue))
        yield env.timeout(random.uniform(*ORDER_TAKING_TIME))
        print(f"{name}'s order taken at {env.now:.2f}")

    with coffee_maker.request() as req:
        yield req
        queue_lengths_coffee_maker.append(len(coffee_maker.queue))
        yield env.timeout(random.uniform(*COFFEE_MAKING_TIME))
        print(f"{name}'s coffee ready at {env.now:.2f}")

    total_time = env.now - arrival_time
    wait_times.append(total_time)
    print(f"{name} leaves at {env.now:.2f} (total time: {total_time:.2f} min)")

def customer_generator(env, order_taker, coffee_maker):
    i = 0
    while True:
        yield env.timeout(random.uniform(*CUSTOMER_ARRIVAL_INTERVAL))
        i += 1
        env.process(customer(env, f"Customer {i}", order_taker, coffee_maker))

def run_simulation():
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    order_taker = simpy.Resource(env, capacity=2)
    coffee_maker = simpy.Resource(env, capacity=2)
    env.process(customer_generator(env, order_taker, coffee_maker))
    env.run(until=SIM_TIME)

    avg_wait = statistics.mean(wait_times)
    print("\n=== Simulation Results ===")
    print(f"Average total time per customer: {avg_wait:.2f} minutes")
    print(f"Max queue length (Order Taker): {max(queue_lengths_order_taker, default=0)}")
    print(f"Max queue length (Coffee Maker): {max(queue_lengths_coffee_maker, default=0)}")
    print(f"Total customers served: {len(wait_times)}")

if __name__ == "__main__":
    run_simulation()
