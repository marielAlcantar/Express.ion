"""
============================================
Express.ion
============================================
Autor: Karla Mariel Alcantar Domínguez
Año: 2025

-----------
Descripción
-----------
Aplicación de escritorio en Python/Tkinter que ejecuta una ventana de 
selección en el que hay tres opciones, la primera corresponde a la 
grabación de expresiones sin  ningún estímulo presentado, la segunda 
sección corresponde a la grabación con estímulos presentados y la 
última sección corresponde a la grabación de expresiones mirandose en 
pantalla.

Funcionamiento
--------------
1. Ventana inicial: Muestra instrucciones y un botón para comenzar el experimento.
2. Menú principal con botones para elegir entre tres secciones de experimento y salir del programa.
3. Sección 1: Expresión + Neutral
   -Muestra en pantalla completa las palabras de las expresiones (Alegría, Tristeza, Enojo, etc.).
   -Por cada expresión, la cámara graba un segmento de video de duración fija (DURACION).
3. Sección 2: Imágenes
   -Carga todas las imágenes encontradas en la carpeta RUTA_IMAGENES.
   -Las despliega en pantalla completa una por una, mientras la cámara graba cada estímulo.
   -Cada video se guarda con el nombre de la imagen correspondiente. 
4. Sección 3: Cámara 
   -Graba directamente con OpenCV en pantalla completa.
   -Cada expresión se sobrepone como texto en la parte superior izquierda.
   -El video se ajusta a la resolución de pantalla con bordes negros si es necesario.
   -Se graba un archivo AVI por cada expresión.
5. Al finalizar cada sección se muestra un mensaje emergente con confirmación de grabación.
6. Todos los videos se almacenan en la carpeta Documents\Facial expressions records\Grabacion_YYYYMMDD_HHMMSS, organizada en subcarpetas:
   -Seccion1
   -Seccion2
   -Seccion3
----------------
Clases y Métodos
----------------
- grabar_segmento(nombre_archivo, duracion): graba un segmento de video desde la cámara por duracion segundos.
- iniciar_pantalla(): abre pantalla completa.
- cerrar_pantalla(): cierra Pygame.
- mostrar_mensaje(pantalla, ANCHO, ALTO, texto): despliega texto grande en pantalla.
- mostrar_color(pantalla, color, nombre_video): llena la pantalla de un color sólido y graba.
- mostrar_circulo(pantalla, ANCHO, ALTO, nombre_video): muestra un círculo negro sobre fondo blanco.
- mostrar_imagen(pantalla, ANCHO, ALTO, ruta, nombre_video): despliega una imagen de archivo y graba la reacción.
- seccion1(): ejecuta la grabación de emociones sin estímulo.
- seccion2(): ejecuta la grabación con imágenes.
- seccion3(): ejecuta la grabación frente a cámara con texto.
- mostrar_menu(root): muestra el menú principal de selección de secciones.
- cerrar_programa(root): libera la cámara y cierra la ventana de Tkinter de forma segura.
- ventana inicial(): ventana principal con botones para seleccionar cada sección o salir.
---------------------------
Parámetros de Configuración
---------------------------
-DURACION: 10 segundos (editable).
-FPS: 20 cuadros por segundo.
-RUTA_IMAGENES: ruta local a la carpeta con estímulos visuales.
-EMOCIONES: lista de etiquetas a presentar (Alegría, Tristeza, etc.).
-main_root: carpeta raíz en Documents donde se almacenan todas las grabaciones.
-Estructura de carpetas:
    Facial expressions records/
    Grabacion_YYYYMMDD_HHMMSS/
        Seccion1/
        Seccion2/
        Seccion3/
--------------
Ejemplo de Uso
--------------
Ejecutar el archivo principal:
    python emociones.py
------------
Dependencias
------------
- **Python 3.8+**
- **Tkinter**
  - Windows/macOS: viene con la instalación oficial de Python.
  - Linux: instalar vía sistema (p. ej., `sudo apt-get install python3-tk`).
- Pygame (para mostrar imágenes y colores)
- OpenCV (para capturar y grabar cámara)
- Numpy (para manejar imágenes y marcos negros)
- PIL / Pillow (para dibujar texto sobre imágenes y soportar acentos)
-----
Notas
-----
- Los videos se guardan en formato XVID/AVI.
- Si la cámara no responde, revisar que no esté siendo usada por otra aplicación.
- El efecto espejo (cv2.flip) está activado en la Sección 3 para simular vista natural.
- En Sección 2, las imágenes deben estar en RUTA_IMAGENES. Se recomienda formato JPG o PNG.
- Los mensajes emergentes de Tkinter ayudan a confirmar el avance del experimento.
"""
import os
import time
import cv2
import pygame
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ==============================
# CONFIGURACIÓN
# ==============================
main_root = str(Path.home() / "Documents" / "Facial expressions records")
DURACION = 2  # segundos de grabación
FPS = 20.0  # frames por segundo
RUTA_IMAGENES = r'D:\9no\SS\Sentimientos\Imagenes2'
EMOCIONES = ["Neutral", "Alegría", "Tristeza", "Enojo", "Sorprendido", "Asco", "Miedo"]

