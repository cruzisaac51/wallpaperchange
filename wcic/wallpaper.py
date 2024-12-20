import ctypes
import os
import random
import time
import cv2
import shutil
import numpy as np
import varkeys
from PIL import Image
from collage import create_collage


# Definir las rutas para los collages
collage1 = os.path.join(varkeys.folder_path, 'collage1.jpg')
collage2 = os.path.join(varkeys.folder_path, 'collage2.jpg')
collage3 = os.path.join(varkeys.folder_path, 'collage3.jpg')
collage4 = os.path.join(varkeys.folder_path, 'collage4.jpg')
last_wallpaper_path = os.path.join(varkeys.folder_path, 'last_wallpaper.jpg')


# Variable de control para pausar/reanudar el cambio de fondo
running = True
time_remaining = 60  # Tiempo inicial en segundos


# Crear la carpeta si no existe
if not os.path.exists(varkeys.favoritos_folder):
    os.makedirs(varkeys.favoritos_folder)

def save_to_favorites(collage_path):
    #Guarda el collage actual en la carpeta de favoritos.
    if collage_path and os.path.exists(collage_path):
        # Crear un nombre único basado en la hora o un contador
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        favorite_path = os.path.join(varkeys.favoritos_folder, f"favorito_{timestamp}.jpg")
        
        # Copiar el archivo al directorio de favoritos
        shutil.copy(collage_path, favorite_path)
        print(f"Guardado en favoritos: {favorite_path}")
    else:
        print(f"El archivo {collage_path} no existe o no está definido.")


def save_used_collage(collage_path):
    #Guarda el collage utilizado en la carpeta de historial con un nombre único.
    # Obtener el siguiente nombre disponible
    files = os.listdir(varkeys.history_folder)
    print("numeros guardados001", files)
    indices = [int(f.split('.')[0]) for f in files if f.split('.')[0].isdigit()]
    next_index = max(indices, default=0) + 1  # Encuentra el siguiente índice disponible

    # Generar el nuevo nombre del archivo
    new_filename = os.path.join(varkeys.history_folder, f"{next_index}.jpg")
    print("cuando lo guarda aqui?",new_filename)

    # Copiar el archivo al historial
    shutil.copy(collage_path, new_filename)

    return new_filename  # Devuelve la nueva ruta del archivo


def load_last_used_wallpapers():
    # Carga los archivos existentes en el historial si están disponibles
    if os.path.exists(varkeys.history_folder):
        files = os.listdir(varkeys.history_folder)
        files = [f for f in files if f.endswith('.jpg')]  # Asegúrate de solo incluir archivos .jpg

        # Ordena los archivos por el nombre (asumiendo que son números)
        files.sort(key=lambda x: int(x.split('.')[0]))

        # Carga los archivos en la lista last_used_wallpapers
        return [os.path.join(varkeys.history_folder, f) for f in files]
    return []  # Retorna una lista vacía si no hay archivos en la carpeta

# Variable global para almacenar los últimos 10 fondos
last_used_wallpapers = load_last_used_wallpapers()

# variable global para tomar los favoritos
wallpaper_history = []


def add_to_last_used(collage_path):
    # Guarda el collage utilizado en el historial y actualiza la lista de últimos fondos.
    global last_used_wallpapers
    saved_collage = save_used_collage(collage_path)  # Guarda el collage y obtiene su nueva ruta

    # Verificar si el collage ya está en el historial
    if saved_collage not in last_used_wallpapers:
        # Si la lista tiene 10 imágenes, elimina la más antigua
        if len(last_used_wallpapers) >= 10:
            # Elimina el archivo de la imagen más antigua
            oldest_collage = last_used_wallpapers.pop(0)  # Elimina el fondo más antiguo
            if os.path.exists(oldest_collage):
                os.remove(oldest_collage)  # Elimina el archivo físico

        last_used_wallpapers.append(saved_collage)  # Agrega el nuevo fondo al final
        print(f"Collage guardado en historial: {saved_collage}")
    else:
        print(f"El collage {saved_collage} ya está en el historial.")




def apply_previous_wallpaper():
    global last_used_wallpapers
    if len(last_used_wallpapers) > 1:
        last_used_wallpapers.insert(0, last_used_wallpapers.pop(-1))  # Cambia el orden
        set_wallpaper(last_used_wallpapers[0])  # Establece el fondo anterior
        print(f"Fondo cambiado al anterior: {last_used_wallpapers[0]}")
    else:
        print("No hay suficientes fondos previos para regresar.")



