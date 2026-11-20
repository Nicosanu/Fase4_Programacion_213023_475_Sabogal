from abc import ABC, abstractmethod


class EntidadSistema(ABC):
    def __init__(self, id_entidad):
        if not id_entidad or not str(id_entidad).strip():
            raise ValueError("El identificador de la entidad no puede estar vacío.")
        self._id_entidad = str(id_entidad).strip()

    @property
    def id_entidad(self):
        return self._id_entidad

    @abstractmethod
    def obtener_info(self):
        pass