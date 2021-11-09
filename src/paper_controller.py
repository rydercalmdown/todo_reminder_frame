import sys
import os
import logging
from epaper_libs import epd7in5_V2
import time
from PIL import Image, ImageDraw, ImageFont
import traceback
import numpy as np


class PaperController():
    """Draws an image """

    def __init__(self):
        """Instantiates the module"""
        logging.info('Starting 7.5 inch E-Paper Module')
        self.paper = epd7in5_V2.EPD()
        self.paper.init()

    def __del__(self):
        """Deletes the module"""
        self.paper.sleep()

    def _get_blank_image(self):
        """Returns a blank image to start with"""
        return Image.new('1', (self.paper.width, self.paper.height), 255)

    def _get_default_font(self, size=24):
        """Returns the default font"""
        return ImageFont.truetype("fonts/Roboto-Medium.ttf", size)

    def _convert_image_to_bitmap(self, original_img):
        """Converts an image to bitmap"""
        img_arr = np.array(original_img)
        r, g, b = np.split(img_arr, 3, axis=2)
        r = r.reshape(-1)
        g = r.reshape(-1)
        b = r.reshape(-1)
        bitmap = list(map(lambda x: 0.299 * x[0] + 0.587 * x[1] + 0.114 * x[2], zip(r, g, b)))
        bitmap = np.array(bitmap).reshape([img_arr.shape[0], img_arr.shape[1]])
        bitmap = np.dot((bitmap > 128).astype(float),255)
        im = Image.fromarray(bitmap.astype(np.uint8))
        return im

    def _write_image_to_paper(self, image):
        """Writes the image to the paper"""
        logging.info('Getting image buffer')
        buffer = self.paper.getbuffer(image)
        logging.info('Writing image to paper')
        self.paper.display(buffer)

    def _paste_in_centre(self, original_img, pasted_img):
        """Pastes one image in the centre of an original"""
        org_x = original_img.size[0]
        org_y = original_img.size[1]
        pst_x = pasted_img.size[0]
        pst_y = pasted_img.size[1]
        x1 = int(.5 * org_x) - int(.5 * pst_x)
        y1 = int(.5 * org_y) - int(.5 * pst_y)
        x2 = int(.5 * org_x) + int(.5 * pst_x)
        y2 = int(.5 * org_y) + int(.5 * pst_y)
        bounding_box = (x1, y1, x2, y2)
        original_img.paste(pasted_img, box=bounding_box)
        return original_img

    def clear(self):
        """Fully clears the e paper"""
        self.paper.Clear()

    def sleep(self):
        """Puts the module to sleep"""
        self.paper.sleep()

    def display_title(self, title_text, subtitle_text=''):
        """Displays a title on the paper"""
        blank_img = self._get_blank_image()
        draw = ImageDraw.Draw(blank_img)
        title_font = self._get_default_font(32)
        tw, th = draw.textsize(title_text, font=title_font)
        position_x = (self.paper.width - tw) / 2
        position_y = (self.paper.height - th) / 2
        draw.text((position_x, position_y), title_text, font=title_font)
        if subtitle_text:
            subtitle_font = self._get_default_font(16)
            sw, sh = draw.textsize(subtitle_text, font=subtitle_font)
            position_x = (self.paper.width - sw) / 2
            position_y = (self.paper.height - sh + th + 32) / 2
            draw.text((position_x, position_y), subtitle_text, font=subtitle_font)
        self._write_image_to_paper(blank_img)

    def display_image(self, image_file):
        """Displays an image file on the paper"""
        original_img = Image.open(image_file)
        bmp = self._convert_image_to_bitmap(original_img)
        display_img = self._get_blank_image()
        display_img = self._paste_in_centre(display_img, bmp)
        self._write_image_to_paper(display_img)
