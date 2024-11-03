import tkinter as tk
from tkinter import filedialog
import threading
from wallpaper import *
# Función para parar el ciclo
def stop_changing():
    global running
    running = False

# Función para reanudar el ciclo
def resume_changing():
    global running
    running = True
    
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
        root.geometry("250x260")  # Volver al tamaño pequeño
    else:
        folder1_button.pack(pady=5)
        folder2_button.pack(pady=5)
        toggle_button.config(text="▼ Ocultar Carpetas")
        root.geometry("250x350")  # Ampliar tamaño de la ventana


def create_interface():
    global folder1_button, folder2_button, toggle_button, root

    root = tk.Tk()
    root.title("Wallpaper Changer")
    root.geometry("250x260")

    # Establecer ícono personalizado
    icon_path = "C:/Users/mayra/Documents/wallpaperchange/wcic/wp.ico"
    root.iconbitmap(icon_path)

    # Etiqueta para mostrar el número de imágenes que se están pegando en el collage
    collage_label = tk.Label(root, text="Pegando 0 imágenes en el collage")
    collage_label.pack_forget()

    # Etiqueta para mostrar el temporizador
    timer_label = tk.Label(root, text="Próximo cambio en: 60 segundos")
    timer_label.pack(pady=10)

    # Botones para seleccionar las carpetas, inicialmente ocultos
    folder1_button = tk.Button(root, text="Seleccionar Carpeta 1", command=lambda: select_folder('folder1'))
    folder2_button = tk.Button(root, text="Seleccionar Carpeta 2", command=lambda: select_folder('folder2'))

    # Botón para cambiar el fondo de pantalla manualmente
    change_button = tk.Button(root, text="Cambiar Fondo", command=lambda: change_wallpapers(collage_label))
    change_button.pack(pady=10)

    # Botón para parar el cambio automático
    stop_button = tk.Button(root, text="Parar Cambio", command=stop_changing)
    stop_button.pack(pady=10)

    # Botón para reanudar el cambio automático
    resume_button = tk.Button(root, text="Reanudar Cambio", command=resume_changing)
    resume_button.pack(pady=10)

    # Botón para mostrar/ocultar botones de selección de carpetas
    toggle_button = tk.Button(root, text="▶ Seleccionar Carpetas", command=toggle_folder_buttons)
    toggle_button.pack(pady=5)

    # Iniciar un hilo para cambiar wallpapers en segundo plano
    thread = threading.Thread(target=change_wallpapers_in_background, args=(collage_label, timer_label), daemon=True)
    thread.start()

    root.mainloop()