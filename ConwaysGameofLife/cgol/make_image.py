""" Make Images """
from PIL import Image
from PIL import ImageOps

"""
width = 10
height =10
image = Image.new('RGBA', (width, height), (255, 255, 255, 255))

pixels = image.load()
color = pixels[4, 5]

print(color)

pixels[4, 5] = (128, 0, 128, 255) # purple

print(pixels[4, 5])

filepath = 'cgol/images/image.png'
image.save(filepath)
"""

IMAGEDATA = {
    'width' : 0,
    'height' : 0,
    'color' : (0, 0, 0)
    }


def create_new_image(height, width, color=(0, 0, 0)):
    """ Create a new white png with size width and height. """

    IMAGEDATA['color'] = color
    IMAGEDATA['width'] = width
    IMAGEDATA['height'] = height

    image = Image.new('RGB', (width, height), color)
    pixels = image.load()
    return image, pixels


def set_live_pixel(pixels, col, row, color=(0, 255, 0)):
    """ Set the pixel at r,c to purple """

    pixels[col, row] = color # green


# Not Used
def set_dead_pixel(pixels, col, row):
    """ Set the pixel at r,c to black """

    pixels[col, row] = IMAGEDATA['color']


def save_image(image, index, resize=True):
    """ Save image at cgol/images/image_index.png """

    if resize:
        image = resize_image(image, 512)

    filepath = '{0}{1}{2}'.format('cgol/images/image_', str(index), '.png')
    image.save(filepath)


def resize_image(image, base=512):
    """
        Resize and image to scale with maximum base value.
        If base value < image dimensions, image is not resized.
    """

    width = IMAGEDATA['width']
    height = IMAGEDATA['height']

    if maximum(width, height) >= base:
        return image

    scale = maximum(width, height, base) / maximum(width, height)
    return image.resize((int(width * scale), int(height * scale)), Image.ANTIALIAS)

def save_width_height(width, height):
    """ Save the wdith and height of an opened image """

    IMAGEDATA['width'] = width
    IMAGEDATA['height'] = height


def maximum(a, b, c=0):
    """ Return the greatest of 3 values """

    if a > b and a > c:
        return a
    if b > c:
        return b
    return c
