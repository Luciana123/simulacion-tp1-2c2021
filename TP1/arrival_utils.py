import numpy as np
from model import Car, Pedestrian, Position


class Poisson:
    def __init__(self, arrival_rate, t_limit=3600, seed=0):
        self.seed = seed
        self.t_limit = t_limit
        self.arrival_rate = arrival_rate
        self.random = RandomNumber(seed)
        self.arrivals = self.__sim()
        self.intervals = self.__interval_split()
        self.last_offset = -1

    def next(self, offset=1):
        """Get next instances per second.
        Example: first next() should return the arrivals between [0, 0 + offset)."""
        self.last_offset += offset
        if self.last_offset == len(self.arrivals):
            raise AttributeError

        return self.intervals[self.last_offset]

    def reset(self):
        self.last_offset = -1

    def __interval_split(self, offset=1):
        acc = offset
        bucket = []
        intervals = []
        for x in self.arrivals:
            if x < acc:
                bucket.append(x)
            else:
                intervals.append(bucket)
                bucket = [x]
                acc += offset
                while x > acc:
                    acc += offset
                    intervals.append([])

        # last bucket
        intervals.append(bucket)

        return intervals

    def __sim(self):
        t_acum = 0
        aux = []
        while t_acum <= self.t_limit:
            z = self.__exponential(self.random.get())
            t_acum += z
            aux.append(t_acum)

        return aux

    def __exponential(self, n):
        return - np.log(1-n) / self.arrival_rate


class ObjectArrival(Poisson):
    def __init__(self, arrival_rate, t_limit, seed):
        super().__init__(arrival_rate, t_limit, seed)
        self.velocity_calculator = VelocityCalculator()

    def map_object(self, x):
        raise NotImplementedError("Please Implement this method")

    def next(self, offset=1):
        return list(map(lambda x: self.map_object(x), super().next()))


class CarArrival(ObjectArrival):
    CAR_VELOCITY = 10

    def __init__(self, arrival_rate, t_limit=3600, seed=0):
        super().__init__(arrival_rate, t_limit, seed)

    def map_object(self, x):
        return Car(Position(1, 1), CarArrival.CAR_VELOCITY)


class PedestrianArrival(ObjectArrival):
    def __init__(self, arrival_rate, t_limit=3600, seed=0):
        super().__init__(arrival_rate, t_limit, seed)

    def map_object(self, x):
        return Pedestrian(Position(-1, -1), self.velocity_calculator.next(self.random.get()))


class RandomNumber:
    MODULE = 4294967296
    MULTIPLIER = 1013904223
    INCREMENT = 1664525

    def __init__(self, seed=1):
        self.seed = seed

    def get(self):
        return self.__next() / RandomNumber.MODULE

    def __next(self):
        self.seed = (RandomNumber.MULTIPLIER * self.seed + RandomNumber.INCREMENT) % RandomNumber.MODULE
        return self.seed

class VelocityCalculator:
    VALUES = [2, 3, 4, 5, 6]
    P = [2730 / 10000, 5200 / 10000, 1370 / 10000, 480 / 10000, 220 / 10000]

    def __init__(self):
        p = VelocityCalculator.P
        self.proba_vector = [
            0, p[0], p[0] + p[1], p[0] + p[1] + p[2], p[0] + p[1] + p[2] + p[3], p[0] + p[1] + p[2] + p[3] + p[4]
        ]

    def next(self, n):
        label_idx = 0
        for idx in range(0, len(self.proba_vector) - 1):
            if (n >= self.proba_vector[idx]) and (n <= self.proba_vector[idx + 1]):
                label_idx = idx
        return VelocityCalculator.VALUES[label_idx]
