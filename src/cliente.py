from entidad import EntidadSistema
from excepciones import DatoInvalidoError, ParametroFaltanteError


class Cliente(EntidadSistema):
    def __init__(self, id_cliente, nombre, correo, telefono):
        try:
            super().__init__(id_cliente)
        except ValueError as e:
            raise ParametroFaltanteError("El ID del cliente es obligatorio.") from e

        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not str(valor).strip():
            raise ParametroFaltanteError("El nombre del cliente es obligatorio.")
        self.__nombre = str(valor).strip()

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not valor or "@" not in str(valor) or "." not in str(valor):
            raise DatoInvalidoError(f"Correo electrónico inválido: {valor}")
        self.__correo = str(valor).strip()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        telefono_str = str(valor).strip()
        if not telefono_str.isdigit() or len(telefono_str) < 7:
            raise DatoInvalidoError(f"Teléfono inválido (debe tener al menos 7 dígitos): {valor}")
        self.__telefono = telefono_str

    def obtener_info(self):
        return f"Cliente [{self.id_entidad}]: {self.__nombre} | Correo: {self.__correo} | Tel: {self.__telefono}"