# Función para manejar el clic en el botón de favoritos
def on_save_favorite():
    #Guarda la última imagen utilizada como fondo en la carpeta de favoritos.
    if last_used_wallpapers:  # Verifica si hay imágenes en el historial
        last_image = last_used_wallpapers[-1]  # Última imagen de la lista
        if os.path.exists(last_image):
            save_to_favorites(last_image)
        else:
            print(f"El archivo {last_image} no existe en el sistema.")
    else:
        print("No se ha usado ningún fondo aún. No se puede guardar en favoritos.")



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

changing_active = True
mix_mode = True
def toggle_mix_mode(label):
    global mix_mode
    mix_mode = not mix_mode
    mode = "Normal" if mix_mode else "Mix"
    label.config(text=f"Modo actual: {mode}")
    print(f"Modo cambiado a: {mode}")

def toggle_changing(button):
    global changing_active
    changing_active = not changing_active
    if changing_active:
        button.config(text="‖")
        resume_changing()  # Llama a la función para reanudar el cambio
    else:
        button.config(text="⏵")
        stop_changing()  # Llama a la función para detener el cambio
    print(f"Cambio automático {'activado' if changing_active else 'detenido'}")

# Función para crear los collages iniciales
def create_all_collages(label):
    print(f"Usando las carpetas: {varkeys.folder1}, {varkeys.folder2}")
    if mix_mode:
        # Combinar imágenes de ambas carpetas
        create_collage([varkeys.folder1, varkeys.folder2], collage1, label=label)
        create_collage([varkeys.folder1, varkeys.folder2], collage2, label=label)
        create_collage([varkeys.folder1, varkeys.folder2], collage3, label=label)
        create_collage([varkeys.folder1, varkeys.folder2], collage4, label=label)
    else:
        # Usar imágenes de carpetas individuales
        create_collage(varkeys.folder1, collage1, label=label)
        create_collage(varkeys.folder2, collage2, label=label)
        create_collage(varkeys.folder1, collage3, label=label)
        create_collage(varkeys.folder2, collage4, label=label)
    
# Función para crear nuevos collages
def create_new_collages():
    if mix_mode:
        # Modo mix: combinar imágenes de ambas carpetas
        create_collage([varkeys.folder1, varkeys.folder2], collage3, label="new")
        create_collage([varkeys.folder1, varkeys.folder2], collage4, label="new")
    else:
        # Modo normal: usar imágenes de carpetas individuales
        create_collage(varkeys.folder1, collage3, label="new")
        create_collage(varkeys.folder2, collage4, label="new")

# Función para elegir dos collages aleatorios
def select_random_collages():
    selected_collages = random.sample(collages, 2)  # Elige dos collages aleatorios
    return selected_collages



# Cambiar el fondo de pantalla en Windows
def set_wallpaper(image_path, monitor_index=0):
    # Copiar el fondo actual a la ruta designada
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)


# Obtener el fondo de pantalla actual
def get_current_wallpaper():
    print("cual es el ultimo?",last_wallpaper_path)

    return last_wallpaper_path if os.path.exists(last_wallpaper_path) else collage1


# Ciclo para cambiar los collages automáticamente cada minuto
def change_wallpapers_in_background(label, timer_label):
    global running, time_remaining, last_used_wallpapers
    while True:
        if running:
            create_all_collages(label)  # Crear todos los collages de antemano
            # Seleccionar el collage actual y uno nuevo aleatorio para la transición
            current_collage = get_current_wallpaper()  # El collage actual
            print("cual es el ultimo1?",current_collage)
            
            new_collages = select_random_collages()  # Seleccionamos dos collages aleatorios


            # Actualizar el fondo de pantalla
            set_wallpaper(new_collages[0])

            # Guardar el nuevo fondo en la lista de últimos usados
            add_to_last_used(new_collages[0])

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

        # Guardar el collage usado en el historial
        #add_to_last_used(new_collages[0])



def change_wallpapers(label):
    global last_used_wallpapers
    current_wallpaper = get_current_wallpaper()
    print("cual es el ultimo?",current_wallpaper)
    
    create_all_collages(label)  # Crea todos los collages usando el modo actual

    # Seleccionar un collage aleatorio de los pre-creados
    new_collages = select_random_collages()

    # Actualizar el fondo de pantalla
    set_wallpaper(new_collages[0], monitor_index=0)

    # Guardar el collage usado en el historial
    add_to_last_used(new_collages[0])





