from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List
from datetime import datetime

@dataclass
class Sensor(ABC):
    id: str
    ventana: int = 5
    _calibracion: float = field(default=0.0, repr=False)
    _buffer: list[float] = field(default_factory=list, repr=False)

    def leer(self, valor: float) -> None:
        v = valor + self._calibracion
        self._buffer.append(v)
        if len(self._buffer) > self.ventana:
            self._buffer.pop(0)

    @property
    def promedio(self) -> float:
        return sum(self._buffer)/len(self._buffer) if self._buffer else 0.0

    @abstractmethod
    def en_alerta(self) -> bool:
        pass

@dataclass
class SensorTemperatura(Sensor):
    umbral: float = 80.0

    def en_alerta(self) -> bool:
        return self.promedio >= self.umbral

@dataclass
class SensorVibracion(Sensor):
    rms_umbral: float = 2.5

    def en_alerta(self) -> bool:
        return abs(self.promedio) >= self.rms_umbral

class Notificador(ABC):
    @abstractmethod
    def enviar(self, mensaje: str) -> None:
        pass

class NotificadorEmail(Notificador):
    def __init__(self, destinatario: str):
        self._destinatario = destinatario

    def enviar(self, mensaje: str) -> None:
        print(f"[EMAIL a {self._destinatario}] {mensaje}")

class NotificadorWebhook(Notificador):
    def __init__(self, url: str):
        self._url = url

    def enviar(self, mensaje: str) -> None:
        print(f"[WEBHOOK {self._url}] {mensaje}")

@dataclass
class Alerta:
    id: str
    mensaje: str
    timestamp: datetime

class Logger:
    def log(self, msg: str) -> None:
        print(f"[LOG] {msg}")

class ModuloUI:
    def mostrar(self, alerta: Alerta) -> None:
        print(f"[UI] {alerta.mensaje} (id={alerta.id})")

class GestorAlertas:
    def __init__(self, sensores: List[Sensor], notificadores: List[Notificador]):
        self._sensores = sensores
        self._notificadores = notificadores
        self._alertas: List[Alerta] = []
        self._logger = Logger()
        self._ui = ModuloUI()

    def evaluar_y_notificar(self) -> None:
        for s in self._sensores:
            if s.en_alerta():
                msg = f"ALERTA → Sensor {s.id} en umbral (avg={s.promedio:.2f})"
                alerta = Alerta(id=s.id, mensaje=msg, timestamp=datetime.now())
                self._alertas.append(alerta)
                self._logger.log(msg)
                self._ui.mostrar(alerta)
                for n in self._notificadores:
                    n.enviar(msg)
                    