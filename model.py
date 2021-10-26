import numpy as np

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return 'X {0} Y {1}'.format(self.x, self.y)

class Pedestrian:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
    def __str__(self):
        return 'Pos {0} Vel {1}'.format(self.position, self.velocity)

class Car:
    
    size_x = 6
    size_y = 5
    
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        
    def __str__(self):
        return 'Pos {0} Vel {1}'.format(self.position, self.velocity)

class State:
    
    street_cell = 50
    waiting_area = 99
    pedestrian_cell = 90
    car_cell = 20
    
    def __init__(self):
        self.cars = []
        self.pedestrians = []
        self.crossroad_width = 42
        self.crossroad_height = 10
        
    def valid_pos(self, x, y, width, height):
        if(x >= 0 and x < width and y >= 0 and y < height):
            return True
        return False
    
    def iterate():
        rand_x = np.random.randint(self.crossroad_width)
        rand_y = np.random.randint(self.crossroad_height)
        p1 = Pedestrian(rand_x, rand_y, 1)
        rand_x = np.random.randint(self.crossroad_width)
        rand_y = np.random.randint(self.crossroad_height)
        p2 = Pedestrian(rand_x, rand_y, 1)
        rand_x = np.random.randint(self.crossroad_width)
        rand_y = np.random.randint(self.crossroad_height)
        c1 = Car(rand_x, rand_y, 1)
        self.pedestrians = [p1, p2]
        self.cars = [c1]

    def matrix(self):
        
        w = self.crossroad_width
        h = self.crossroad_height
        
        matrix = np.array([[self.street_cell for number in range(h) ] for i in range(w)])
                
        for pedestrian in self.pedestrians:
            if(self.valid_pos(pedestrian.position.x, pedestrian.position.y, w, h)):
                matrix[pedestrian.position.x, pedestrian.position.y] = self.pedestrian_cell
        for car in self.cars:
            for i in range (0, car.size_x):
                for j in range (0, car.size_y):
                    if(self.valid_pos(car.position.x+i, car.position.y+j, w, h)):
                        matrix[car.position.x+i, car.position.y+j] = self.car_cell
        return matrix