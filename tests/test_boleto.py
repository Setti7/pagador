import datetime
from _decimal import Decimal

from boleto.boleto import Boleto


def test_parse_barcode():
    boleto = Boleto.from_barcode("23797404300001240200448056168623793601105800")

    assert boleto.bank_code == 237
    assert boleto.checksum == 7
    assert boleto.currency_code == 9
    assert boleto.due_date_factor == 4043
    assert boleto.raw_value == 124020
    assert boleto.free_field == "0448056168623793601105800"

    assert boleto.value == Decimal("1240.20")
    assert boleto.due_date == datetime.date(2008, 11, 1)


def test_parse_barcode_2():
    boleto = Boleto.from_barcode("34191917700000030561760234433857849034355000")

    assert boleto.bank_code == 341
    assert boleto.checksum == 1
    assert boleto.currency_code == 9
    assert boleto.due_date_factor == 9177
    assert boleto.raw_value == 3056
    assert boleto.free_field == "1760234433857849034355000"

    assert boleto.value == Decimal("30.56")
    assert boleto.due_date == datetime.date(2022, 11, 22)


def test_get_code_from_image():
    code = Boleto.decode_image("tests/fixtures/boleto.png")
    assert ["23791486220000000001111060000000100100022220"] == code


def test_boleto_from_image():
    boletos_from_image = Boleto.from_image("tests/fixtures/boleto.png")

    assert len(boletos_from_image) == 1

    boleto = boletos_from_image[0]

    assert boleto.bank_code == 237
    assert boleto.checksum == 1
    assert boleto.currency_code == 9

    assert boleto.value == Decimal(20_000_000)
    assert boleto.due_date == datetime.date(2011, 1, 29)
