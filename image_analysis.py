import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


def is_binary(gray_image):
    """
    Check whether a grayscale image is binary.
    A binary image contains only pixel values 0, 1, or 255.
    """
    unique_values = np.unique(gray_image)
    return set(unique_values).issubset({0, 1, 255})


def analyze_image(image_path):
    """
    Analyze an image and display its properties
    along with its intensity histogram.
    """

    print("\n" + "=" * 50)
    print(f"Analyzing Image: {os.path.basename(image_path)}")
    print("=" * 50)

    # Read image
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    if image is None:
        print(f"Error: Could not load '{image_path}'.")
        return

    # Determine image type
    if image.ndim == 2:

        gray_image = image

        if is_binary(gray_image):
            image_type = "Binary Image"
        else:
            image_type = "Grayscale Image"

    else:

        # Check whether all three channels are identical
        if (
            np.array_equal(image[:, :, 0], image[:, :, 1])
            and np.array_equal(image[:, :, 1], image[:, :, 2])
        ):

            gray_image = image[:, :, 0]

            if is_binary(gray_image):
                image_type = "Binary Image (Stored as BGR)"
            else:
                image_type = "Grayscale Image (Stored as BGR)"

        else:

            image_type = "True Color Image"
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Image information
    height, width = image.shape[:2]
    channels = 1 if image.ndim == 2 else image.shape[2]

    print("\nImage Information")
    print("-" * 30)
    print(f"Dimensions     : {width} x {height}")
    print(f"Channels       : {channels}")
    print(f"Image Type     : {image_type}")

    print("\nPixel Statistics")
    print("-" * 30)
    print(f"Minimum Pixel  : {image.min()}")
    print(f"Maximum Pixel  : {image.max()}")
    print(f"Average Pixel  : {image.mean():.2f}")

    # Display histogram
    plt.figure(figsize=(8, 4))

    plt.hist(
        gray_image.ravel(),
        bins=256,
        range=(0, 256),
        color="gray",
        edgecolor="black"
    )

    plt.title(f"Histogram of {os.path.basename(image_path)}")
    plt.xlabel("Pixel Intensity")
    plt.ylabel("Frequency")
    plt.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.show()


def main():

    images = [
        "images/126.bmp",
        "images/cover.bmp",
        "images/256secret.bmp"
    ]

    if not images:
        print("No images found.")
        return

    for image_path in images:
        analyze_image(image_path)


if __name__ == "__main__":
    main()