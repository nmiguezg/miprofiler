class NotSupportedAlgorithmException(Exception):
    def __init__(self, algoritmo):
        mensaje = f"El algoritmo de perfilado seleccionado no está disponible: {algoritmo}"
        super().__init__(mensaje)
