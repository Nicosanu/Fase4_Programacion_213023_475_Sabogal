from logs import configurar_logger
from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva, GestorSoftwareFJ
from excepciones import SoftwareFJError


def ejecutar_simulaciones():
    logger = configurar_logger()
    sistema = GestorSoftwareFJ(logger)
    logger.info("=== INICIO DE SIMULACIONES SISTEMA INTEGRAL SOFTWARE FJ ===")

    # SIMULACIÓN 1 (Válida): Registro correcto de Cliente 1
    try:
        c1 = Cliente("C001", "Carlos Ramírez", "carlos.ramirez@correo.com", "3104567890")
        sistema.registrar_cliente(c1)
    except SoftwareFJError as e:
        logger.error(f"[Simulación 1] Error inesperado: {e}")

    # SIMULACIÓN 2 (Válida): Registro correcto de Cliente 2
    try:
        c2 = Cliente("C002", "Laura Gómez", "laura.gomez@empresa.co", "3209876543")
        sistema.registrar_cliente(c2)
    except SoftwareFJError as e:
        logger.error(f"[Simulación 2] Error inesperado: {e}")

    # SIMULACIÓN 3 (Inválida): Cliente con nombre faltante (ParametroFaltanteError)
    try:
        c_invalido1 = Cliente("C003", "   ", "sin.nombre@correo.com", "3001112233")
        sistema.registrar_cliente(c_invalido1)
    except SoftwareFJError as e:
        logger.error(f"[Simulación 3 - Controlada] Error registrando cliente: {e}")

    # SIMULACIÓN 4 (Inválida): Cliente con correo inválido (DatoInvalidoError)
    try:
        c_invalido2 = Cliente("C004", "Andrés López", "andres_correo_malo", "3004445566")
        sistema.registrar_cliente(c_invalido2)
    except SoftwareFJError as e:
        logger.error(f"[Simulación 4 - Controlada] Error registrando cliente: {e}")

    # SIMULACIÓN 5 (Válida): Creación de servicio ReservaSala
    try:
        s1 = ReservaSala("S001", "Sala Ejecutiva Norte", 80000, capacidad=12)
        sistema.registrar_servicio(s1)
    except SoftwareFJError as e:
        logger.error(f"[Simulación 5] Error inesperado: {e}")

    # SIMULACIÓN 6 (Válida): Creación de servicio AlquilerEquipo
    try:
        s2 = AlquilerEquipo("S002", "Estación WorkStation Pro", 45000, cantidad_equipos=4)
        sistema.registrar_servicio(s2)
    except SoftwareFJError as e:
        logger.error(f"[Simulación 6] Error inesperado: {e}")

    # SIMULACIÓN 7 (Válida): Creación de servicio AsesoriaEspecializada
    try:
        s3 = AsesoriaEspecializada("S003", "Consultoría Cloud", 120000, especialidad="Arquitectura AWS")
        sistema.registrar_servicio(s3)
    except SoftwareFJError as e:
        logger.error(f"[Simulación 7] Error inesperado: {e}")

    # SIMULACIÓN 8 (Inválida): Servicio con tarifa negativa (DatoInvalidoError)
    try:
        s_invalido = ReservaSala("S004", "Sala Fantasma", -50000, capacidad=5)
        sistema.registrar_servicio(s_invalido)
    except SoftwareFJError as e:
        logger.error(f"[Simulación 8 - Controlada] Error creando servicio: {e}")

    # SIMULACIÓN 9 (Válida): Reserva exitosa con cálculo sobrecargado (descuento y recargo) y procesamiento
    try:
        r1 = Reserva("R001", c1, s1, duracion=3, descuento=0.10, recargo=15000)
        sistema.registrar_reserva(r1)
        r1.confirmar(logger)
        r1.procesar(logger)
    except SoftwareFJError as e:
        logger.error(f"[Simulación 9] Error en reserva R001: {e}")

    # SIMULACIÓN 10 (Inválida): Intento de reservar un servicio que ya no está disponible (Encadenamiento)
    try:
        r2 = Reserva("R002", c2, s1, duracion=2)
        sistema.registrar_reserva(r2)
        r2.confirmar(logger)
    except SoftwareFJError as e:
        logger.error(f"[Simulación 10 - Controlada] Excepción encadenada capturada: {e} | Causa: {e.__cause__}")

    # SIMULACIÓN 11 (Inválida): Cálculo inconsistente por descuento >= 100% (CalculoInconsistenteError)
    try:
        r3 = Reserva("R003", c2, s2, duracion=2, descuento=1.5)
        sistema.registrar_reserva(r3)
        r3.confirmar(logger)
    except SoftwareFJError as e:
        logger.error(f"[Simulación 11 - Controlada] Excepción encadenada capturada: {e} | Causa: {e.__cause__}")

    # SIMULACIÓN 12 (Válida e Inválida): Reserva válida, cancelación controlada e intento de reconfirmar cancelada
    try:
        r4 = Reserva("R004", c2, s3, duracion=4)
        sistema.registrar_reserva(r4)
        r4.confirmar(logger)
        r4.cancelar(logger)
        r4.confirmar(logger)
    except SoftwareFJError as e:
        logger.error(f"[Simulación 12 - Controlada] Intento inválido tras cancelación: {e} | Causa: {e.__cause__}")

    logger.info(
        f"=== FIN DE SIMULACIONES | Clientes: {len(sistema.clientes)} | Servicios: {len(sistema.servicios)} | Reservas: {len(sistema.reservas)} ==="
    )


if __name__ == "__main__":
    ejecutar_simulaciones()