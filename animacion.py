import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter
from matplotlib.pyplot import figure

from model import State

global s
s = State()

# Colores de las celdas (escala de grises)
street_cell = 50
waiting_area = 99
pedestrian_cell = 90
car_cell = 20
traffic_light_green = 4
traffic_light_red = 2
traffic_light_off = 0

# Cantidad de celdas maxima
x_cells = s.crossroad_width
y_cells = s.crossroad_height

# Genero el semaforo
traffic_lights = np.array([[traffic_light_red],[0]])

def update(i):
    traffic_lights_matrix.set_array(s.semaforo.matrix())
    s.iterar()
    matrix.set_array(s.matrix().transpose())

    ped = "Pedestrians in simulation: {}".format(len(s.pedestrians))
    cars = "Cars in simulation: {}".format(len(s.cars))
    conflict1 = "Pedestrian Pedestrian conflict: {}".format(s.conflicto_peatones_misma_pos)
    conflict2 = "Pedestrian Car conflict: {}".format(s.conflicto_auto_espera_peaton)
    red_light_time = "Red light time: {}".format(s.semaforo_tiempo_rojo)
    green_light_time = "Green light time: {}".format(s.semaforo_tiempo_verde)
    
    stats = [ped, cars, conflict1, red_light_time, green_light_time]
    label_stats.set_text('\n'.join(stats))


fig, ax = plt.subplots(2, 1, figsize=(16,9), gridspec_kw={'height_ratios': [1, 3]})

matrix = ax[1].imshow(s.matrix().transpose(), cmap='gray', norm=plt.Normalize(0,100))

# Minor ticks
ax[1].set_xticks(np.arange(0.5, x_cells, step=1))
ax[1].set_yticks(np.arange(0.5, y_cells, step=1))

# Gridlines based on minor ticks
ax[1].grid(color='w', linestyle='-', linewidth=2)

cmap = mpl.colors.LinearSegmentedColormap.from_list("", ["black","red","green"])

traffic_lights_matrix = ax[0].imshow(traffic_lights, cmap=cmap, norm=plt.Normalize(0,4))
ax[0].axis('off')
ax[0].set_title('Pedestrian light')
ax[1].set_title('Crosswalk')

ped = "Pedestrians in simulation: {}".format(len(s.pedestrians))
stats = [ped]

label_stats = ax[0].text(0.1, 0.7, '\n'.join(stats), fontsize=14, transform=plt.gcf().transFigure)

# Animacion
ani = FuncAnimation(fig, update, frames=200000000, interval=500)
plt.show()

# Graficar la cantidad de peatones.
# Graficar info de la simulación.

# Guardado de la animacion en video
# probablemente se necesite correr sudo apt install ffmpeg
writervideo = FFMpegWriter(fps=2)
ani.save('animacion/simu.mp4', writer=writervideo)
plt.close()