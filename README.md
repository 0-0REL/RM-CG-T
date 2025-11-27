# Robot con seguimieto de mano
Usa MyCobot280:
[Python API](https://github.com/elephantrobotics/pymycobot/blob/main/docs/MyCobot_280_en.md)

## Carpetas

| | Contenido |
|-|-----------|
| [dev](./dev/) | Modulos de prueba, archivos independientes |
| [matlab](./matlab/) | Calculos con matlab |
| [myCobot](./myCobot/) | - Modelo para simulación <br> - Modelo CAD <br> - STL del modelo CAD |
| [src](./src/) | Implementación funcional |

## Uso

```bash
# Intalar requerimietos
python3 -m pip install -r requirements.txt
```

### Iniciar

```bash
# Obtener coordenadas de la mano
python hand_coord.py
# Mover el robot
python mycobot_control.py
```

### Simulación

```bash
python hand_coord.py
# En mycobot_control.py en la clase robot seleccionar modo 3 o 4
python mycobot_control.py
# Abrir coppeliaSim y cargar escena
# Inicia simulación desde dev/robot/sim/
python simMyCobot.py
```

Todos los programas se comunican por tcp local, puerto 5556 para control del robot y 5557 para simulación