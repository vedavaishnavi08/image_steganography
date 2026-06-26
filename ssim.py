import os
import cv2
from skimage.metrics import structural_similarity as ssim


def calculate_ssim(original_image, stego_image):
    """
    Calculate the Structural Similarity Index (SSIM)
    between two grayscale images.
    """
    score, _ = ssim(original_image, stego_image, full=True)
    return score


def main():

    original_path = "images/126.bmp"
    stego_path = "images/hide.bmp"

    # Read images
    original = cv2.imread(original_path, cv2.IMREAD_GRAYSCALE)
    stego = cv2.imread(stego_path, cv2.IMREAD_GRAYSCALE)

    # Check whether images loaded successfully
    if original is None:
        print(f"Error: Could not load '{os.path.basename(original_path)}'")
        return

    if stego is None:
        print(f"Error: Could not load '{os.path.basename(stego_path)}'")
        return

    # Check image dimensions
    if original.shape != stego.shape:
        print("Error: Images must have the same dimensions.")
        return

    # Calculate SSIM
    score = calculate_ssim(original, stego)

    # Display results
    print("\nImage Quality Metrics")
    print("-" * 30)
    print(f"Original Image : {os.path.basename(original_path)}")
    print(f"Stego Image    : {os.path.basename(stego_path)}")
    print(f"SSIM           : {score:.6f}")


if __name__ == "__main__":
    main()