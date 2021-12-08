import argparse
import logging
import sys
import os

from badge_creator import __version__, generators
from badge_creator.utils import RgbColor

__author__ = "gaz"
__copyright__ = "gaz"
__license__ = "MIT"

_logger = logging.getLogger(__name__)

import PIL.ImageFont

def generate(command_line_args):
    args = [command_line_args.label, command_line_args.text, command_line_args.output]

    kwargs = {
        'label_background': RgbColor.parse_rgb_color(command_line_args.label_background),
        'text_background': RgbColor.parse_rgb_color(command_line_args.text_background)
    }
    if hasattr(command_line_args, 'font') and command_line_args.font:
        kwargs['font'] = PIL.ImageFont.truetype(command_line_args.font, command_line_args.font_size)

    _logger.debug("Generating simple badge {}: {}".format(command_line_args.label, command_line_args.text))
    getattr(generators.SimpleGenerator(), 'generate')(*args, **kwargs)
    _logger.debug("Generatied simple badge {}: {}".format(command_line_args.label, command_line_args.text))

def parse_args(args):
    parser = argparse.ArgumentParser(description="""A badge creator.
    Example: """)
    parser.add_argument(
        "--version",
        action="version",
        version="badge-creator {ver}".format(ver=__version__),
    )
    parser.add_argument(dest="label", help="set the badge label", type=str, metavar="LABEL")
    parser.add_argument(dest="text", help="set the badge text", type=str, metavar="TEXT")
    parser.add_argument(dest="output", help="the output file to store the generated png badge", type=str, metavar="OUTPUT")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    parser.add_argument(
        "-f",
        "--font",
        dest="font",
        help="set the truetype font to use (see https://pillow.readthedocs.io/en/stable/reference/ImageFont.html#PIL.ImageFont.truetype)",
        action="store",
    )
    parser.add_argument(
        "-s",
        "--font-size",
        type=int,
        dest="font_size",
        help="set the font size to use.  Only effective if --font is also specified (default: 14)",
        default=14,
        action="store",
    )
    parser.add_argument(
        "-c",
        "--label-background",
        dest="label_background",
        help="set the background color of the banner label in RGB hex format (default: 444444)",
        default='444444',
        action="store",
    )
    parser.add_argument(
        "-b",
        "--text-background",
        dest="text_background",
        help="set the background color of the banner value in RGB hex format (default: 3366FF)",
        default='3366FF',
        action="store",
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )

def main(args):
    args = parse_args(args)
    setup_logging(args.loglevel)
    generate(args)

def run():
    main(sys.argv[1:])

if __name__ == "__main__":
    run()
