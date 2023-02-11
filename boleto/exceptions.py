class BoletoException(Exception):
    message: str = None

    def __init__(self, message):
        self.message = message


class InvalidBarcode(BoletoException):
    pass
