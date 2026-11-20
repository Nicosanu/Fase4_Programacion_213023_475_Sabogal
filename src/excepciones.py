class SoftwareFJError(Exception):
    pass


class DatoInvalidoError(SoftwareFJError):
    pass


class ParametroFaltanteError(SoftwareFJError):
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    pass


class ReservaInvalidaError(SoftwareFJError):
    pass


class CalculoInconsistenteError(SoftwareFJError):
    pass