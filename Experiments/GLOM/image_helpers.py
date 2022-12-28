import numpy as np
import matplotlib.pyplot as plt

# Pillow
import PIL
from PIL import Image

# https://developer.ibm.com/articles/image-recognition-challenge-with-tensorflow-and-keras-pt1/


# Use Pillow library to convert an input jpeg to a 8 bit grey scale image array.
def jpeg_to_8_bit_greyscale(path, maxsize):
    img = Image.open(path).convert('L')   # convert image to 8-bit grayscale
    # Change aspect ratio to 1:1 by applying image crop.
    WIDTH, HEIGHT = img.size
    if WIDTH != HEIGHT:
            m_min_d = min(WIDTH, HEIGHT)
            img = img.crop((0, 0, m_min_d, m_min_d))
    # Scale the image to the requested maxsize by Anti-alias sampling.
    img.thumbnail(maxsize, PIL.Image.ANTIALIAS)
    return np.asarray(img)


def display_image(image, title):
    plt.imshow(image, cmap=plt.cm.binary)
    plt.title(title)
    plt.show()


def display_images(images, labels, title):
    plt.figure(figsize=(10, 10))
    grid_size = min(25, len(images))
    title_shown = False
    for i in range(grid_size):
        plt.subplot(5, 5, i + 1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(images[i], cmap=plt.cm.binary)
        plt.xlabel(labels[i])
        if not title_shown:
            plt.title(title)
            title_shown = True

    plt.show()
