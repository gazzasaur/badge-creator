import io
import unittest

import PIL.Image
from badge_creator.generators import SimpleGenerator
from badge_creator.utils import RgbColor

class TestGenerators(unittest.TestCase):
    def test_generate(self):
        """
        Cheap and nasty test against a known benchmark

        To reproduce this test image run:
            python -m badge_creator.cli -f DejaVuSans.ttf -b FFFF00 coverage '90%' samples/coverage.png
        """
        buffer = io.BytesIO()
        subject = SimpleGenerator()
        font = PIL.ImageFont.truetype('DejaVuSans.ttf', 14)

        subject.generate('coverage', '90%', buffer, text_background=RgbColor(255, 255, 0), font=font)
        standard = PIL.Image.open('samples/coverage.png')
        generated = PIL.Image.open(buffer)

        width = standard.width
        height = standard.height
        self.assertEqual(width, generated.width)
        self.assertEqual(height, generated.height)
        for x in range(0, width):
            for y in range(0, height):
                self.assertEqual(standard.getpixel((x, y)), generated.getpixel((x, y)))

    def test_generate_default_font(self):
        """
        Cheap and nasty test against a known benchmark

        To reproduce this test image run:
            python -m badge_creator.cli -c 00FF00 -b 0000FF default font samples/default_font.png
        """
        buffer = io.BytesIO()
        subject = SimpleGenerator()

        subject.generate('default', 'font', buffer, label_background=RgbColor(0, 255, 0), text_background=RgbColor(0, 0, 255))
        standard = PIL.Image.open('samples/default_font.png')
        generated = PIL.Image.open(buffer)

        width = standard.width
        height = standard.height
        self.assertEqual(width, generated.width)
        self.assertEqual(height, generated.height)
        for x in range(0, width):
            for y in range(0, height):
                self.assertEqual(standard.getpixel((x, y)), generated.getpixel((x, y)))