# ==============================
# INICIO CÁMARA
# ==============================
camara = cv2.VideoCapture(0)
ancho_cam = int(camara.get(cv2.CAP_PROP_FRAME_WIDTH))
alto_cam = int(camara.get(cv2.CAP_PROP_FRAME_HEIGHT))

def grabar_segmento(nombre_archivo, duracion=DURACION):
    """Graba un video de la cámara durante `duracion` segundos"""
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(nombre_archivo, fourcc, FPS, (ancho_cam, alto_cam))
    inicio = time.time()
    while (time.time() - inicio) < duracion:
        ret, frame = camara.read()
        if ret:
            out.write(frame)
        else:
            break
    out.release()

# ==============================
# FUNCIONES DE PYGAME
# ==============================
def iniciar_pantalla():
    pygame.init()
    pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    ANCHO, ALTO = pantalla.get_size()
    return pantalla, ANCHO, ALTO

def cerrar_pantalla():
    pygame.quit()

def mostrar_mensaje(pantalla, ANCHO, ALTO, texto, fondo=(0, 0, 0), color_texto=(255, 255, 255)):
    pantalla.fill(fondo)
    fuente = pygame.font.Font(None, 100)
    render = fuente.render(texto, True, color_texto)
    rect = render.get_rect(center=(ANCHO // 2, ALTO // 2))
    pantalla.blit(render, rect)
    pygame.display.flip()

def mostrar_imagen(pantalla, ANCHO, ALTO, ruta, nombre_video):
    img = pygame.image.load(ruta)
    img = pygame.transform.scale(img, (ANCHO, ALTO))
    pantalla.blit(img, (0, 0))
    pygame.display.flip()
    grabar_segmento(nombre_video)

# ==============================
# CREAR CARPETAS DINÁMICAS
# ==============================
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
RUTA_SALIDA = os.path.join(main_root, f"Grabacion_{timestamp}")

carpeta_s1 = os.path.join(RUTA_SALIDA, "Seccion1")
carpeta_s2 = os.path.join(RUTA_SALIDA, "Seccion2")
carpeta_s3 = os.path.join(RUTA_SALIDA, "Seccion3")

for c in [carpeta_s1, carpeta_s2, carpeta_s3]:
    os.makedirs(c, exist_ok=True)

# ==============================
# SECCIONES
# ==============================
def seccion1():
    pantalla, ANCHO, ALTO = iniciar_pantalla()
    for emo in EMOCIONES:
        mostrar_mensaje(pantalla, ANCHO, ALTO, emo)
        nombre_video = f"emocion_{emo}.avi"
        grabar_segmento(os.path.join(carpeta_s1, nombre_video), DURACION)
    cerrar_pantalla()
    messagebox.showinfo("Finalizado", "Sección 1 completada. Videos guardados en carpeta Seccion1.")

def seccion2():
    pantalla, ANCHO, ALTO = iniciar_pantalla()
    if os.path.exists(RUTA_IMAGENES):
        imagenes = sorted(os.listdir(RUTA_IMAGENES))
        for img in imagenes:
            ruta = os.path.join(RUTA_IMAGENES, img)
            if os.path.isfile(ruta):
                nombre_salida = os.path.splitext(img)[0] + ".avi"
                ruta_salida = os.path.join(carpeta_s2, nombre_salida)
                mostrar_imagen(pantalla, ANCHO, ALTO, ruta, ruta_salida)
    else:
        messagebox.showerror("Error", "No se encontró la carpeta de imágenes.")
    cerrar_pantalla()
    messagebox.showinfo("Sección 2", "Grabación finalizada.")

def seccion3():
    cv2.namedWindow("Sección 3 - Cámara", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Sección 3 - Cámara", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    screen_res = (1920, 1080)

    for emo in EMOCIONES:
        inicio = time.time()
        nombre_archivo = os.path.join(carpeta_s3, f"{emo}.avi")
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(nombre_archivo, fourcc, FPS, (ancho_cam, alto_cam))

        while (time.time() - inicio) < DURACION:
            ret, frame = camara.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            h, w = frame.shape[:2]
            screen_w, screen_h = screen_res
            scale = min(screen_w / w, screen_h / h)
            new_w, new_h = int(w * scale), int(h * scale)
            resized = cv2.resize(frame, (new_w, new_h))
            canvas = np.zeros((screen_h, screen_w, 3), dtype=np.uint8)
            x_offset = (screen_w - new_w) // 2
            y_offset = (screen_h - new_h) // 2
            canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized

            # Dibujar texto con PIL (para acentos)
            img_pil = Image.fromarray(canvas)
            draw = ImageDraw.Draw(img_pil)
            font = ImageFont.truetype("arial.ttf", 70)
            draw.text((50, 50), emo, font=font, fill=(255, 0, 0))
            canvas = np.array(img_pil)

            cv2.imshow("Sección 3 - Cámara", canvas)
            out.write(frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

        out.release()

    cv2.destroyAllWindows()
    messagebox.showinfo("Sección 3", "Grabación finalizada.")

# ==============================
# INTERFAZ UNIFICADA
# ==============================
def mostrar_menu(root):
    """Reemplaza el contenido de la ventana con el menú principal."""
    for widget in root.winfo_children():
        widget.destroy()

    ttk.Label(root, text="Seleccione:", font=("Arial", 14)).pack(pady=20)
    ttk.Button(root, text="Sección 1: Sin estímulo", command=seccion1).pack(pady=10)
    ttk.Button(root, text="Sección 2: Con estímulo visual", command=seccion2).pack(pady=10)
    ttk.Button(root, text="Sección 3: Cámara + Texto", command=seccion3).pack(pady=10)
    ttk.Button(root, text="Salir", command=lambda: cerrar_programa(root)).pack(pady=20)


def cerrar_programa(root):
    """Cierra la cámara y la ventana principal de forma segura."""
    try:
        if camara.isOpened():
            camara.release()
        cv2.destroyAllWindows()
    except:
        pass
    root.destroy()


def ventana_inicial():
    """Ventana con instrucciones y botón de comenzar"""
    root = tk.Tk()
    root.title("Instrucciones")
    root.geometry("800x500")

    # Cuando el usuario intenta cerrar la ventana (X)
    root.protocol("WM_DELETE_WINDOW", lambda: cerrar_programa(root))

    texto = (
        "Instrucciones:\n\n"
        "Sección 1:\nHaz la expresión que se muestra en el texto de cada diapositiva durante 10 segundos.\n\n"
        "Sección 2:\nHaz la expresión que se muestra en la imagen durante 10 segundos.\n\n"
        "Sección 3:\nMírate en la cámara y realiza la expresión que corresponda al texto durante 10 segundos.\n"
    )

    ttk.Label(root, text=texto, wraplength=550, justify="left", font=("Arial", 12)).pack(padx=20, pady=30)
    ttk.Button(root, text="Comenzar", command=lambda: mostrar_menu(root)).pack(pady=10)

    root.mainloop()

# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    ventana_inicial()
