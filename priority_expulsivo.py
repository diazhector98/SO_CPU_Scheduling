import queue as Q
from texttable import Texttable

"""
Definición de la clase de Proceso

Se hara un objeto de esta clase por cada proceso de la simulación
"""
class Proceso:
    def __init__(self, id, prioridad, tiempoLlegada):
        #El id del proceso, un caracter
        self.id = id
        #La prioridad del proceso, un numero entre 1 y 5
        self.prioridad = prioridad
        #El tiempo de llegada o el tiempo en que se crea el proceso
        self.tiempoLlegada = tiempoLlegada
        #Tiempo en que acaba el proceso, calculado después
        self.tiempoTerminacion = 0
        self.tiempoCPU = 0
        self.tiempoEspera = 0
        self.turnaround = 0
        #Total de tiempo en que el proceso estuvo bloqueado
        self.tiempoIO = 0
        return

    """
    Método de la clase para comparar 'valor' entre dos objetos de la clase Proceso
    Este método se utiliza para la cola priorizada(Priority Queue) de la cola de listos
    """
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


"""
Definición de la clase Evento

Se hará un objeto de esta clase por cada evento en el log de entrada.
Lo importante de esta clase es que almacene el tipo de evento,
el timestamp y el proceso relacionado
"""
class Evento:
    def __init__(self, texto, proceso):
        #El texto tal cual del evento como viene en el archivo de entrada
        self.texto = texto
        #El proceso asociado con el evento, es nulo si es el de terminar simulacion
        self.proceso = None
        #El tiempo(entero) en que llego el evento
        self.tiempo = None
        #El tipo de evento que es: Llegada, Acaba, Quantum, Start y End IO, o termino de Simulación
        self.tipo = None
        componentes = texto.split()
        if len(componentes) == 1:
            return
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
            self.tipo = "EndI/O"
            self.proceso = proceso
        elif componentes[1] == "endSimulacion":
            self.tipo = "EndSimulacion"
            self.proceso = None
    def getProceso(self):
        return self.proceso

"""
Definición de la clase de la Cola de listos

Solo habra un objeto de esta clase que mantenga las colas/filas de los Procesos
en la cola de listos.
Tiene dos atributos esta clase, una cola priorizada que contiene objetos de
tipo Proceso, y un arreglo que solo contiene los IDs (Esto para que sea más sencillo
verificar la existencia de un proceso y de imprimirla a la consola),
"""
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
        #Se quita el proceso más enfrente de la fila priorizada y se regresa
        proceso = self.fila.get()
        #Se quita el proceso id también de la lista de IDs
        for p in self.filaSinPrioridades:
            if p == proceso:
                self.filaSinPrioridades.remove(p)
        return proceso

    #Método para checar si un proceso está en la cola de Listos
    #Utilizado para checar si tenemos un log válido
    #Y utilizado para saber cómo manejar cuando un proceso Acaba
    def estaProceso(self, proceso):
        for p in self.filaSinPrioridades:
            if p == proceso:
                return True
        return False
    def quitarTodosLosProcesosDeLaColaPriorizada(self):
        while not self.fila.empty():
            self.fila.get(False)
    def quitarProceso(self, proceso):
        if self.estaProceso(proceso):
            index = 0
            while self.filaSinPrioridades[index] != proceso:
                index += 1
            self.filaSinPrioridades.pop(index)
            self.quitarTodosLosProcesosDeLaColaPriorizada()
            for p in self.filaSinPrioridades:
                self.fila.put(p)


"""
Definición de la clase de CPU

Es una clase para aumentar el entendimiento de los componentes visualizados.
Solo habrá una instancia de ella
Solo tiene un atributo: el proceso que esta actualmente en el CPU(puede ser nulo si no hay)
"""
class CPU:
    def __init__(self):
        self.proceso = None
    def getProceso(self):
        return self.proceso
    def insertarProceso(self, proceso):
        self.proceso = proceso
    def sacarProceso(self):
        self.proceso = None

