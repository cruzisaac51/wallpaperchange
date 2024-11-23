import tkinter as tk
from tkinter import filedialog
import threading
from wallpaper import *
from collage import *


def select_folder(folder_variable):
    selected_folder = filedialog.askdirectory()
    if selected_folder:
        globals()[folder_variable] = selected_folder
        print(f"{folder_variable} actualizado a: {selected_folder}")

def toggle_folder_buttons():
    # Muestra u oculta los botones de selección de carpetas y cambia el tamaño de la ventana
    if folder1_button.winfo_viewable():
        folder1_button.pack_forget()
        folder2_button.pack_forget()
        toggle_button.config(text="▶ Seleccionar Carpetas")
        root.geometry("250x250")  # Volver al tamaño pequeño
    else:
        folder1_button.pack(pady=5)
        folder2_button.pack(pady=5)
        toggle_button.config(text="▼ Ocultar Carpetas")
        root.geometry("250x300")  # Ampliar tamaño de la ventana


def create_interface():
    global folder1_button, folder2_button, toggle_button, mix_button, root

    root = tk.Tk()
    root.title("Wallpaper Changer")
    root.geometry("250x250")

    # Establecer ícono personalizado
    icon_path = "C:/Users/mayra/Documents/wallpaperchange/wcic/wp.ico"
    root.iconbitmap(icon_path)

    status_label = tk.Label(root, text="Modo actual: Mix", font=("Arial", 12))
    status_label.pack(pady=10)

    # Etiqueta para mostrar el número de imágenes que se están pegando en el collage
    collage_label = tk.Label(root, text="Pegando 0 imágenes en el collage")
    collage_label.pack_forget()

    # Etiqueta para mostrar el temporizador
    timer_label = tk.Label(root, text="Próximo cambio en: 60 segundos")
    timer_label.pack(pady=10)

    # Botones para seleccionar las carpetas, inicialmente ocultos
    folder1_button = tk.Button(root, text="Seleccionar Carpeta 1", command=lambda: select_folder('folder1'))
    folder2_button = tk.Button(root, text="Seleccionar Carpeta 2", command=lambda: select_folder('folder2'))

    # Crear un contenedor (Frame) para los botones en la misma fila
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    change_button = tk.Button(button_frame, text="Cambiar Fondo", command=lambda: change_wallpapers(collage_label))
    change_button.grid(row=0, column=0, padx=5, pady=5)

    toggle_change_button = tk.Button(button_frame, text="⏸", command=lambda: toggle_changing(toggle_change_button))
    toggle_change_button.grid(row=0, column=1, padx=5, pady=5)

    mix_button = tk.Button(button_frame, text="Mix", command=lambda: toggle_mix_mode(status_label))
    mix_button.grid(row=0, column=2, padx=5, pady=5)

    # Botón para mostrar/ocultar botones de selección de carpetas
    toggle_button = tk.Button(root, text="▶ Seleccionar Carpetas", command=toggle_folder_buttons)
    toggle_button.pack(pady=5)

    # Iniciar un hilo para cambiar wallpapers en segundo plano
    thread = threading.Thread(target=change_wallpapers_in_background, args=(collage_label, timer_label), daemon=True)
    thread.start()

    root.mainloop()
