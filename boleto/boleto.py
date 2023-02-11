import datetime
from _decimal import Decimal
from dataclasses import dataclass

from PIL.Image import Image
from pdf2image import convert_from_bytes
from pyzbar.pyzbar import decode
from pyzbar.wrapper import ZBarSymbol

from boleto.exceptions import InvalidBarcode


@dataclass(frozen=True)
class Boleto:
    barcode: str
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
    def from_barcode(value: str):
        return _parse_barcode(value)

    @staticmethod
    def from_image(image: Image):
        barcodes = _get_barcodes_from_image(image)
        return [_parse_barcode(b) for b in barcodes]

    @staticmethod
    def from_pdf(pdf: bytes):
        images = convert_from_bytes(pdf)
        for img in images:
            return Boleto.from_image(img)


def _get_barcodes_from_image(image: Image) -> list[str]:
    a = [decoded for decoded in decode(image, symbols=[ZBarSymbol.I25])]
    return [i.data.decode() for i in a]


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
        barcode=data,
        bank_code=bank_code,
        checksum=checksum,
        currency_code=currency_code,
        due_date_factor=due_data_factor,
        raw_value=value,
        free_field=free_field,
    )
