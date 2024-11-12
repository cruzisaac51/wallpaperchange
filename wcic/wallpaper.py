import ctypes
import os
import random
import time
import cv2
import numpy as np
from PIL import Image
from collage import create_collage


# Ruta de las carpetas de imágenes
folder1 = r"C:\Users\mayra\Pictures\morraschidas"
folder2 = r"C:\Users\mayra\Pictures\monaschinas"

# Crear carpeta si no existe
folder_path = r"C:\mis_collages"

# Definir las rutas para los collages
collage1 = os.path.join(folder_path, 'collage1.jpg')
collage2 = os.path.join(folder_path, 'collage2.jpg')
collage3 = os.path.join(folder_path, 'collage3.jpg')
collage4 = os.path.join(folder_path, 'collage4.jpg')
last_wallpaper_path = os.path.join(folder_path, 'last_wallpaper.jpg')

# Ruta donde se guardarán los collages temporales
# collage1 = os.path.join(os.getenv('TEMP'), 'collage1.jpg')
# collage2 = os.path.join(os.getenv('TEMP'), 'collage2.jpg')
# collage3 = os.path.join(os.getenv('TEMP'), 'collage3.jpg')
# collage4 = os.path.join(os.getenv('TEMP'), 'collage4.jpg')
# last_wallpaper_path = os.path.join(os.getenv('TEMP'), 'last_wallpaper.jpg')

# Variable de control para pausar/reanudar el cambio de fondo
running = True
time_remaining = 60  # Tiempo inicial en segundos

# Función para parar el ciclo
def stop_changing():
    global running
    running = False
    print("El cambio de fondo se ha detenido")

# Función para reanudar el ciclo
def resume_changing():
    global running
    running = True
    print("El cambio de fondo se ha reanudado")


# Lista de collages pre-creados
collages = [collage1, collage2, collage3, collage4]

# Función para crear los collages iniciales
def create_all_collages(label):
    create_collage(folder1, collage1, label=label)
    create_collage(folder2, collage2, label=label)
    create_collage(folder1, collage3, label=label)
    create_collage(folder2, collage4, label=label)
    
# Función para crear nuevos collages
def create_new_collages():
    # Genera nuevos collages para reemplazar los que no se usan en la transición
    create_collage(folder1, collage3, label="new")
    create_collage(folder2, collage4, label="new")

# Función para elegir dos collages aleatorios
def select_random_collages():
    selected_collages = random.sample(collages, 2)  # Elige dos collages aleatorios
    return selected_collages




# Función para la transición entre collages
def apply_fade_between_collages(collage1, collage2, duration=0.5):
    apply_fade_transition(collage1, collage2, duration)
    set_wallpaper(collage2)

def apply_fade_transition(image_path_1, image_path_2, duration=0.5):
    img1 = cv2.imread(image_path_1)
    img2 = cv2.imread(image_path_2)

    if img1 is None:
        print(f"Error: No se pudo cargar la imagen {image_path_1}")
        return
    if img2 is None:
        print(f"Error: No se pudo cargar la imagen {image_path_2}")
        return

    # Lista de direcciones posibles
    directions = ['right', 'left', 'up', 'down']
    
    # Seleccionar una dirección aleatoria
    direction = random.choice(directions)
    print(f"Dirección seleccionada: {direction}")

    # Asegurarse de que las imágenes tengan el mismo tamaño
    #if img1.shape != img2.shape:
    #   img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # Ajustar el FPS para acelerar la transición
    fps = 20  # Aumenta el FPS para una transición más fluida y rápida
    num_frames = int(duration * fps)

    # Inicializar la variable de desplazamiento
    height, width, _ = img1.shape
    
    for i in range(num_frames + 1):
        alpha = i / num_frames  # Proporción de transición
        blend = img1.copy()

        if direction == 'right':
            # Desplazar la imagen de izquierda a derecha
            shift = int(i * width / num_frames)
            blend[:, shift:] = img2[:, :width-shift]
        
        elif direction == 'left':
            # Desplazar la imagen de derecha a izquierda
            shift = int(i * width / num_frames)
            blend[:, :width-shift] = img2[:, shift:]
        
        elif direction == 'up':
            # Desplazar la imagen de abajo hacia arriba
            shift = int(i * height / num_frames)
            blend[:height-shift, :] = img2[shift:, :]
        
        elif direction == 'down':
            # Desplazar la imagen de arriba hacia abajo
            shift = int(i * height / num_frames)
            blend[shift:, :] = img2[:height-shift, :]

        # Establecer el fondo de pantalla (puedes modificar esto dependiendo de tu implementación)
        temp_frame_path = r'C:\mis_collages\temp_frame.jpg'
        cv2.imwrite(temp_frame_path, blend)
        set_wallpaper(temp_frame_path)
        
        # Esperar entre frames
        #time.sleep(1 / fps)

    # Establecer la imagen final (cuando termina la transición)
    set_wallpaper(image_path_2)

def apply_transition():
    # Elige dos collages aleatorios
    current_collage, next_collage = select_random_collages()
    
    # Aplica la transición entre los dos collages seleccionados
    apply_fade_transition(current_collage, next_collage, duration=2)
    
    # Después de la transición, crea nuevos collages para los no utilizados
    # Los collages no utilizados en la transición serán reemplazados
    create_new_collages()


# Cambiar el fondo de pantalla en Windows
def set_wallpaper(image_path, monitor_index=0):
    # Copiar el fondo actual a la ruta designada
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)


# Obtener el fondo de pantalla actual
def get_current_wallpaper():
    return last_wallpaper_path if os.path.exists(last_wallpaper_path) else collage1


# Ciclo para cambiar los collages automáticamente cada 2 minutos
def change_wallpapers_in_background(label, timer_label):
    global running, time_remaining
    while True:
        if running:
            create_all_collages(label)  # Crear todos los collages de antemano
            # Seleccionar el collage actual y uno nuevo aleatorio para la transición
            current_collage = get_current_wallpaper()  # El collage actual
            new_collages = select_random_collages()  # Seleccionamos dos collages aleatorios

            # Realizar la transición entre los collages
            apply_fade_between_collages(current_collage, new_collages[0], duration=2)  # Usamos new_collages[0] y new_collages[1] individualmente

            # Actualizar el fondo de pantalla
            set_wallpaper(new_collages[0])
            
            # Actualizar el último fondo
            global last_wallpaper_path
            last_wallpaper_path = new_collages[0]

            # Restablecer el temporizador
            time_remaining = 60

        # Temporizador para mostrar el tiempo restante
        while time_remaining > 0:
            if not running:
                # Esperar hasta que se reanude
                time.sleep(0.1)  # Pequeña espera para evitar uso excesivo de CPU
                continue
            timer_label.config(text=f"Próximo cambio en: {time_remaining} segundos")
            time.sleep(1)
            time_remaining -= 1



def change_wallpapers(label):
    current_wallpaper = get_current_wallpaper()
    create_all_collages(label)  # Crea todos los collages de antemano

    # Seleccionar un collage aleatorio de los pre-creados
    new_collages = select_random_collages()

    # Realizar la transición entre el fondo actual y el nuevo
    apply_fade_transition(current_wallpaper, new_collages[0], duration=2)  # Usa new_collages[0] y new_collages[1] como rutas individuales

    # Actualizar el fondo de pantalla
    set_wallpaper(new_collages[0], monitor_index=0)

    # Actualizar el último fondo
    global last_wallpaper_path
    last_wallpaper_path = new_collages[0]


