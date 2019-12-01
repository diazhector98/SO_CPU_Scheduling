import queue as Q

nombre_de_archivo = 'entrada.txt'

archivo_de_entrada = open(nombre_de_archivo, 'r')
lineas_de_archivo_de_entrada = archivo_de_entrada.readlines()
archivo_de_entrada.close()



class Proceso:
    def __init__(self, id, prioridad):
        self.id = id
        self.prioridad = prioridad
        return
    def __lt__(self, other):
        return self.prioridad < other.prioridad

class Evento:
    def __init__(self, texto):
        componentes = texto.split()
        self.tiempo = componentes[0]
        if componentes[1] == "Llega":
            self.tipo = "Llegada"
            self.proceso = Proceso(id=componentes[2], prioridad=componentes[4])
        elif componentes[1] == "quantum":
            self.tipo = "Quantum"
        elif componentes[1] == "Acaba":
            self.tipo = "Acaba"
            self.proceso = Proceso(id=componentes[2], prioridad=None)
        elif componentes[1] == "startI/O":
            self.tipo = "StartI/0"
            self.proceso = Proceso(id=componentes[2], prioridad=None)
        elif componentes[1] == "endI/O":
            self.tipo = "EndI/0"
            self.proceso = Proceso(id=componentes[2], prioridad=None)
        elif componentes[1] == "endSimulacion":
            self.tipo = "EndSimulacion"


class ColaDeListos:
    def __init__(self):
        self.filaSinPrioridades = []
        self.fila = Q.PriorityQueue()
    def getFila(self):
        return self.fila
    def getFilaIDs(self):
        ids = []
        for proceso in self.filaSinPrioridades:
            ids.append(proceso.id)
        return ids
    def insertar(self, proceso):
        self.filaSinPrioridades.append(proceso)
        self.fila.put(proceso)
    def pop(self):
        self.filaSinPrioridades.pop()
        return self.fila.get()

class CPU:
    def __init__(self):
        self.proceso = None
    def getProceso(self):
        return self.proceso
    def insertarProceso(self, proceso):
        self.proceso = proceso
    def sacarProceso(self):
        self.proceso = None


class ProcesosBloqueados:
    def __init__(self):
        self.procesos = []
    def getLista(self):
        return self.procesos
    def insertar(self, proceso):
        self.procesos.append(proceso)

class ProcesosTerminados:
    def __init__(self):
        self.procesos = []
    def getProcesos(self):
        return self.procesos
    def insertar(self, proceso):
        self.procesos.append(proceso)


line_index = 0
algoritmo = lineas_de_archivo_de_entrada[line_index]
line_index += 1
quantum = lineas_de_archivo_de_entrada[line_index]
line_index += 1

cola_de_listos = ColaDeListos()
cpu = CPU()
procesos_bloqueados = ProcesosBloqueados()
procesos_terminados = ProcesosTerminados()


def manejarLlegada(evento, cola_de_listos, cpu, procesos_bloqueados, procesos_terminados):
    if cpu.proceso == None:
        cpu.insertarProceso(evento.proceso)
    else:
        cola_de_listos.insertar(evento.proceso)
def manejarAcaba(evento, cola_de_listos, cpu, procesos_bloqueados, procesos_terminados):
    print(evento.proceso.id)
    cpu.sacarProceso()
    if cola_de_listos.getFila().qsize() != 0:
        cpu.insertarProceso(cola_de_listos.pop())
def manejarStartIO(evento, cola_de_listos, cpu, procesos_bloqueados, procesos_terminados):
    print(evento.proceso.id)
def manejarEndIO(evento, cola_de_listos, cpu, procesos_bloqueados, procesos_terminados):
    print(evento.proceso.id)



manejadores = {
'Llegada' : manejarLlegada,
'Acaba' : manejarAcaba,
'StartI/O': manejarStartIO,
'EndI/0': manejarEndIO,
'EndSimulacion': None
}

while line_index < len(lineas_de_archivo_de_entrada):
    linea = lineas_de_archivo_de_entrada[line_index]
    evento = Evento(texto=linea)

    print("Evento: " , linea)
    funcion = manejadores.get(evento.tipo)
    if funcion != None:
        funcion(evento=evento, cola_de_listos=cola_de_listos, cpu=cpu, procesos_bloqueados=procesos_bloqueados, procesos_terminados=procesos_terminados)
        if cpu.proceso != None:
            print("Proceso En CPU: ", cpu.proceso.id)
        cola = cola_de_listos.getFila().queue
        print("Cola de listos: ")
        for p in cola:
            print("Id: ", p.id, "Prioridad: ", p.prioridad)
        print("------------------------")


    line_index += 1

from texttable import Texttable
t = Texttable()
t.add_rows([['Name', 'Age'], ['Alice', 24], ['Bob', 19]])
print(t.draw())
