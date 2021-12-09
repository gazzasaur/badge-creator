import re
import numbers

class ParseError(Exception):
    def __init__(self, message):
        super().__init__(message)

class RgbColor:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue
        self.validate_color()

    def multiply(self, value):
        if (not isinstance(value, numbers.Number)):
            raise ValueError("Can only multiply a color by a number but {} of type {} was used.".format(value, type(value)))

        result = RgbColor(0, 0, 0)
        for component in ['red', 'green', 'blue']:
            setattr(result, component, getattr(self, component) * value + 0.5)
        result.clamp()

        return result

    def add(self, value):
        if (not isinstance(value, RgbColor)):
            raise ValueError("Can only add a color from another color but {} of type {} was used.".format(value, type(value)))

        result = RgbColor(0, 0, 0)
        for component in ['red', 'green', 'blue']:
            setattr(result, component, getattr(self, component) + getattr(value, component))
        result.clamp()

        return result

    def subtract(self, value):
        if (not isinstance(value, RgbColor)):
            raise ValueError("Can only subtract a color from another color but {} of type {} was used.".format(value, type(value)))

        result = RgbColor(0, 0, 0)
        for component in ['red', 'green', 'blue']:
            setattr(result, component, getattr(self, component) - getattr(value, component))
        result.clamp()

        return result

    def __repr__(self) -> str:
        return "RgbColor({}, {}, {})".format(self.red, self.green, self.blue)

    def clamp(self):
        for component in ['red', 'green', 'blue']:
            setattr(self, component, min(255, max(0, int(getattr(self, component)))))

    def validate_color(self):
        for color_attribute in ['red', 'green', 'blue']:
            value = getattr(self, color_attribute)
            if (not isinstance(value, int) or value > 0xFF or value < 0):
                raise ValueError('Color component {} must be and int between 0 and 255 inclusive but was {} of type {}'.format(color_attribute, value, type(value)))

    def parse_rgb_color(rgb_color_hex_string):
        matcher = re.match('^#?([0-9a-fA-F]{6})$', rgb_color_hex_string);
        if not matcher:
            raise ParseError("Cannot parse hex color string '{}'".format(rgb_color_hex_string))
        hex_color = matcher.group(1)
        rgb_color_hex_int = int(hex_color, 16);
        return RgbColor(rgb_color_hex_int // 65536 % 256, rgb_color_hex_int // 256 % 256, rgb_color_hex_int % 256)
