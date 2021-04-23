"""Handler for the image/text processing and display to eInk."""
import os

from fonts.ttf import FredokaOne # noqa
from inky import BLACK
from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont

from psb import logger


class EinkDisplay:
    """Object controlling the display of content to the eink display.
    """
    def __init__(self):
        """Init function for EinkDisplay.
        """
        self.inky_display = auto(ask_user=True, verbose=True)
        self.inky_display.set_border(BLACK)

    def image(self, path: str, status: str = 'idle'):
        """Function to process the request for an image to be displayed.

        Parameters
        ----------
        path : str
            The path that locates the image files.
        status : str, optional
            The state (and corrosponding filename) use to display, by default 'idle'
        """
        filename = f"{status}.png"
        logger.info(f'Using filename: {filename}')
        try:
            img = Image.open(os.path.join(path, filename))
            self.__eink_show(img)
        except FileNotFoundError:
            logger.error(f'Cannot set image, no image {filename}')

    def text(self, text: str):
        """Function to process request for text to be displayed on the eink display.
        Will check that there are no more than 3 lines of 20 characters each, if so
        they will be cut down to to correct size. If more than 3 lines, no text is displayed.txt.

        Parameters
        ----------
        text : str
            The text string to process.
        """
        logger.info(f'Setting display to text: {text}')
        img = Image.new("P", (self.inky_display.WIDTH, self.inky_display.HEIGHT))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(FredokaOne, 22)
        x_axis = 0
        y_axis = 0

        if len(text) <= 20 and len(text.split("\n")) == 1: # noqa #TODO: fix the amount of if statements.
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
                    new_line = line_split.pop(0)
                    while line_split:
                        if len(" ".join([new_line, line_split.pop(0)])) <= 20:
                            new_line = " ".join([new_line, line_split.pop(0)])
                        else:
                            split_lines.append(new_line)
                            try:
                                new_line = line_split.pop(0)
                            except IndexError:
                                split_lines.append(line_split.pop(0))
                else:
                    split_lines.append(line)
            if len(split_lines) <= 3:
                text = "\n".join(split_lines)
                logger.info(f'New message: {text}')
                draw.multiline_text((x_axis, y_axis), text, self.inky_display.BLACK, font, align="center")
                self.__eink_show(img)
            else:
                logger.error(f'Cannot display message, more than 3 lines long, ({len(split_lines)})')
                logger.error(f'Post-processing message: {split_lines}')

    def __eink_show(self, img: Image):
        """Function to show completed image on display.png

        Parameters
        ----------
        img : Image
            The PIL image to display.
        """
        self.inky_display.set_image(img)
        self.inky_display.show()
