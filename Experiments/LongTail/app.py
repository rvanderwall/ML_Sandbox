import random
from math import sqrt, ceil, floor
from numpy.random import default_rng
import matplotlib.pyplot as plt

"""https://constructionphysics.substack.com/p/why-its-hard-to-innovate-in-construction"""

"""Consider a worker with just one job, driving nails with a nail gun.
Assume the time it takes to drive a nail is normally distributed [0], with a fairly narrow spread
 - each nail takes an average time of one second, with a standard deviation of 0.5 seconds.
But every 100 nails, he needs to reload the nail gun, an action which is also normally-distributed
but has a mean of 10 seconds.
Every 500 nails, he needs to go to his truck and get another box of nails,
which has a mean time of 60 seconds.
And every 5000 nails, he has to drive to the store to get more,
which has a mean time of 10 minutes.
"""

class NailGunSimulation:
    def __init__(self):
        self._verbose = False
        self.gun_capacity = 100         # Gun holds 100 nails
        self.nails_in_box = 100         # One box will refill the gun
        self.site_box_capacity = 5      # We have 5 boxes on site, with us
        self.truck_box_capacity = 50    # the truck holds 50 boxes

        self.nails_in_gun = self.gun_capacity
        self.boxes_on_site = self.site_box_capacity
        self.boxes_in_truck = self.truck_box_capacity

        self.rng = default_rng()

    def restart_simulation(self):
        self.nails_in_gun = self.gun_capacity
        self.boxes_on_site = self.site_box_capacity
        self.boxes_in_truck = self.truck_box_capacity

    def simulate(self, n):
        self.restart_simulation()
        t = 0.0
        for i in range(n):
            t += self.drive_nail_time()
        return t, t / n

    def drive_nail_time(self):
        if self.nails_in_gun > 0:
            jam_time = self.jam_time()
            if jam_time > 0:
                # This nail jammed, unjam and try again
                return jam_time + self.drive_nail_time()
            else:
                t = self.activity_time(mu=1.0)
                self.nails_in_gun -= 1
                return t
        else:
            t = self.reload_gun_time()
            t += self.drive_nail_time()
            return t

    def jam_time(self):
        j = random.randint(1, 100)
        if j > 101:
            t = self.activity_time(mu=30.0)
            return t
        return 0

    def reload_gun_time(self):
        if self.boxes_on_site >= 1:
            t = self.activity_time(mu=10.0)
            self.boxes_on_site -= 1
            self.nails_in_gun = self.nails_in_box
            self._log(f"Reloading took {t} seconds")
            return t
        else:
            t = self.get_nails_from_truck()
            t += self.reload_gun_time()
            self._log(f"Getting nails and reloading took {t} seconds")
            return t

    def get_nails_from_truck(self):
        if self.boxes_in_truck >= self.site_box_capacity:
            t = self.activity_time(mu=60.0)
            self.boxes_in_truck -= self.site_box_capacity
            self.boxes_on_site = self.site_box_capacity
            self._log(f"Getting nails from truck took {t} seconds")
            return t
        else:
            t = self.buy_more_nails()
            t += self.get_nails_from_truck()
            self._log(f"Buying and getting nails from truck took {t} seconds")
            return t

    def buy_more_nails(self):
        t = self.activity_time(mu=10.0 * 60)
        self.boxes_in_truck = self.truck_box_capacity
        self._log(f"Buying more nails took {t} seconds")
        return t

    def activity_time(self, mu):
        # An activity typically takes mu seconds but
        # things can go wrong and it may take more
        # The activity really can't go faster than mu
        # but certainly can go slower
        sigma = sqrt(mu / 20)
        return mu + abs(sigma * self.rng.normal())

    def _log(self, msg):
        if self._verbose:
            print(msg)

    def expected_time(self, N):
        if N == 0:
            reloads = 0
        else:
            reloads = floor((N - 1) / self.gun_capacity)

        if reloads == 0:
            trips_to_truck = 0
        else:
            trips_to_truck = floor((reloads - 1) / self.site_box_capacity)

        if trips_to_truck == 0:
            trips_to_store = 0
        else:
            # Each trip removes a case, not a single box
            num_cases = self.truck_box_capacity / self.site_box_capacity
            trips_to_store = floor((trips_to_truck - 1) / num_cases)

        t = N * 1 + reloads * 10 + trips_to_truck * 60 + trips_to_store * 600
        print(f"N:{N}  reloads:{reloads}  trips to truck:{trips_to_truck}, trips to store:{trips_to_store}")
        return t


def run_tests():
    tests = [(0, 0),
             (1, 1),
             (100, 100),
             (101, 111),
             (600, 650),
             (601, 721),
             (1000, 1150),
             (1100, 1260),
             (1101, 1331),
             (5000, 6030),  # 5000 nails + 49 reloads + 9 trips to truck
             (5600, 6750),   # 5600 nails + 55 reloads + 10 trips to truck
             (5601, 7421)    # 5601 nails + 56 reloads + 11 trips to truck + 1 store trip
             ]
    ngs = NailGunSimulation()
    for t in tests:
        N, expected = t
        actual = ngs.expected_time(N)
        if expected == actual:
            print(f"OK:   expected: {expected}, actual:{actual}")
        else:
            print(f"FAIL: expected: {expected}, actual:{actual}")


def main_sim():
    ngs = NailGunSimulation()
    num_sims = 100
    nails_per_sim = 20000
    results = []
    print(f"Expected time: {ngs.expected_time(nails_per_sim)}")
    for s in range(num_sims):
        print(f"Simulation round {s}")
        t, t_ave = ngs.simulate(nails_per_sim)
        results.append(t)

    plt.hist(results, bins=100)
    plt.show()


if __name__ == "__main__":
    print("Long tail")
    # run_tests()
    main_sim()
