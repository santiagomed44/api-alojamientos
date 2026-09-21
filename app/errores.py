class ErrorAPI(Exception):
    """Error controlado de la API."""

    def __init__(self, mensaje, status_code=400, codigo=None):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.status_code = status_code
        self.codigo = codigo