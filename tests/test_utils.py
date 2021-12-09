import unittest

import badge_creator.utils

class TestRgbColor(unittest.TestCase):
    def test_constructor(self):
        subject = badge_creator.utils.RgbColor(0xFE, 0xDC, 0xBA)
        self.assertEqual(subject.red, 0xFE)
        self.assertEqual(subject.green, 0xDC)
        self.assertEqual(subject.blue, 0xBA)

        subject = badge_creator.utils.RgbColor(0x00, 0x01, 0x02)
        self.assertEqual(subject.red, 0x00)
        self.assertEqual(subject.green, 0x01)
        self.assertEqual(subject.blue, 0x02)

    def test_constructor_invalid(self):
        try:
            badge_creator.utils.RgbColor(0xFE, 0xDC, 0x100)
            self.fail()
        except ValueError as e:
            self.assertEqual(e.__str__(), "Color component blue must be and int between 0 and 255 inclusive but was 256 of type <class 'int'>")

        try:
            badge_creator.utils.RgbColor(0xFE, -1, 0xBA)
            self.fail()
        except ValueError as e:
            self.assertEqual(e.__str__(), "Color component green must be and int between 0 and 255 inclusive but was -1 of type <class 'int'>")

        try:
            badge_creator.utils.RgbColor(128.0, 0xDC, 0xBA)
            self.fail()
        except ValueError as e:
            self.assertEqual(e.__str__(), "Color component red must be and int between 0 and 255 inclusive but was 128.0 of type <class 'float'>")

    def test_multiply(self):
        subject = badge_creator.utils.RgbColor(3, 5, 7).multiply(11)
        self.assertEqual(subject.red, 33)
        self.assertEqual(subject.green, 55)
        self.assertEqual(subject.blue, 77)

        subject = badge_creator.utils.RgbColor(3, 5, 7).multiply(0.5)
        self.assertEqual(subject.red, 2)
        self.assertEqual(subject.green, 3)
        self.assertEqual(subject.blue, 4)

    def test_multiply_clamped(self):
        subject = badge_creator.utils.RgbColor(3, 5, 7).multiply(50)
        self.assertEqual(subject.red, 150)
        self.assertEqual(subject.green, 250)
        self.assertEqual(subject.blue, 255)

        subject = badge_creator.utils.RgbColor(9, 7, 5).multiply(50)
        self.assertEqual(subject.red, 255)
        self.assertEqual(subject.green, 255)
        self.assertEqual(subject.blue, 250)

        subject = badge_creator.utils.RgbColor(9, 7, 5).multiply(-1)
        self.assertEqual(subject.red, 0)
        self.assertEqual(subject.green, 0)
        self.assertEqual(subject.blue, 0)

    def test_multiply_invalidType(self):
        try:
            badge_creator.utils.RgbColor(3, 5, 7).multiply('hello')
        except ValueError as e:
            self.assertEqual(e.__str__(), "Can only multiply a color by a number but hello of type <class 'str'> was used.")

    def test_add(self):
        subject = badge_creator.utils.RgbColor(3, 5, 7).add(badge_creator.utils.RgbColor(4, 6, 8))
        self.assertEqual(subject.red, 7)
        self.assertEqual(subject.green, 11)
        self.assertEqual(subject.blue, 15)

    def test_add_clamp(self):
        subject = badge_creator.utils.RgbColor(254, 5, 7).add(badge_creator.utils.RgbColor(4, 6, 251))
        self.assertEqual(subject.red, 255)
        self.assertEqual(subject.green, 11)
        self.assertEqual(subject.blue, 255)

    def test_add_invalidType(self):
        try:
            badge_creator.utils.RgbColor(3, 5, 7).add(5)
        except ValueError as e:
            self.assertEqual(e.__str__(), "Can only add a color from another color but 5 of type <class 'int'> was used.")

    def test_substract(self):
        subject = badge_creator.utils.RgbColor(4, 6, 8).subtract(badge_creator.utils.RgbColor(3, 4, 5))
        self.assertEqual(subject.red, 1)
        self.assertEqual(subject.green, 2)
        self.assertEqual(subject.blue, 3)

    def test_substract_clamp(self):
        subject = badge_creator.utils.RgbColor(3, 4, 5).subtract(badge_creator.utils.RgbColor(4, 6, 8))
        self.assertEqual(subject.red, 0)
        self.assertEqual(subject.green, 0)
        self.assertEqual(subject.blue, 0)

    def test_subtract_invalidType(self):
        try:
            badge_creator.utils.RgbColor(3, 5, 7).subtract(5)
        except ValueError as e:
            self.assertEqual(e.__str__(), "Can only subtract a color from another color but 5 of type <class 'int'> was used.")

    def test_parse(self):
        subject = badge_creator.utils.RgbColor.parse_rgb_color('#FEDCBA')
        self.assertEqual(subject.red, 0xFE)
        self.assertEqual(subject.green, 0xDC)
        self.assertEqual(subject.blue, 0xBA)
    
        subject = badge_creator.utils.RgbColor.parse_rgb_color('FEDCBA')
        self.assertEqual(subject.red, 0xFE)
        self.assertEqual(subject.green, 0xDC)
        self.assertEqual(subject.blue, 0xBA)

        subject = badge_creator.utils.RgbColor.parse_rgb_color('FeDCbA')
        self.assertEqual(subject.red, 0xFE)
        self.assertEqual(subject.green, 0xDC)
        self.assertEqual(subject.blue, 0xBA)

        subject = badge_creator.utils.RgbColor.parse_rgb_color('#010203')
        self.assertEqual(subject.red, 0x01)
        self.assertEqual(subject.green, 0x02)
        self.assertEqual(subject.blue, 0x03)
    
        subject = badge_creator.utils.RgbColor.parse_rgb_color('010203')
        self.assertEqual(subject.red, 0x01)
        self.assertEqual(subject.green, 0x02)
        self.assertEqual(subject.blue, 0x03)

    def test_parse_invalid(self):
        try:
            badge_creator.utils.RgbColor.parse_rgb_color('#EDCBA')
            self.fail()
        except badge_creator.utils.ParseError as e:
            self.assertEqual(e.__str__(), "Cannot parse hex color string '#EDCBA'")

        try:
            badge_creator.utils.RgbColor.parse_rgb_color('EDCBA')
            self.fail()
        except badge_creator.utils.ParseError as e:
            self.assertEqual(e.__str__(), "Cannot parse hex color string 'EDCBA'")

        try:
            badge_creator.utils.RgbColor.parse_rgb_color('FEDZBA')
            self.fail()
        except badge_creator.utils.ParseError as e:
            self.assertEqual(e.__str__(), "Cannot parse hex color string 'FEDZBA'")