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