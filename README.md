El objetivo de este codigo es mostrar los 4 pilares de POO.

Para probar que el codigo funcione solo se necesita ejecutar el script `4_pilares.py`.

Diagrama del programa:
![alt text](<Untitled diagram _ Mermaid Chart-2025-08-30-043117.png>)

Codigo del diagrama UML realizado como evidencia del programa:
```
classDiagram
        Sensor <|-- "Generalizacion" SensorTemperatura
        Sensor <|-- "Generalizacion" SensorVibracion
        Notificador <|.. "Implementa" NotificadorEmail
        Notificador <|.. "Implementa" NotificadorWebhook
        GestorAlertas *-- "Composicion" Sensor
        GestorAlertas *-- "Composicion" Notificador
        GestorAlertas o-- "Agregacion" Alerta
        GestorAlertas ..> "Dependencia" Logger
        GestorAlertas --> "Asociacion" ModuloUI

        class Sensor {
            <<Abstract>>
            +str : id
            +int : ventana
            -float : _calibracion
            -list[float] : _buffer
            +float : promedio
            +leer(valor : float)
            +en_alerta() : bool*
        }
        class GestorAlertas {
            -List[Sensor] : _sensores
            -List[Notificador] : _notificadores
            -List[Alerta] : _alertas
            -Logger : _logger
            -ModuloUI : _ui
            +evaluar_y_notificar() : void
        }
        class SensorVibracion {
            +float : rms_umbral = 2.5
            +en_alerta() : bool*
        }
        class SensorTemperatura {
            +float : umbral = 80.0
            +en_alerta() : bool*
        }
        class NotificadorWebhook {
            -str : _url
            +enviar(mensaje : str) : void
        }
        class NotificadorEmail {
            -str : _destinatario
            +enviar(mensaje : str) : void
        }
        class Notificador {
            +enviar(mensaje : str) : void
        }
        class Alerta {
            +str : id
            +str : mensaje
            +datetime : timestamp
        }
        class Logger {
            +log(msg : str) : void
        }
        class ModuloUI {
            +mostrar(alerta : Alerta) : void
        }
```