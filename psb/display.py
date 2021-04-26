"""Handler for the image/text processing and display to eInk."""
import os

from font_fredoka_one import FredokaOne # noqa
from inky import BLACK, InkyPHAT
from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont

from psb import logger


class EinkDisplay:
    """Object controlling the display of content to the eink display.
    """
    def __init__(self):
        """Init function for EinkDisplay.
        """
        try:
            self.inky_display = auto(ask_user=False, verbose=True)
        except RuntimeError:
            logger.error('Problem connecting to eInk display automatically, trying manually.')
            self.inky_display = InkyPHAT('black')

        self.inky_display.set_border(BLACK)

    @staticmethod
    def process_message(text: str) -> list:
        """Static method to process incoming message.

        Parameters
        ----------
        text : str
            The contents of message to be processed.

        Returns
        -------
        list
            The message after being processed.
        """
        logger.info('Message requires processing.')
        split_lines = []
        lines = text.split("\n")
        for line in lines:
            if len(line) > 20:
                logger.info(f'Line, \"{line}\" longer than 20 characters, splitting')
                line_split = line.split(' ')
                logger.debug(f'Line when split: {line_split}')
                new_line = line_split.pop(0)
                logger.info(new_line)
                while line_split:
                    logger.debug(f'Contents of left in line_split: {line_split}')
                    logger.debug('Line length after join: %s' % len(" ".join([new_line, line_split[0]])))
                    if len(" ".join([new_line, line_split[0]])) <= 20:
                        new_line = " ".join([new_line, line_split.pop(0)])
                    else:
                        split_lines.append(new_line)
                        new_line = line_split.pop(0)
                split_lines.append(new_line)
            else:
                logger.info(f'Line, \"{line}\" does not require splitting.')
                split_lines.append(line)
        logger.debug(f'Contents of split lines: {split_lines}')
        return split_lines

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
        except FileNotFoundError as file_not_found:
            logger.error(f'Cannot set image, no image {filename}')
            raise FileNotFoundError from file_not_found

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
            processed_message = self.process_message(text)
            if len(processed_message) <= 3:
                text = "\n".join(processed_message)
                logger.info(f'New message: {text}')
                draw.multiline_text((x_axis, y_axis), text, self.inky_display.BLACK, font, align="center")
                self.__eink_show(img)
            else:
                logger.error(f'Cannot display message, more than 3 lines long, ({len(processed_message)})')
                logger.error(f'Post-processing message: {processed_message}')

    def __eink_show(self, img: Image):
        """Function to show completed image on display.png

        Parameters
        ----------
        img : Image
            The PIL image to display.
        """
        self.inky_display.set_image(img)
        self.inky_display.show()
