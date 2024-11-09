import ctypes
import os
import random
import time
from PIL import Image
from collage import create_collage


# Ruta de las carpetas de imágenes
folder1 = r"C:\Users\mayra\Pictures\morraschidas"
folder2 = r"C:\Users\mayra\Pictures\monaschinas"
# Ruta donde se guardarán los collages temporales
collage1 = os.path.join(os.getenv('TEMP'), 'collage1.jpg')
collage2 = os.path.join(os.getenv('TEMP'), 'collage2.jpg')

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


# Cambiar el fondo de pantalla en Windows
def set_wallpaper(image_path, monitor_index=0):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)

# Ciclo para cambiar los collages automáticamente cada 2 minutos
def change_wallpapers_in_background(label,timer_label):
    global running, time_remaining
    while True:
        if running:
            # Crear collages para ambos monitores
            create_collage(folder1, collage1, label=label)
            create_collage(folder2, collage2, label=label)

            # Cambiar fondo de pantalla (se asume que hay dos monitores)
            collage = random.choice([collage1, collage2])
            set_wallpaper(collage, monitor_index=0)
            #set_wallpaper(collage2, monitor_index=1)

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
    create_collage(folder1, collage1, label=label)
    create_collage(folder2, collage2, label=label)
    collage = random.choice([collage1, collage2])
    set_wallpaper(collage, monitor_index=0)
