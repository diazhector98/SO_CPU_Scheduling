import queue as Q
from fcfs import fcfs
from priority_expulsivo import priority_expulsivo

nombre_de_archivo = 'entrada_expulsivo.txt'
archivo_de_entrada = open(nombre_de_archivo, 'r')
lineas_de_archivo_de_entrada = archivo_de_entrada.readlines()
archivo_de_entrada.close()

algoritmo = lineas_de_archivo_de_entrada[0]
algoritmo = algoritmo.replace("\n", "")

if algoritmo == "prioPreemptive":
    priority_expulsivo(lineas_de_archivo_de_entrada=lineas_de_archivo_de_entrada)
elif algoritmo == "FCFS":
    fcfs(lineas_de_archivo_de_entrada=lineas_de_archivo_de_entrada, quantum=1000)
