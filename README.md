# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Proyecto desarrollado para la **Fase 4 - Componente Práctico** del curso **Programación (213023)** de la UNAD.

## Descripción
Aplicación orientada a objetos desarrollada en Python sin uso de bases de datos que gestiona clientes, servicios especializados (salas, alquiler de equipos y asesorías) y reservas mediante listas internas, aplicando abstracción, herencia, polimorfismo, encapsulación, sobrecarga de métodos y manejo robusto de excepciones con registro en logs (`software_fj.log`).

## Estructura del Proyecto
- `src/excepciones.py`: Jerarquía de excepciones personalizadas (`SoftwareFJError`, `DatoInvalidoError`, `ParametroFaltanteError`, `ServicioNoDisponibleError`, `ReservaInvalidaError`, `CalculoInconsistenteError`).
- `src/logs.py`: Configuración del sistema de auditoría y registro en `software_fj.log`.
- `src/entidad.py`: Clase abstracta base `EntidadSistema`.
- `src/cliente.py`: Clase `Cliente` con encapsulación y validaciones estrictas.
- `src/servicios.py`: Clase abstracta `Servicio`, subclases (`ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`) y método sobrecargado `calcular_costo()`.
- `src/reserva.py`: Clase `Reserva` y `GestorSoftwareFJ` con bloques `try/except/else`, `try/except/finally` y encadenamiento de excepciones.
- `src/main.py`: Ejecución de 12 simulaciones completas (válidas e inválidas).

## Ejecución
```bash
python src/main.py