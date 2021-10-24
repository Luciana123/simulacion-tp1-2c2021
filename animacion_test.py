import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter
from matplotlib.pyplot import figure

# Colores de las celdas (escala de grises)
street_cell = 50
waiting_area = 99
pedestrian_cell = 90
car_cell = 20
traffic_light_green = 4
traffic_light_red = 2
traffic_light_off = 0

# Cantidad de celdas maxima
x_cells = 42
y_cells = 10

# Constantes de la simulacion
traffic_lights_lapse = 10

# Genero la matrix de la simulacion
def generate_map():
    return np.array([[waiting_area]+[street_cell for number in range(x_cells)]+[waiting_area] for i in range(0,y_cells)])

M = generate_map()

# Genero el semaforo
traffic_lights = np.array([[traffic_light_red],[0]])

global traffic_light_timer
traffic_light_timer=0

def update(i):
    # Codigo referente a la actualizacion del semaforo.
    global traffic_light_timer
    traffic_light_timer+=1
    if(traffic_light_timer >= traffic_lights_lapse):
        traffic_light_timer = 0
        update_traffic_lights(traffic_light_timer, traffic_lights)
    
    traffic_lights_matrix.set_array(traffic_lights)
    
    # Regenero matriz
    M = generate_map()
    
    # Vuelvo a dibujar los objetos
    move_pedestrian_to(i, 1, M)
    move_car_to(17, y_cells - i, M)

    matrix.set_array(M)

def move_pedestrian_to(x, y, M):
    update_cell(x, y, pedestrian_cell, M)

def move_car_to(x, y, M):
    if(x<x_cells and y<y_cells and x>0 and y >0):
        M[y,x] = car_cell
    if(x<x_cells and y-1<y_cells and x>0 and y >0):
        M[y-1,x] = car_cell
    if((x+1<x_cells and y<y_cells and x>0 and y >0)):
        M[y,x+1] = car_cell
    if((x+1<x_cells and y-1<y_cells and x>0 and y >0)):
        M[y-1,x+1] = car_cell

def update_cell(x, y, color, M):
    if((x<x_cells and y<y_cells and x>0 and y >0)):
        M[y,x] = color


def update_traffic_lights(traffic_light_timer, traffic_lights):        
    if(traffic_lights[0,0] == traffic_light_off):
        traffic_lights[0,0] = traffic_light_red
        traffic_lights[1,0] = traffic_light_off
    elif(traffic_lights[1,0] == traffic_light_off):
       traffic_lights[0,0] = traffic_light_off
       traffic_lights[1,0] = traffic_light_green

def get_traffic_light_color(traffic_lights):
	if(traffic_lights[1,0] == traffic_light_red):
		return traffic_light_red
	else:
		return traffic_light_green

fig, ax = plt.subplots(2, 1, figsize=(16,9), gridspec_kw={'height_ratios': [1, 3]})
matrix = ax[1].imshow(M, cmap='gray', norm=plt.Normalize(0,100))

# Minor ticks
ax[1].set_xticks(np.arange(0.5, x_cells, step=1))
ax[1].set_yticks(np.arange(0.5, y_cells, step=1))

# Gridlines based on minor ticks
ax[1].grid(color='w', linestyle='-', linewidth=2)

cmap = mpl.colors.LinearSegmentedColormap.from_list("", ["black","red","green"])

traffic_lights_matrix = ax[0].imshow(traffic_lights, cmap=cmap, norm=plt.Normalize(0,4))
ax[0].axis('off')

# Animacion
ani = FuncAnimation(fig, update, frames=200, interval=500)
plt.show()


# Guardado de la animacion en video
# probablemente se necesite correr sudo apt install ffmpeg
writervideo = FFMpegWriter(fps=2)
ani.save('animacion/simu.mp4', writer=writervideo)
plt.close()