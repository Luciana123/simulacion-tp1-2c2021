import numpy as np


class Poisson:
    def __init__(self, arrival_rate, t_limit=3600, seed=0):
        self.seed = seed
        self.t_limit = t_limit
        self.arrival_rate = arrival_rate
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
        num = self.seed
        aux = []
        while t_acum <= self.t_limit:
            num = RandomNumber.next(num)
            z = self.__exponential(num)
            t_acum += z
            aux.append(t_acum)

        return aux

    def __exponential(self, num):
        return - np.log(num / RandomNumber.MODULE) / self.arrival_rate

class CarArrival(Poisson):
    def __init__(self, arrival_rate, seed=0):
        super().__init__(arrival_rate, seed)

    def next(self, offset=1):
        offset
        # TODO: complete the following line.
        # return [Car(pos, velocity) for x in super()]

class PedestrianArrival(Poisson):
    def __init__(self, arrival_rate, seed=0):
        super().__init__(arrival_rate, seed)

    def next(self, offset=1):
        offset
        # TODO: complete the following line.
        # return [Pedestrian(pos, velocity) for x in super()]

class RandomNumber:
    MODULE = 4294967296
    MULTIPLIER = 1013904223
    INCREMENT = 1664525

    @classmethod
    def next(cls, n):
        return (RandomNumber.MULTIPLIER * n + RandomNumber.INCREMENT) % RandomNumber.MODULE