from datetime import datetime

    
class Collection():
    """Clase que representa una colección de usuarios,
      cada uno con un conjunto de posts, a perfilar."""

    def __init__(
        self,
        nombre: str,
        algoritmo: str,
        id: str = None,
        tiempo: int = None,
        users: list[dict] = None,
    ) -> None:
        self.id = id
        self.nombre = nombre
        self.algoritmo = algoritmo
        self.fecha_creacion = datetime.now().timestamp()
        self.tiempo = tiempo
        self.users = users
