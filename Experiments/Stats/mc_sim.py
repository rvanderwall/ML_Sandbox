# seed the pseudorandom number generator
from random import seed
from random import randint

# seed random number generator
seed(42)

def get_list_of_randoms(num_count):
    for _ in range(num_count):
        value = randint(0, 1000000)
        print(value)