"""
Definicion de la clase de ProcesosBloqueados


Solo habrá una instancia de esta clase que represente
la lista de procesos bloqueados por I/O.
El único atributo es un arreglo de los procesos contenidos en ella.

"""
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
    def estaProceso(self, proceso):
        for p in self.procesos:
            if p == proceso:
                return True
        return False

"""
Definición de la clase de ProcesosTerminados

Igual que la clase de ProcesosBloqueados,
pero solo contiene procesos que ya acabaron

"""

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

"""
Método en donde se maneja un tipo de evento en el que llega/se crea un proceso nuevo
"""
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
"""
Método en donde se maneja un tipo de evento en el que acaba un proceso y
pasa a procesos terminados
"""
def manejarAcaba(evento, cola_de_listos, cpu, procesos_bloqueados, procesos_terminados):
    proceso = evento.proceso
    if cola_de_listos.estaProceso(proceso):
        print("Proceso acabado esta en Cola de Listos")
        proceso.setTiempoTerminacion(evento.tiempo)
        cola_de_listos.quitarProceso(proceso)
    elif procesos_bloqueados.estaProceso(proceso):
        print("Proceso acabado esta en procesos bloqueados(En I/0)")
        proceso.setTiempoTerminacion(evento.tiempo)
        proceso.setEndIO(evento.tiempo)
        procesos_bloqueados.removeProceso(proceso_terminado_io)
    else:
        proceso_terminado = cpu.getProceso()
        proceso_terminado.setTiempoTerminaCPU(evento.tiempo)
        proceso.setTiempoTerminacion(evento.tiempo)
        cpu.sacarProceso()
        if cola_de_listos.getFila().qsize() != 0:
            proceso_siquiente = cola_de_listos.pop()
            proceso_siquiente.setTiempoLlegadaCPU(evento.tiempo)
            cpu.insertarProceso(proceso_siquiente)
    procesos_terminados.insertar(proceso)

"""
Método en donde se maneja un tipo de evento en el que un proceso empieza su I/O
y pasa a los ProcesosBloqueados
"""
def manejarStartIO(evento, cola_de_listos, cpu, procesos_bloqueados, procesos_terminados):
    ##Sacar procesos del CPU y ponerlo en la lista de procesos bloqueados

    proceso = cpu.getProceso()
    if proceso != evento.proceso:
        return
    proceso.setTiempoTerminaCPU(evento.tiempo)
    proceso.setStartIO(evento.tiempo)
    cpu.sacarProceso()
    procesos_bloqueados.insertar(proceso)
    if cola_de_listos.getFila().qsize() != 0:
        proceso_siquiente = cola_de_listos.pop()
        proceso_siquiente.setTiempoLlegadaCPU(evento.tiempo)
        cpu.insertarProceso(proceso_siquiente)
    ##Poner el procesos con mayor prioridad de la cola de listos en el cpu

"""
Método en donde se maneja un tipo de evento en el que un proceso termina su I/O
y sale de la lista de bloqueados
"""
def manejarEndIO(evento, cola_de_listos, cpu, procesos_bloqueados, procesos_terminados):
    if not procesos_bloqueados.estaProceso(evento.proceso):
        return
    proceso_terminado_io = procesos_bloqueados.getProcesoConId(evento.proceso.id)
    proceso_terminado_io.setEndIO(evento.tiempo)
    procesos_bloqueados.removeProceso(proceso_terminado_io)
    if cpu.getProceso() == None:
        #No hay proceso en el CPU
        proceso_terminado_io.setTiempoLlegadaCPU(evento.tiempo)
        cpu.insertarProceso(proceso_terminado_io)
    elif cpu.getProceso().prioridad > proceso_terminado_io.prioridad:
        #Si hay proceso en el cpu pero es de prioridad menor
        proceso_en_cpu = cpu.getProceso()
        proceso_en_cpu.setTiempoTerminaCPU(evento.tiempo)
        cpu.sacarProceso()
        cpu.insertarProceso(proceso_terminado_io)
        proceso_terminado_io.setTiempoLlegadaCPU(evento.tiempo)
        cola_de_listos.insertar(proceso_en_cpu)
    else:
        #Si hay proceso en CPU, pero su prioridad es mayor, entonces se va a la cola de listos
        cola_de_listos.insertar(proceso_terminado_io)



