import os
import cv2
import numpy as np


def calculate_mse(original_image, stego_image):
    """
    Calculate Mean Squared Error (MSE) between two images.
    """
    return np.mean((original_image - stego_image) ** 2)


def calculate_psnr(mse):
    """
    Calculate Peak Signal-to-Noise Ratio (PSNR).
    """
    if mse == 0:
        return float("inf")
    return 10 * np.log10((255 ** 2) / mse)


def main():

    original_path = "images/126.bmp"
    stego_path = "images/hide.bmp"

    # Read images in grayscale
    original = cv2.imread(original_path, cv2.IMREAD_GRAYSCALE)
    stego = cv2.imread(stego_path, cv2.IMREAD_GRAYSCALE)

    # Check whether images loaded successfully
    if original is None:
        print(f"Error: Could not load '{os.path.basename(original_path)}'")
        return

    if stego is None:
        print(f"Error: Could not load '{os.path.basename(stego_path)}'")
        return

    # Ensure both images have the same dimensions
    if original.shape != stego.shape:
        print("Error: Images must have the same dimensions.")
        return

    # Convert to float to avoid uint8 overflow
    original = original.astype(np.float32)
    stego = stego.astype(np.float32)

    # Calculate metrics
    mse = calculate_mse(original, stego)
    psnr = calculate_psnr(mse)

    # Display results
    print("\nImage Quality Metrics")
    print("-" * 30)
    print(f"Original Image : {os.path.basename(original_path)}")
    print(f"Stego Image    : {os.path.basename(stego_path)}")
    print(f"MSE            : {mse:.4f}")

    if psnr == float("inf"):
        print("PSNR           : Infinite (Images are identical)")
    else:
        print(f"PSNR           : {psnr:.2f} dB")


if __name__ == "__main__":
    main()