import os

from font_fredoka_one import FredokaOne
from inky import BLACK
from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont

from psb import logger


class EinkDisplay:
    def __init__(self):
        self.inky_display = auto(ask_user=True, verbose=True)
        self.inky_display.set_border(BLACK)

    def image(self, path: str, status: str = 'idle'):
        filename = f"{status}.png"
        logger.info(f'Using filename: {filename}')
        try:
            img = Image.open(os.path.join(path, filename))
            self.eink_show(img)
        except FileNotFoundError:
            logger.error(f'Cannot set image, no image {filename}')

    def text(self, text):
        logger.info(f'Setting display to text: {text}')
        img = Image.new("P", (self.inky_display.WIDTH, self.inky_display.HEIGHT))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(FredokaOne, 22)
        x_axis = 0
        y_axis = 0

        if len(text) <= 20 and len(text.split("\n")) == 1:
            logger.info('Message 1 line and <= 20 characters, displaying.')
            draw.text((x_axis, y_axis), text, self.inky_display.BLACK, font)
        else:
            logger.info('Message requires processing.')
            split_lines = []
            lines = text.split("\n")
            for line in lines:
                if len(line) > 20:
                    logger.info(f'Line, \"{line}\" longer than 20 characters, splitting')
                    line_split = line.split(' ')
                    new_line = line_split[0]
                    line_split.pop(0)
                    while line_split:
                        if len(" ".join([new_line, line_split[0]])) <= 20:
                            new_line = " ".join([new_line, line_split[0]])
                            line_split.pop(0)
                        else:
                            split_lines.append(new_line)
                            if len(line_split) != 1:
                                new_line = line_split[0]
                                line_split.pop(0)
                            else:
                                split_lines.append(line_split[0])
                                line_split.pop(0)
                else:
                    split_lines.append(line)
            if len(split_lines) <= 3:
                text = "\n".join(split_lines)
                logger.info(f'New message: {text}')
                draw.multiline_text((x_axis, y_axis), text, self.inky_display.BLACK, font, align="center")
                self.eink_show(img)
            else:
                logger.error(f'Cannot display message, more than 3 lines long, ({len(split_lines)})')
                logger.error(f'Post-processing message: {split_lines}')

    def eink_show(self, img):
        self.inky_display.set_image(img)
        self.inky_display.show()
