import os
import random
from PIL import Image
# Crear un collage con imágenes seleccionadas

mix_mode = False

def create_collage(image_folder, output_path, min_images=0, max_images=4, screen_size=(1920, 1090), label=None):
    # Calcular el tamaño del canvas basado en la resolución de la pantalla
    canvas_width = int(screen_size[0])
    canvas_height = int(screen_size[1])

    #print(f"image_folders recibido: {image_folder} ({type(image_folder)})")
    # Manejar múltiples carpetas
    if isinstance(image_folder, list):
        images = []
        for folder in image_folder:
            images.extend([
                os.path.join(folder, img)
                for img in os.listdir(folder)
                if img.lower().endswith(('.jpg', '.jpeg', '.png'))
            ])
    else:
        images = [
            os.path.join(image_folder, img)
            for img in os.listdir(image_folder)
            if img.lower().endswith(('.jpg', '.jpeg', '.png'))
        ]

    if not images:
        print(f"⚠️ No se encontraron imágenes válidas en {image_folder}")
        return  # o podrías poner una imagen por defecto en lugar de romper


    # Seleccionar un número aleatorio de imágenes entre min_images y max_images
    num_images = random.randint(min_images, max_images)

    # Actualizar la etiqueta, si existe
    if label:
        label.config(text=f"Pegando {num_images} imágenes en el collage")

    # Asegurarse de que no se seleccionen más imágenes de las que hay disponibles
    num_images = min(num_images, len(images))

    selected_images = random.sample(images, num_images)

    # Seleccionar una imagen aleatoria para el fondo
    background_image_path = random.choice(images)
    background_image = Image.open(background_image_path)

    # Redimensionar el fondo al tamaño del canvas
    background_image = background_image.resize((canvas_width, canvas_height))

    # Crear el canvas del collage usando la imagen de fondo
    collage = Image.new('RGB', (canvas_width, canvas_height))
    collage.paste(background_image, (0, 0))

    # Variables para almacenar las posiciones donde se pegarán las imágenes
    x_offset = 0
    y_offset = 0
    max_row_height = 0


    if num_images == 0:
        print("se usaron 0 imágenes en 12")
        
        # Parte izquierda para 4 imágenes en una cuadrícula 2x2 (65% del ancho)
        left_width = int(canvas_width * 0.65)
        square_width = left_width // 2
        square_height = canvas_height // 2

        # Parte derecha para rectángulo vertical dividido en 2 columnas de 6 espacios (35% del ancho)
        right_width = int(canvas_width * 0.35)
        cell_width = right_width // 2
        cell_height = canvas_height // 4

        # Seleccionar 16 imágenes aleatorias sin repetirse
        selected_images = random.sample(images, 16)

        # Las primeras 4 imágenes se colocan en la parte izquierda (2x2 cuadrícula)
        left_images = selected_images[:4]
        
        # Las siguientes 12 imágenes se colocan en la parte derecha (12 espacios en 2 columnas)
        right_images = selected_images[4:]

        # Colocar las 4 imágenes en la parte izquierda (2x2 cuadrícula)
        for i in range(4):
            img = Image.open(left_images[i])
            img = img.resize((square_width, square_height))
            
            # Posicionar en cuadrícula
            x_offset = (i % 2) * square_width
            y_offset = (i // 2) * square_height
            collage.paste(img, (x_offset, y_offset))

        # Colocar las 12 imágenes en el área de columnas verticales a la derecha
        for j in range(8):
            img = Image.open(right_images[j])
            img = img.resize((cell_width, cell_height))
            
            # Posicionar en las 12 celdas del lado derecho
            x_offset = left_width + (j % 2) * cell_width
            y_offset = (j // 2) * cell_height
            collage.paste(img, (x_offset, y_offset))

    # Si hay 1 imagen, aplicamos la lógica específica
    # Verificar si la imagen es horizontal o vertical
    elif num_images == 1:
        # Filtro de imágenes que tengan un ancho mayor a 1/3 del canvas
        valid_images = [img for img in selected_images if Image.open(img).width > canvas_width // 3]
        
        # Si no hay imágenes válidas, utilizamos la imagen seleccionada originalmente
        if valid_images:
            img_path = random.choice(valid_images)  # Seleccionamos una de las imágenes válidas
        else:
            img_path = selected_images[0]  # Si no hay válidas, usamos la seleccionada original

        img = Image.open(img_path)
        img_ratio = img.width / img.height

        # Verificar si la imagen es horizontal o vertical
        if img.width > img.height:
            # Imagen horizontal: hacer que cubra todo el ancho del canvas
            img_width = canvas_width
            img_height = int(img_width / img_ratio)
            
            # Si la altura de la imagen es mayor que la altura del canvas, ajustarla
            if img_height > canvas_height:
                img_height = canvas_height
                img_width = int(img_height * img_ratio)
        else:
            # Imagen vertical: hacer que cubra toda la altura del canvas
            img_height = canvas_height
            img_width = int(img_height * img_ratio)

            # Si el ancho de la imagen es mayor que el ancho del canvas, ajustarlo
            if img_width > canvas_width:
                img_width = canvas_width
                img_height = int(img_width / img_ratio)

        # Redimensionar la imagen
        img = img.resize((img_width, img_height))

        # Calcular los offsets para centrar la imagen
        x_offset = (canvas_width - img_width) // 2  # Centrar horizontalmente
        y_offset = (canvas_height - img_height) // 2  # Centrar verticalmente

        # Pegar la imagen en el collage
        collage.paste(img, (x_offset, y_offset))


    # Si hay 2 imágenes, las colocamos lado a lado
    elif num_images == 2:
        img_width = canvas_width // 2  # Dividir el canvas en dos
        img_height = canvas_height  # Mantener la altura completa
        
        # Pegar cada imagen
        for i in range(2):
            img = Image.open(selected_images[i])
            img = img.resize((img_width, img_height))
            collage.paste(img, (i * img_width, 0))  # Pegar una imagen a la derecha de la otra
    
    elif num_images == 3:
        img_width = canvas_width // 3  # Dividir el canvas en tres partes iguales
        img_height = canvas_height  # Mantener la altura completa

        # Pegar cada imagen en una columna
        for i in range(3):
            img = Image.open(selected_images[i])
            img = img.resize((img_width, img_height))
            collage.paste(img, (i * img_width, 0))  # Pegar las imágenes de izquierda a derecha

    elif num_images == 4:

        # Dimensiones iniciales para la cuadrícula (2x2)
        img_width = canvas_width // 2
        img_height = canvas_height // 2
        occupied_area = 0  # Variable para almacenar el área ocupada por las imágenes

        # Primero, calcular el área ocupada por las imágenes redimensionadas en cuadrícula
        for img_path in selected_images:
            img = Image.open(img_path)

            # Calcular la relación de aspecto y redimensionar
            img_ratio = img.width / img.height
            if img_ratio > 1:
                img = img.resize((img_width, int(img_width / img_ratio)))
            else:
                img = img.resize((int(img_height * img_ratio), img_height))

            # Sumar el área ocupada por cada imagen
            occupied_area += img.width * img.height

        # Verificar si el área ocupada es menor a la mitad del canvas
        canvas_area = canvas_width * canvas_height
        if occupied_area < canvas_area / 2 and occupied_area >= 5 * canvas_area / 12:
            print("se supone es vertical ")
            # Cambiar a disposición en columnas verticales (4 espacios)
            img_width = canvas_width // 4
            img_height = canvas_height  # Mantener la altura completa del canvas
            for i, img_path in enumerate(selected_images):
                img = Image.open(img_path)

                # Redimensionar para columnas verticales
                img_ratio = img.width / img.height
                if img_ratio > 1:
                    img = img.resize((img_width, int(img_width / img_ratio)))
                else:
                    img = img.resize((int(img_height * img_ratio), img_height))

                # Posicionar en columnas
                x_offset = i * img_width
                y_offset = (canvas_height - img.height) // 2
                collage.paste(img, (x_offset, y_offset))
        else:
            print("se ocupa el normal")
            # Si el área es suficiente, usar la disposición en cuadrícula (2x2)
            for i, img_path in enumerate(selected_images):
                img = Image.open(img_path)

                # Redimensionar la imagen manteniendo la relación de aspecto
                img_ratio = img.width / img.height
                if img_ratio > 1:
                    img = img.resize((img_width, int(img_width / img_ratio)))
                else:
                    img = img.resize((int(img_height * img_ratio), img_height))

                # Posicionar en cuadrícula
                if i % 2 == 0:  # Izquierda
                    x_offset = 0
                else:  # Derecha
                    x_offset = img_width
                if i < 2:  # Fila superior
                    y_offset = 0
                else:  # Fila inferior
                    y_offset = img_height

                # Centrar la imagen en su celda
                centered_x = x_offset + (img_width - img.width) // 2
                centered_y = y_offset + (img_height - img.height) // 2
                collage.paste(img, (centered_x, centered_y))

        # Guardar el collage
        collage.save(output_path)





    else:
        x_offset = 0
        y_offset = 0
        max_row_height = 0
        adjusted_img_width = None  # Para guardar el ancho ajustado de la primera fila
        min_img_width = canvas_width // 4  # Establecer un ancho mínimo permitido (ajusta según tus necesidades)

        img_width = canvas_width // min(num_images, max_images)  # Calcular el ancho de cada imagen
        row_images = []  # Lista para almacenar imágenes de la fila actual

        for img_path in selected_images:
            img = Image.open(img_path)
            img_ratio = img.width / img.height

            # Calcular el alto de la imagen manteniendo su relación de aspecto
            img_height = int(img_width / img_ratio)
            img = img.resize((img_width, img_height))

            # Verificar si la imagen cabe en la fila actual o si el ancho es menor que el límite mínimo
            if x_offset + img_width >= canvas_width:
                # Si hay imágenes en la fila actual
                if row_images:
                    # Calcular nuevo ancho (95% del canvas)
                    scaled_width = int(canvas_width * 0.99)
                    # Recalcular img_width para la fila actual
                    adjusted_img_width = scaled_width // len(row_images)

                    # Redimensionar y pegar todas las imágenes de la fila actual con el nuevo ancho
                    for i, im in enumerate(row_images):
                        im_ratio = im.width / im.height
                        im_height = int(adjusted_img_width / im_ratio)
                        im = im.resize((adjusted_img_width, im_height))
                        collage.paste(im, (i * adjusted_img_width, y_offset))

                # Actualizar los desplazamientos para la nueva fila
                x_offset = 0  # Reiniciar x_offset para nueva fila
                y_offset += max_row_height  # Mover hacia abajo en el collage
                max_row_height = 0  # Reiniciar la altura máxima de la fila
                row_images = []  # Reiniciar la lista de imágenes para la nueva fila

                # Asegurarse de que las siguientes imágenes usen el mismo ancho de la primera fila
                img_width = adjusted_img_width if adjusted_img_width else img_width

            # Añadir la imagen a la lista de la fila actual
            row_images.append(img)
            x_offset += img_width  # Actualizar el desplazamiento en x
            max_row_height = max(max_row_height, img_height)  # Actualizar la altura máxima de la fila

        # Redimensionar y pegar la última fila al 95% si aún quedan imágenes no pegadas
        if row_images:
            if adjusted_img_width is None:
                # Si no hubo un salto de fila antes, redimensionar esta fila al 95%
                scaled_width = int(canvas_width * 0.99)
                adjusted_img_width = scaled_width // len(row_images)

            for i, im in enumerate(row_images):
                im_ratio = im.width / im.height
                im_height = int(adjusted_img_width / im_ratio)
                im = im.resize((adjusted_img_width, im_height))
                collage.paste(im, (i * adjusted_img_width, y_offset))

    # Guardar el collage
    collage.save(output_path)