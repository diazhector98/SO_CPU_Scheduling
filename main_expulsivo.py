import queue as Q

nombre_de_archivo = 'entrada_expulsivo.txt'

archivo_de_entrada = open(nombre_de_archivo, 'r')
lineas_de_archivo_de_entrada = archivo_de_entrada.readlines()
archivo_de_entrada.close()



class Proceso:
    def __init__(self, id, prioridad, tiempoLlegada):
        self.id = id
        self.prioridad = prioridad
        self.tiempoLlegada = tiempoLlegada
        self.tiempoTerminacion = 0
        self.tiempoCPU = 0
        self.tiempoEspera = 0
        self.turnaround = 0
        self.tiempoIO = 0
        return
    def __lt__(self, other):
        return self.prioridad < other.prioridad

    def setTiempoLlegadaCPU(self, tiempo):
        self.tiempoLlegadaCPU = tiempo
    def setTiempoTerminaCPU(self, tiempo):
        self.tiempoTerminaCPU = tiempo
        self.tiempoCPU += (self.tiempoTerminaCPU-self.tiempoLlegadaCPU)
    def setStartIO(self, tiempo):
        self.startIOTiempo = tiempo
    def setEndIO(self, tiempo):
        self.endIOTiempo = tiempo
        self.tiempoIO += (self.endIOTiempo - self.startIOTiempo)
    def setTiempoLlegada(self, tiempoLlegada):
        self.tiempoLlegada = tiempoLlegada
    def setTiempoTerminacion(self, tiempoTerminacion):
        self.tiempoTerminacion = tiempoTerminacion

class Evento:
    def __init__(self, texto, proceso):
        self.texto = texto
        componentes = texto.split()
        self.tiempo = int(componentes[0])
        if componentes[1] == "Llega":
            self.tipo = "Llegada"
            self.proceso = Proceso(id=componentes[2], prioridad=componentes[4], tiempoLlegada=self.tiempo)
        elif componentes[1] == "quantum":
            self.tipo = "Quantum"
        elif componentes[1] == "Acaba":
            self.tipo = "Acaba"
            self.proceso = proceso
        elif componentes[1] == "startI/O":
            self.tipo = "StartI/O"
            self.proceso = proceso
        elif componentes[1] == "endI/O":
            self.tipo = "EndI/0"
            self.proceso = proceso
        elif componentes[1] == "endSimulacion":
            self.tipo = "EndSimulacion"
            self.proceso = None
    def getProceso(self):
        return self.proceso

class ColaDeListos:
    def __init__(self):
        self.filaSinPrioridades = []
        self.fila = Q.PriorityQueue()
    def getFila(self):
        return self.fila
    def getFilaIDs(self):
        ids = []
        for proceso in self.fila.queue:
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
    def getListaIds(self):
        ids = []
        for proceso in self.procesos:
            ids.append(proceso.id)
        return ids
    def insertar(self, proceso):
        self.procesos.append(proceso)
    def getProcesoConId(self, id):
        for proceso in self.procesos:
            if proceso.id == id:
                return proceso
        return None
    def removeProceso(self, proceso):
        self.procesos.remove(proceso)


class ProcesosTerminados:
    def __init__(self):
        self.procesos = []
    def getProcesos(self):
        return self.procesos
    def getProcesosIds(self):
        ids = []
        for proceso in self.procesos:
            if proceso != None:
                ids.append(proceso.id)
        return ids
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
        evento.proceso.setTiempoLlegadaCPU(evento.tiempo)
        cpu.insertarProceso(evento.proceso)
    else:
        #Checar si la prioridad del nuevo es mayor a la que esta en el CPU
        proceso_en_cpu = cpu.getProceso()
        proceso_nuevo = evento.proceso
        if proceso_en_cpu.prioridad > proceso_nuevo.prioridad:
            #Nuevo proceso tiene mayor prioridad que el del CPU
            proceso_en_cpu.setTiempoTerminaCPU(evento.tiempo)
            cola_de_listos.insertar(proceso_en_cpu)
            proceso_nuevo.setTiempoLlegadaCPU(evento.tiempo)
            cpu.insertarProceso(proceso_nuevo)
        else:
            #Nuevo proceso tiene menor prioridad al que está en el CPU
            cola_de_listos.insertar(evento.proceso)

def manejarAcaba(evento, cola_de_listos, cpu, procesos_bloqueados, procesos_terminados):
    print(evento.proceso.id)
    proceso_terminado = cpu.getProceso()
    proceso_terminado.setTiempoTerminaCPU(evento.tiempo)
    proceso.setTiempoTerminacion(evento.tiempo)
    cpu.sacarProceso()
    if cola_de_listos.getFila().qsize() != 0:
        proceso_siquiente = cola_de_listos.pop()
        print(proceso_siquiente)
        proceso_siquiente.setTiempoLlegadaCPU(evento.tiempo)
        cpu.insertarProceso(proceso_siquiente)
    procesos_terminados.insertar(proceso_terminado)

