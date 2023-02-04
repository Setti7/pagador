import datetime
from _decimal import Decimal
from dataclasses import dataclass

from PIL import Image
from pyzbar.pyzbar import decode

from boleto.exceptions import InvalidBarcode


@dataclass(frozen=True)
class Boleto:
    code: str
    bank_code: int
    currency_code: int
    checksum: int
    due_date_factor: int
    raw_value: int
    free_field: str

    @property
    def due_date(self) -> datetime.date:
        return datetime.date(1997, 10, 7) + datetime.timedelta(
            days=self.due_date_factor
        )

    @property
    def value(self) -> Decimal:
        return Decimal(self.raw_value) / 100

    @staticmethod
    def decode_image(path):
        """Returns all Boleto codes from an image."""
        return _decode_image(path)

    @staticmethod
    def from_barcode(data):
        return _parse_barcode(data)

    @staticmethod
    def from_image(path):
        barcodes = _decode_image(path)
        return [_parse_barcode(b) for b in barcodes]


def _decode_image(path: str) -> list[str]:
    return [decoded.data.decode() for decoded in decode(Image.open(path))]


def _parse_barcode(data: str) -> Boleto:
    if len(data) != 44:
        raise InvalidBarcode("Barcode data doesn't have correct length.")

    bank_code = int(data[:3])
    currency_code = int(data[3])
    checksum = int(data[4])
    due_data_factor = int(data[5:9])
    value = int(data[9:19])
    free_field = data[19:44]

    return Boleto(
        code=data,
        bank_code=bank_code,
        checksum=checksum,
        currency_code=currency_code,
        due_date_factor=due_data_factor,
        raw_value=value,
        free_field=free_field,
    )
