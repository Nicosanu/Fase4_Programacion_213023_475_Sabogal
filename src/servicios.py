from abc import abstractmethod
from entidad import EntidadSistema
from excepciones import (
    DatoInvalidoError,
    ParametroFaltanteError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError,
)


class Servicio(EntidadSistema):
    def __init__(self, id_servicio, nombre_servicio, tarifa_base, disponible=True):
        try:
            super().__init__(id_servicio)
        except ValueError as e:
            raise ParametroFaltanteError("El ID del servicio es obligatorio.") from e

        if not nombre_servicio or not str(nombre_servicio).strip():
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")
        if tarifa_base <= 0:
            raise DatoInvalidoError("La tarifa base debe ser mayor que cero.")

        self._nombre_servicio = str(nombre_servicio).strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = bool(disponible)
        self.validar_parametros()

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, estado):
        self._disponible = bool(estado)

    @abstractmethod
    def validar_parametros(self):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass

    def calcular_costo(self, duracion, descuento=0.0, impuesto=0.19, recargo=0.0):
        if duracion <= 0:
            raise DatoInvalidoError("La duración para calcular el costo debe ser mayor a cero.")
        if descuento < 0 or descuento >= 1:
            raise CalculoInconsistenteError(f"Descuento fuera de rango permitido (0 a 0.99): {descuento}")
        if impuesto < 0 or recargo < 0:
            raise CalculoInconsistenteError("Los impuestos y recargos no pueden ser negativos.")

        subtotal = (self._tarifa_base * duracion) + recargo
        monto_descuento = subtotal * descuento
        total = (subtotal - monto_descuento) * (1 + impuesto)

        if total <= 0:
            raise CalculoInconsistenteError("El costo total calculado es inconsistente (menor o igual a cero).")
        return round(total, 2)

    def obtener_info(self):
        estado = "Disponible" if self._disponible else "No disponible"
        return f"[{self.id_entidad}] {self._nombre_servicio} - Tarifa: ${self._tarifa_base}/h ({estado})"


class ReservaSala(Servicio):
    def __init__(self, id_servicio, nombre_servicio, tarifa_base, capacidad, disponible=True):
        self.capacidad = capacidad
        super().__init__(id_servicio, nombre_servicio, tarifa_base, disponible)

    def validar_parametros(self):
        if self.capacidad <= 0:
            raise DatoInvalidoError("La capacidad de la sala debe ser mayor a 0 personas.")

    def describir_servicio(self):
        return f"Sala '{self._nombre_servicio}' con capacidad para {self.capacidad} personas."


class AlquilerEquipo(Servicio):
    def __init__(self, id_servicio, nombre_servicio, tarifa_base, cantidad_equipos, disponible=True):
        self.cantidad_equipos = cantidad_equipos
        super().__init__(id_servicio, nombre_servicio, tarifa_base, disponible)

    def validar_parametros(self):
        if self.cantidad_equipos <= 0:
            raise DatoInvalidoError("La cantidad de equipos a alquilar debe ser al menos 1.")

    def describir_servicio(self):
        return f"Alquiler de {self.cantidad_equipos} unidad(es) de '{self._nombre_servicio}'."


class AsesoriaEspecializada(Servicio):
    def __init__(self, id_servicio, nombre_servicio, tarifa_base, especialidad, disponible=True):
        self.especialidad = especialidad
        super().__init__(id_servicio, nombre_servicio, tarifa_base, disponible)

    def validar_parametros(self):
        if not self.especialidad or not str(self.especialidad).strip():
            raise ParametroFaltanteError("Debe indicar la especialidad de la asesoría.")

    def describir_servicio(self):
        return f"Asesoría técnica en '{self.especialidad}' ({self._nombre_servicio})."