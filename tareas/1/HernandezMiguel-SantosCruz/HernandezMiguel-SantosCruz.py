import threading
import random
import time
from collections import deque

num_trabajadores = 5   
peticiones = threading.Semaphore(0)
mutex = threading.Semaphore(1)
cinta = deque()

def msg(rol, id_num, mensaje):
    print(f"[{rol} {id_num}] {mensaje}")

def jefe():
    contador = 1
    while True:
        time.sleep(random.random()*2)
        pagina = f"pagina_web_{contador}.html"
        msg("Jefe", "Unico", f"Recibí conexión de red. Precesando {pagina}...")
        
        with mutex:
            cinta.append(pagina)
        
        peticiones.release()
        contador +=1

def trabajador(id_trabajador):
    tareas_completadas = 0
    tiempo_total = 0

    while True:
        peticiones.acquire()
    
        with mutex: 
            tarea = cinta.popleft()
        msg("Trabajador", id_trabajador, f"Despertado. Atendiendo solicitud: {tarea}")

        tiempo_prosesamiento= random.random()*3 
        time.sleep(tiempo_prosesamiento)

        tareas_completadas += 1
        tiempo_total += tiempo_prosesamiento

        msg("Trabajador", id_trabajador, f"Finalicé solicitud: {tarea}. Tiempo de procesamiento: {tiempo_prosesamiento:.2f}s. Total tareas completadas: {tareas_completadas}.")

threading.Thread(target=jefe).start()

for i in range(num_trabajadores):
    threading.Thread(target=trabajador, args=[i]).start()        