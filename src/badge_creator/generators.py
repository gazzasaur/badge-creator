import re
import PIL
import PIL.Image
import PIL.ImageFont
import PIL.ImageDraw

from badge_creator.utils import RgbColor

class SimpleGenerator:
    """
    Generates a simple gradient style badge and writes the output in PNG format.
    The text is white with a black shadow to suit light and dark colors.
    """

    def __init__(self):
        pass

    def generate(self, label, text, output, label_background=RgbColor(0x33, 0x33, 0x33), text_background=RgbColor(0x33, 0x66, 0xFF), fade_factor=0.20, font=PIL.ImageFont.load_default()):
        """
        Generates a simple gradient style badge and writes the output in PNG format.

        :param label: The label portion of a badge.
        :param text: The text portion of a badge.
        :param label_background: The lightest label background color of the gradient (default = RgbColor(0x33, 0x33, 0x33)).
        :param text_background: The lightest text background color of the gradient (default = RgbColor(0x33, 0x66, 0xFF)).
        :param fade_factor: Multiplied by the background colors to calculate the darkest porition of the gradient (default = 0.2).
        :param font: The font to use.  Set this to something, the default is not very good (default = a builtin font mask).
        :param output: A filename (string), pathlib.Path object or file object.
        :returns: None
        :exception OSError: If the file could not be written.  The file
           may have been created, and may contain partial data.
        """

        text_height = self.calculate_text_height(font)
        label_width = font.getmask(label).getbbox()[2];
        value_width = font.getmask(text).getbbox()[2];

        badge_padding = text_height // 2
        badge_height = 2*badge_padding + text_height
        badge_width = label_width + value_width + 4*badge_padding;
        image = PIL.Image.new("RGBA", (badge_width, badge_height))

        self.generate_background(image, label_background, text_background, 2*badge_padding + label_width, badge_padding, fade_factor)
        self.generate_shadow_text(image, label, badge_padding, font, badge_padding)
        self.generate_shadow_text(image, text, 3*badge_padding + label_width, font, badge_padding)

        image.save(output, "PNG")

    def generate_shadow_text(self, image, text, location, font, padding):
        drawing = PIL.ImageDraw.Draw(image)
        drawing.text((location + 1, padding + 1), text, fill="black", font=font)
        drawing.text((location, padding), text, fill="white", font=font)

    def generate_background(self, image, label_background, text_background, label_width, padding, fade_factor):
        drawing = PIL.ImageDraw.Draw(image)
        # Create the mask we want to generate the gradient against
        drawing.rounded_rectangle(((0, 0), (image.width - 1, image.height - 1)), radius=padding, fill ="#ffffff")

        faded_text_background = text_background.multiply(fade_factor)
        faded_label_background = label_background.multiply(fade_factor)

        for x in range(0, image.width):
            for y in range(0, image.height):
                if image.getpixel((x, y))[0] != 0:
                    stage_color = RgbColor(0, 0, 0)
                    if (x < label_width):
                        stage_color = label_background.subtract(faded_label_background).multiply(1.0 / image.height).multiply(image.height - y).add(faded_label_background)
                    else:
                        stage_color = text_background.subtract(faded_text_background).multiply(1.0 / image.height).multiply(image.height - y).add(faded_text_background)
                    drawing.point((x, y), fill="#{:02X}{:02X}{:02X}".format(stage_color.red, stage_color.green, stage_color.blue))

    def calculate_text_height(self, font):
        text_height = font.getmask('M').getbbox()[3]
        if hasattr(font, 'getmetrics'):
            ascent, descent = font.getmetrics()
            text_height += descent
        return text_height
