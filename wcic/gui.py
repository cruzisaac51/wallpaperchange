import tkinter as tk
from tkinter import filedialog
import threading
import varkeys
from wallpaper import *
from collage import *
import customtkinter as ctk
from varkeys import folder1, folder2


def select_folder(folder_variable):
    selected_folder = filedialog.askdirectory()
    if selected_folder:
        # Asigna la ruta seleccionada a la variable correspondiente
        if folder_variable == 'folder1':
            varkeys.folder1 = selected_folder
        elif folder_variable == 'folder2':
            varkeys.folder2 = selected_folder
        print(f"{folder_variable} actualizado a: {selected_folder}")



def toggle_folder_buttons():
    # Muestra u oculta los botones de selección de carpetas y cambia el tamaño de la ventana
    if folder1_button.winfo_viewable():
        folder1_button.pack_forget()
        folder2_button.pack_forget()
        toggle_button.config(text="▶ Seleccionar Carpetas")
        root.geometry("250x300")  # Volver al tamaño pequeño
    else:
        folder1_button.pack(pady=5)
        folder2_button.pack(pady=5)
        toggle_button.config(text="▼ Ocultar Carpetas")
        root.geometry("300x350")  # Ampliar tamaño de la ventana

ctk.set_appearance_mode("dark")
#ctk.set_default_color_theme("blue")
def create_interface():
    global folder1_button, folder2_button, toggle_button, mix_button, root

    root = ctk.CTk()
    root.title("Wallpaper Changer")
    root.geometry("250x300")

    # Establecer ícono personalizado
    icon_path = "C:/Users/mayra/Documents/wallpaperchange/wcic/wp.ico"
    root.iconbitmap(icon_path)

    status_label = tk.Label(root, text="Modo actual: Mix", font=("Segoe UI", 15, "bold"), fg="white", bg="#242323")
    status_label.pack(pady=5)

    # Etiqueta para mostrar el número de imágenes que se están pegando en el collage
    collage_label = tk.Label(root, text="Pegando 0 imágenes en el collage")
    collage_label.pack_forget()

    # Etiqueta para mostrar el temporizador
    timer_label = tk.Label(root, text="Próximo cambio en: 60 segundos", font=("Segoe UI", 10), fg="white", bg="#242323")
    timer_label.pack(pady=5)

    # Crear el botón de favoritos
    save_favorite_button = tk.Button(root, text="★", command=on_save_favorite, bg="#3b44ad", fg="white", font=("Segoe UI", 10, "bold"))
    save_favorite_button.pack(pady=10)

    # Botones para seleccionar las carpetas, inicialmente ocultos
    folder1_button = tk.Button(root, text="Seleccionar Carpeta 1", command=lambda: select_folder('folder1'), fg="white", bg="#3b44ad", font=("Segoe UI", 10, "bold"))
    folder2_button = tk.Button(root, text="Seleccionar Carpeta 2", command=lambda: select_folder('folder2'), fg="white", bg="#3b44ad", font=("Segoe UI", 10, "bold"))

    # Crear un contenedor (Frame) para los botones en la misma fila
    button_frame = tk.Frame(root, bg="#242323")
    button_frame.pack(pady=10)

    change_button1 = tk.Button(button_frame, text="<<", command=apply_previous_wallpaper, fg="white", bg="#3b44ad", font=("Segoe UI", 10, "bold"))
    change_button1.grid(row=0, column=0, padx=5, pady=5)

    change_button = tk.Button(button_frame, text=">>", command=lambda: change_wallpapers(collage_label), fg="white", bg="#3b44ad", font=("Segoe UI", 10, "bold"))
    change_button.grid(row=0, column=2, padx=5, pady=5)

    toggle_change_button = tk.Button(button_frame, text="‖", command=lambda: toggle_changing(toggle_change_button), fg="white", bg="#3b44ad", width=5, font=("Segoe UI", 10, "bold"))
    toggle_change_button.grid(row=0, column=1, padx=5, pady=5)

    mix_button = tk.Button(button_frame, text="Mix", command=lambda: toggle_mix_mode(status_label),fg="white", bg="#3b44ad", font=("Segoe UI", 10, "bold"))
    mix_button.grid(row=1, column=1, padx=5, pady=5)

    # Botón para mostrar/ocultar botones de selección de carpetas
    toggle_button = tk.Button(root, text="⏵ Seleccionar Carpetas", command=toggle_folder_buttons, fg="white", bg="#3b44ad", font=("Segoe UI", 10, "bold"))
    toggle_button.pack(pady=5)

    # Iniciar un hilo para cambiar wallpapers en segundo plano
    thread = threading.Thread(target=change_wallpapers_in_background, args=(collage_label, timer_label), daemon=True)
    thread.start()

    root.mainloop()
