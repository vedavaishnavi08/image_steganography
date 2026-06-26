import os
from PIL import Image
import numpy as np


def load_image(image_path):
    """
    Load an image from the given path.
    """
    try:
        return Image.open(image_path)
    except FileNotFoundError:
        print(f"Error: '{image_path}' not found.")
        return None


def display_pixel_information(image_path):
    """
    Display basic information and sample pixel values of an image.
    """

    image = load_image(image_path)

    if image is None:
        return

    pixels = np.array(image)

    print("\nImage Information")
    print("-" * 30)
    print(f"File Name   : {os.path.basename(image_path)}")
    print(f"Image Size  : {image.size}")
    print(f"Image Mode  : {image.mode}")
    print(f"Array Shape : {pixels.shape}")

    print("\nFirst 5 × 5 Pixel Values")
    print("-" * 30)
    print(pixels[:5, :5])


def main():

    image_path = "images/cover.bmp"

    display_pixel_information(image_path)


if __name__ == "__main__":
    main()