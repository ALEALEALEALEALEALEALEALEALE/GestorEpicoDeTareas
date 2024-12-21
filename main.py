from tkinter import Tk, Checkbutton, IntVar, Label, Button, Toplevel, Listbox, END, Entry, messagebox, Canvas
import os
import time
from pygame import mixer
import cv2
from PIL import Image, ImageTk

mixer.init()

tasks_file = "tareas_guardadas.txt"

def cargar_estado():
    estado = {"algebra": 0, "analisis": 0, "poo": 0, "redes": 0}
    if os.path.exists(tasks_file):
        with open(tasks_file, "r") as f:
            for linea in f:
                tarea, valor = linea.strip().split(",")
                estado[tarea] = int(valor)
    return estado

def reproducir_video():
    cap = cv2.VideoCapture("dance.mp4")

    if not cap.isOpened():
        print("Error: No se pudo abrir el archivo de video.")
        return

    mixer.music.load("dance.mp3")
    mixer.music.play()

    video_window = Toplevel()
    video_window.title("¡Felicitaciones, campeón!")
    video_window.geometry("700x500")
    video_window.config(bg="lightblue")

    Label(video_window, text="¡Felicitaciones, campeón! Puedes descansar ahora.", font=("Arial", 16), bg="lightblue", fg="darkblue").pack(pady=10)

    canvas = Canvas(video_window, width=640, height=360, bg="black")
    canvas.pack(pady=10)

    def cerrar_ventana():
        mixer.music.stop()
        video_window.destroy()
        cap.release()
        cv2.destroyAllWindows()

    Button(video_window, text="Cerrar", command=cerrar_ventana, bg="red", fg="white", font=("Arial", 12)).pack(pady=10)

    def actualizar_frame():
        ret, frame = cap.read()
        if not ret:
            cerrar_ventana()
            return

        frame = cv2.resize(frame, (640, 360))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(frame))
        canvas.create_image(0, 0, anchor="nw", image=img)
        canvas.image = img

        video_window.after(10, actualizar_frame)

    actualizar_frame()

def guardar_estado():
    with open(tasks_file, "w") as f:
        f.write(f"algebra,{algebra.get()}\n")
        f.write(f"analisis,{analisis.get()}\n")
        f.write(f"poo,{poo.get()}\n")
        f.write(f"redes,{redes.get()}\n")

    if all([algebra.get(), analisis.get(), poo.get(), redes.get()]):
        reproducir_video()

def mostrar_tareas():
    tareas_completadas = []
    if algebra.get():
        tareas_completadas.append("Álgebra Lineal")
    if analisis.get():
        tareas_completadas.append("Análisis Matemático")
    if poo.get():
        tareas_completadas.append("Programación Orientada a Objetos (POO)")
    if redes.get():
        tareas_completadas.append("Redes")

    completadas_label.config(text="Tareas Completadas:\n" + "\n".join(tareas_completadas))
    guardar_estado()

def agregar_tarea():
    def guardar_nueva_tarea():
        nueva_tarea = nueva_tarea_entry.get()
        if nueva_tarea:
            lista_tareas.insert(END, nueva_tarea)
            with open("tareas_personalizadas.txt", "a") as f:
                f.write(nueva_tarea + "\n")
        ventana_nueva_tarea.destroy()

    ventana_nueva_tarea = Toplevel(ventana)
    ventana_nueva_tarea.title("Agregar Tarea")
    ventana_nueva_tarea.geometry("300x150")
    Label(ventana_nueva_tarea, text="Nueva Tarea:").pack(pady=5)
    nueva_tarea_entry = Entry(ventana_nueva_tarea, width=30)
    nueva_tarea_entry.pack(pady=5)
    Button(ventana_nueva_tarea, text="Guardar", command=guardar_nueva_tarea).pack(pady=10)

def cargar_tareas_personalizadas():
    if os.path.exists("tareas_personalizadas.txt"):
        with open("tareas_personalizadas.txt", "r") as f:
            for tarea in f:
                lista_tareas.insert(END, tarea.strip())

estado_inicial = cargar_estado()

ventana = Tk()
ventana.title("Lista de Tareas")
ventana.geometry("400x400")
ventana.config(bg="lightyellow")

algebra = IntVar(value=estado_inicial["algebra"])
analisis = IntVar(value=estado_inicial["analisis"])
poo = IntVar(value=estado_inicial["poo"])
redes = IntVar(value=estado_inicial["redes"])

titulo_label = Label(ventana, text="Lista de Tareas para el Fin de Semana", font=("Arial", 12), bg="lightyellow")
titulo_label.pack(pady=10)

Checkbutton(ventana, text="Álgebra Lineal", variable=algebra, command=guardar_estado, bg="lightyellow").pack(anchor="w")
Checkbutton(ventana, text="Análisis Matemático", variable=analisis, command=guardar_estado, bg="lightyellow").pack(anchor="w")
Checkbutton(ventana, text="Programación Orientada a Objetos (POO)", variable=poo, command=guardar_estado, bg="lightyellow").pack(anchor="w")
Checkbutton(ventana, text="Redes", variable=redes, command=guardar_estado, bg="lightyellow").pack(anchor="w")

mostrar_button = Button(ventana, text="Mostrar Tareas Completadas", command=mostrar_tareas, bg="gold", font=("Arial", 10))
mostrar_button.pack(pady=10)

completadas_label = Label(ventana, text="", font=("Arial", 10), bg="lightyellow")
completadas_label.pack()

Button(ventana, text="Agregar Nueva Tarea", command=agregar_tarea, bg="gold", font=("Arial", 10)).pack(pady=10)

Label(ventana, text="Tareas Personalizadas:", bg="lightyellow").pack(pady=5)
lista_tareas = Listbox(ventana, width=50, height=10)
lista_tareas.pack(pady=5)

cargar_tareas_personalizadas()

ventana.mainloop()
