import datetime
from unittest import TestCase, main
from _decimal import Decimal

from boleto.boleto import Boleto


class TestParsing(TestCase):
    def test_parse_barcode(self):
        boleto = Boleto.from_barcode("23797404300001240200448056168623793601105800")

        self.assertEqual(boleto.bank_code, 237)
        self.assertEqual(boleto.checksum, 7)
        self.assertEqual(boleto.currency_code, 9)
        self.assertEqual(boleto.due_date_factor, 4043)
        self.assertEqual(boleto.raw_value, 124020)
        self.assertEqual(boleto.free_field, "0448056168623793601105800")

        self.assertEqual(boleto.value, Decimal("1240.20"))
        self.assertEqual(boleto.due_date, datetime.date(2008, 11, 1))

    def test_parse_barcode_2(self):
        boleto = Boleto.from_barcode("34191917700000030561760234433857849034355000")

        self.assertEqual(boleto.bank_code, 341)
        self.assertEqual(boleto.checksum, 1)
        self.assertEqual(boleto.currency_code, 9)
        self.assertEqual(boleto.due_date_factor, 9177)
        self.assertEqual(boleto.raw_value, 3056)
        self.assertEqual(boleto.free_field, "1760234433857849034355000")

        self.assertEqual(boleto.value, Decimal("30.56"))
        self.assertEqual(boleto.due_date, datetime.date(2022, 11, 22))

    def test_get_code_from_image(self):
        code = Boleto.decode_image("fixtures/boleto.png")
        self.assertEqual(["23791486220000000001111060000000100100022220"], code)

    def test_boleto_from_image(self):
        boletos_from_image = Boleto.from_image("fixtures/boleto.png")

        self.assertEqual(len(boletos_from_image), 1)

        boleto = boletos_from_image[0]

        self.assertEqual(boleto.bank_code, 237)
        self.assertEqual(boleto.checksum, 1)
        self.assertEqual(boleto.currency_code, 9)

        self.assertEqual(boleto.value, Decimal(20_000_000))
        self.assertEqual(boleto.due_date, datetime.date(2011, 1, 29))


if __name__ == "__main__":
    main()