"""
Método en donde se regresa la respuesta del simulador dependiendo del tipo de evento
que se recibe.
"""
def obtenerRspuestaDelSimulador(evento):
    if evento.tipo == "Llegada":
        return "proceso " + evento.proceso.id + " creado"
    elif evento.tipo == "Acaba":
        return "Proceso " + evento.proceso.id + " terminado"
    elif evento.tipo == "StartI/O":
        return "Proceso " + evento.proceso.id + " startI/0"
    elif evento.tipo == "EndI/O":
        return "Proceso " + evento.proceso.id + " endI/0"

    return "Wut"

"""
Método en donde se imprime un renglon de una tabla
con el estado de la cola de listos, el cpu, los procesos Bloqueados
y terminados en el momento del time del evento
"""
def imprimirSnap(evento, snap_cola_de_listos, cpu, snap_bloqueados, snap_terminados):
    print(evento.texto)
    print("\t", obtenerRspuestaDelSimulador(evento=evento))
    table = Texttable()
    rows = []
    cpu_text = cpu.getProceso().id if cpu.getProceso() != None else "-"
    rows.append(['Evento', 'Cola de listos', 'CPU', 'Bloqueados', 'Terminados'])
    rows.append([evento.texto, snap_cola_de_listos, cpu_text, snap_bloqueados, snap_terminados])
    table.add_rows(rows)
    print(table.draw())


"""
Un diccionario de funciones a la cuál se hará referencia dependiendo
del tipo de evento que se está manejando
"""
manejadores = {
'Llegada' : manejarLlegada,
'Acaba' : manejarAcaba,
'StartI/O': manejarStartIO,
'EndI/O': manejarEndIO,
'EndSimulacion': None
}

"""
Función principal del algoritmo de priority expulsivo que
recibe cómo parametro una arreglo de los renglones
que se reciben en el archivo de entrada


Se procesa cada evento y al final se imprime una tabla
con el resumen de todos los eventos
y un tabla con el resumen de todos los procesos
"""
def priority_expulsivo(lineas_de_archivo_de_entrada):
        line_index = 0
        algoritmo = lineas_de_archivo_de_entrada[line_index]
        algoritmo = algoritmo.replace("\n", "")
        line_index += 1
        quantum = lineas_de_archivo_de_entrada[line_index]
        line_index += 1

        cola_de_listos = ColaDeListos()
        cpu = CPU()
        procesos_bloqueados = ProcesosBloqueados()
        procesos_terminados = ProcesosTerminados()

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
            funcion = manejadores.get(evento.tipo)
            if funcion != None:
                funcion(evento=evento, cola_de_listos=cola_de_listos, cpu=cpu, procesos_bloqueados=procesos_bloqueados, procesos_terminados=procesos_terminados)
                snaps_eventos.append(evento.texto)
                snap_cola_de_listos = cola_de_listos.getFilaIDs()
                snap_cola_de_listos.reverse()
                snaps_cola_de_listos.append(snap_cola_de_listos)
                if cpu.getProceso() != None:
                    snaps_cpus.append(cpu.getProceso().id)
                else:
                    snaps_cpus.append(None)
                snaps_bloqueados.append(procesos_bloqueados.getListaIds())
                snaps_terminados.append(procesos_terminados.getProcesosIds())
                imprimirSnap(
                evento=evento,
                snap_cola_de_listos=cola_de_listos.getFilaIDs(),
                cpu=cpu,
                snap_bloqueados=procesos_bloqueados.getListaIds(),
                snap_terminados=procesos_terminados.getProcesosIds()
                )


            line_index += 1

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