def manejarStartIO(evento, cola_de_listos, cpu, procesos_bloqueados, procesos_terminados):
    print(evento.proceso.id)
    ##Sacar procesos del CPU y ponerlo en la lista de procesos bloqueados
    proceso = cpu.getProceso()
    proceso.setTiempoTerminaCPU(evento.tiempo)
    proceso.setStartIO(evento.tiempo)
    cpu.sacarProceso()
    procesos_bloqueados.insertar(proceso)
    if cola_de_listos.getFila().qsize() != 0:
        proceso_siquiente = cola_de_listos.pop()
        print(proceso_siquiente)
        proceso_siquiente.setTiempoLlegadaCPU(evento.tiempo)
        cpu.insertarProceso(proceso_siquiente)
    ##Poner el procesos con mayor prioridad de la cola de listos en el cpu

def manejarEndIO(evento, cola_de_listos, cpu, procesos_bloqueados, procesos_terminados):
    print(evento.proceso.id)
    proceso_terminado_io = procesos_bloqueados.getProcesoConId(evento.proceso.id)
    proceso_terminado_io.setEndIO(evento.tiempo)
    procesos_bloqueados.removeProceso(proceso_terminado_io)
    if cpu.getProceso() == None:
        #No hay proceso en el CPU
        proceso_terminado_io.setTiempoLlegadaCPU(evento.tiempo)
        cpu.insertarProceso(proceso_terminado_io)
    else:
        #Si hay proceso en el cpu
        cola_de_listos.insertar(proceso_terminado_io)




manejadores = {
'Llegada' : manejarLlegada,
'Acaba' : manejarAcaba,
'StartI/O': manejarStartIO,
'EndI/0': manejarEndIO,
'EndSimulacion': None
}

snaps_eventos = []
snaps_cola_de_listos = []
snaps_cpus = []
snaps_bloqueados = []
snaps_terminados = []


procesos = []

while line_index < len(lineas_de_archivo_de_entrada):
    linea = lineas_de_archivo_de_entrada[line_index]
    linea_componentes = linea.split()
    proceso_id = None
    proceso = None
    if len(linea_componentes) >= 3:
        proceso_id = linea_componentes[2]
        for pro in procesos:
            if pro.id == proceso_id:
                proceso = pro

    evento = Evento(texto=linea, proceso=proceso)

    if proceso == None:
        procesos.append(evento.getProceso())

    print("Evento: " , linea)
    funcion = manejadores.get(evento.tipo)
    if funcion != None:
        funcion(evento=evento, cola_de_listos=cola_de_listos, cpu=cpu, procesos_bloqueados=procesos_bloqueados, procesos_terminados=procesos_terminados)
        snaps_eventos.append(evento.texto)
        snaps_cola_de_listos.append(cola_de_listos.getFilaIDs())
        if cpu.getProceso() != None:
            snaps_cpus.append(cpu.getProceso().id)
        else:
            snaps_cpus.append(None)
        snaps_bloqueados.append(procesos_bloqueados.getListaIds())
        snaps_terminados.append(procesos_terminados.getProcesosIds())


    line_index += 1

from texttable import Texttable
t1 = Texttable()
table1_rows = []
table1_rows.append(['Evento', 'Cola de listos', 'CPU', 'Bloqueados', 'Terminados'])
row_index = 0
while row_index < len(snaps_eventos):
    row = []
    row.append(snaps_eventos[row_index])
    row.append(snaps_cola_de_listos[row_index])
    row.append(snaps_cpus[row_index])
    row.append(snaps_bloqueados[row_index])
    row.append(snaps_terminados[row_index])
    table1_rows.append(row)
    row_index += 1

t1.add_rows(table1_rows)
print(t1.draw())

t2 = Texttable()
table2_rows = []
table2_rows.append(['Proceso', 'Tiempo de llegada', 'Tiempo de terminacion', 'Tiempo de CPU', 'Tiempo de espera', 'Turnaround', 'Tiempo de I/0'])

for p in procesos:
    if p != None:
        tiempo_retorno = p.tiempoTerminacion-p.tiempoLlegada
        row = [p.id, p.tiempoLlegada, p.tiempoTerminacion, p.tiempoCPU,tiempo_retorno - p.tiempoCPU - p.tiempoIO, tiempo_retorno, p.tiempoIO]
        table2_rows.append(row)


t2.add_rows(table2_rows)
print(t2.draw())
