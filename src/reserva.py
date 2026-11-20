from excepciones import (
    DatoInvalidoError,
    ParametroFaltanteError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    SoftwareFJError,
)


class Reserva:
    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA")

    def __init__(self, id_reserva, cliente, servicio, duracion, descuento=0.0, recargo=0.0):
        if not id_reserva or not str(id_reserva).strip():
            raise ParametroFaltanteError("El ID de la reserva es obligatorio.")
        if cliente is None or servicio is None:
            raise ParametroFaltanteError("La reserva requiere un cliente y un servicio válidos.")
        if duracion <= 0:
            raise DatoInvalidoError("La duración de la reserva debe ser mayor a cero.")

        self.id_reserva = str(id_reserva).strip()
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.descuento = descuento
        self.recargo = recargo
        self.estado = "PENDIENTE"
        self.costo_total = 0.0

    def confirmar(self, logger):
        try:
            if self.estado == "CANCELADA":
                raise ReservaInvalidaError(f"La reserva {self.id_reserva} está cancelada y no puede confirmarse.")
            if not self.servicio.disponible:
                raise ServicioNoDisponibleError(f"El servicio '{self.servicio._nombre_servicio}' no está disponible.")

            self.costo_total = self.servicio.calcular_costo(
                self.duracion, descuento=self.descuento, recargo=self.recargo
            )
        except SoftwareFJError as e:
            logger.error(f"Fallo al confirmar reserva {self.id_reserva}: {e}")
            raise ReservaInvalidaError(f"No se pudo confirmar la reserva {self.id_reserva}") from e
        else:
            self.estado = "CONFIRMADA"
            self.servicio.disponible = False
            logger.info(
                f"Reserva {self.id_reserva} CONFIRMADA para {self.cliente.nombre} | Total: ${self.costo_total}"
            )

    def procesar(self, logger):
        bloqueo_auditoria = True
        try:
            if self.estado != "CONFIRMADA":
                raise ReservaInvalidaError(
                    f"La reserva {self.id_reserva} debe estar CONFIRMADA antes de procesarse (estado actual: {self.estado})."
                )
            self.estado = "PROCESADA"
            logger.info(f"Reserva {self.id_reserva} PROCESADA exitosamente ({self.servicio.describir_servicio()}).")
        except SoftwareFJError as e:
            logger.error(f"Error procesando reserva {self.id_reserva}: {e}")
            raise
        finally:
            bloqueo_auditoria = False
            logger.info(f"Auditoría de cierre ejecutada para reserva {self.id_reserva} (bloqueo={bloqueo_auditoria}).")

    def cancelar(self, logger):
        try:
            if self.estado == "PROCESADA":
                raise ReservaInvalidaError(f"No se puede cancelar la reserva {self.id_reserva} porque ya fue procesada.")
            if self.estado == "CANCELADA":
                raise ReservaInvalidaError(f"La reserva {self.id_reserva} ya se encontraba cancelada.")
        except SoftwareFJError as e:
            logger.error(f"Error al cancelar reserva {self.id_reserva}: {e}")
            raise
        else:
            self.estado = "CANCELADA"
            self.servicio.disponible = True
            logger.info(f"Reserva {self.id_reserva} CANCELADA correctamente y servicio liberado.")


class GestorSoftwareFJ:
    def __init__(self, logger):
        self.logger = logger
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, cliente):
        self.clientes.append(cliente)
        self.logger.info(f"Cliente registrado: {cliente.obtener_info()}")

    def registrar_servicio(self, servicio):
        self.servicios.append(servicio)
        self.logger.info(f"Servicio registrado: {servicio.obtener_info()}")

    def registrar_reserva(self, reserva):
        self.reservas.append(reserva)
        self.logger.info(f"Reserva creada en estado {reserva.estado}: ID {reserva.id_reserva}")