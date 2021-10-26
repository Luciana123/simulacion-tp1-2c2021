import numpy as np

global MAX_DISTANCE
MAX_DISTANCE = 10000

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def x(self):
        return self.x
    
    def y(self):
        return self.y
    
    def is_negative(self):
        return (self.x < 0) | (self.y < 0)
    
    def __eq__(self, other):
        return (self.x == other.x) & (self.y == other.y)
    
    def __hash__(self):
        return hash(tuple([self.x, self.y]))

class Pedestrian:
    def __init__(self, position, velocity):
        self.position = position
        self.direction = 'right'
        self.velocity = velocity
        self.next_position = None
       
    def set_in_matrix(self, matrix):
        matrix.put(self.position.x, self.position.y, self)
            
    
    # Establece su posicion y direccion inicial
    def locate(self):
        # cambiar por posiciones al azar
        self.position = Position(0,0)
        if (np.random.rand() < 0.5):
            self.direction = 'right'
        else:
            self.direction = 'left'      
            
            
    def avanzar(self, matrix, semaforo):
        if semaforo.is_red():
            if self.position.is_negative(): # no empieza a cruzar
                return
        
            # Semaforo rojo y estaba cruzando, avanza a maxima velocidad
            self.velocity = 6
            self.next_position = Position(self.position.x + 6, self.position.y)
            return self.next_position
        
        else:  # Semaforo verde
            if self.position.is_negative(): # no empieza a cruzar
                self.locate()
                
            self.move_forward(matrix) 
            if not self.next_position:  # Posicion ocupada
                self.lane_change(matrix)
            return self.next_position
        
        
    def continuar(self, matrix):
        matrix.put(self.position.x, self.position.y, None)
        self.position = self.next_position
        self.next_position = None
        matrix.put(self.position.x, self.position.y, self)

        
        
    def move_forward(self, matrix):
        if self.direction == 'right':
            direction = 1
        elif self.direction == 'left':
            direction = -1
        d = matrix.distance_to_next_object(self.position.x, self.position.y, direction)
        
        if d == 0:  # la siguiene posicion esta ocupada
            return None

        self.next_position = Position(self.position.x + self.velocity * direction, self.position.y)
        self.update_velocity(direction, matrix)
        
        
    def update_velocity(self, direction, matrix):
        d = matrix.distance_to_next_object(self.next_position.x, self.position.y, direction)
        self.velocity = min(d, self.velocity)
        

    def lane_change(self, matrix):
        if self.direction == 'right':
            direction = 1
        elif self.direction == 'left':
            direction = -1

        d = matrix.distance_to_next_object(self.position.x, self.position.y, direction)
        if d != 0: 
            return
        if self.can_turn_right(matrix) & self.can_turn_left(matrix):
            if (np.random.rand() < 0.5):
                self.turn_right()
            else:
                self.turn_left()
        elif self.can_turn_right(matrix):
            self.turn_right()
        elif self.can_turn_left(matrix):
            self.turn_left()
            
    
    def turn_right(self):
        self.next_position = Position(self.position.x, self.position.y + 1)
    
    def turn_left(self):
        self.next_position = Position(self.position.x, self.position.y - 1)
        
                                      
    def can_turn_right(self, matrix):
        return (matrix.is_empty(self.position.x, self.position.y + 1)) & \
               (self.velocity_higher_than_last(self.position.y + 1, matrix)) & \
               (self.velocity_less_than_next(self.position.y + 1, matrix))
                                      
    def can_turn_left(self, matrix):
        return (matrix.is_empty(self.position.x, self.position.y - 1)) & \
               (self.velocity_higher_than_last(self.position.y - 1, matrix)) & \
               (self.velocity_less_than_next(self.position.y - 1, matrix))
        
    def velocity_higher_than_last(self, position_y, matrix):
        if self.direction == 'right':
            direction = -1
        elif self.direction == 'left':
            direction = 1
        last_pedestrian = matrix.get_next_object(self.position.x, position_y, direction)
        
        if not last_pedestrian:  # nadia camina atras
            return True
        return self.velocity > last_pedestrian.velocity    
                
    def velocity_less_than_next(self, position_y, matrix):
        if self.direction == 'right':
            direction = 1
        elif self.direction == 'left':
            direction = -1
        distance = matrix.distance_to_next_object(self.position.x, position_y, direction)
        return self.velocity < distance
 
    def is_pedestrian(self):
        return True
        
    def __str__(self):
        return 'Pos {0} Vel {1}'.format(self.position, self.velocity)

class Car:
    def __init__(self, position, velocity):
        self.size_x = 6
        self.size_y = 5
        self.velocity = 10 # 5 m/s * 2 cell/m
        self.initial_pos = position
        self.positions = []
        for i in range(0, self.size_x):
            self.positions.append([])
            for j in range(0, self.size_y):
                self.positions[i].append(Position(position.x + i, position.y + j))
        
    def set_in_matrix(self, matrix):
        for i in range(0, self.size_x):
            for j in range(0, self.size_y):
                matrix.put(self.positions[i][j].x, self.positions[i][j].y, self)
                
    def del_in_matrix(self, matrix):
        for i in range(0, self.size_x):
            for j in range(0, self.size_y):
                matrix.put(self.positions[i][j].x, self.positions[i][j].y, None)
        
        
    def avanzar(self, matrix, semaforo):
        if semaforo.is_red(): # cambiar
            return 0
        
        conflict = 0
        if not matrix.pedestrian_on_crosswalk():
            distance = self.velocity
        else:
            distance = min(self.distance_to_pedestrian(matrix), self.velocity)
            if distance < self.velocity:
                conflict = 1
            
        print(distance)
        self.move(distance, matrix)
        return conflict
        
        
    def distance_to_pedestrian(self, matrix):
        distance = MAX_DISTANCE
        # Recorro todas las celdas del camino del auto para encontrar la distancia al primer peaton
        for j in range(0, self.size_x):  
            pos_x = self.initial_pos.x + j
            pos_y = self.initial_pos.y + self.size_y - 1
            d = matrix.distance_car_to_pedestrian(pos_x, pos_y)
            if d < distance:
                distance = d
        return distance
            
        
    def move(self, distance, matrix):
        self.initial_pos = Position(self.initial_pos.x, self.initial_pos.y + distance)
        self.del_in_matrix(matrix)
        for i in range(0, self.size_x):
            for j in range(0, self.size_y):
                self.positions[i][j] = Position(self.positions[i][j].x, self.positions[i][j].y + distance)
        self.set_in_matrix(matrix)
        
        
    def is_pedestrian(self):
        return False
        
        
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
    
    def iterate(self):
        ps = []
        cs = []
        for i in range(1, np.random.randint(1,100)):
            rand_x = np.random.randint(self.crossroad_width)
            rand_y = np.random.randint(self.crossroad_height)
            ps.append(Pedestrian(Position(rand_x, rand_y), 1))

        for i in range(1, np.random.randint(1,100)):
            rand_x = np.random.randint(self.crossroad_width)
            rand_y = np.random.randint(self.crossroad_height)
            cs.append(Car(Position(rand_x, rand_y), 1))

        self.pedestrians = ps
        self.cars = cs

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