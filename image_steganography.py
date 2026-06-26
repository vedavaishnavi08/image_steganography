import os
import cv2
import numpy as np


def hide_image(cover_image_path, secret_image_path, output_image_path):
    """
    Hide a binary image inside the least significant bit (LSB)
    of a cover image. The cover can be color OR grayscale --
    its original color is preserved in the output.

    For a color cover, only the blue channel's LSB is used to
    store the secret (the human eye is least sensitive to tiny
    blue changes). For a grayscale cover, the pixel's own LSB
    is used directly.

    The cover no longer needs to match the secret's dimensions --
    it just needs enough pixels to hold it. The secret's height
    and width are stored in the first 32 pixels of the cover so
    extraction knows exactly how much to read back.
    """
    # IMREAD_UNCHANGED keeps the cover exactly as it is on disk:
    # color stays color (3 channels), grayscale stays grayscale (1 channel).
    cover = cv2.imread(cover_image_path, cv2.IMREAD_UNCHANGED)
    secret = cv2.imread(secret_image_path, cv2.IMREAD_GRAYSCALE)

    if cover is None:
        print("Error: Could not load cover image.")
        return

    if secret is None:
        print("Error: Could not load secret image.")
        return

    is_color = cover.ndim == 3
    cover_height, cover_width = cover.shape[:2]
    secret_height, secret_width = secret.shape

    # Header stores secret_height (16 bits) + secret_width (16 bits) = 32 bits total
    HEADER_SIZE = 32
    secret_pixels_needed = secret_height * secret_width
    total_bits_needed = HEADER_SIZE + secret_pixels_needed

    cover_capacity = cover_height * cover_width

    if total_bits_needed > cover_capacity:
        print("Error: Cover image is too small to hold this secret image.")
        return

    # Work on a flat view of just the channel we're allowed to touch:
    # the blue channel (index 0 in OpenCV's BGR order) for color covers,
    # or the only channel there is for grayscale covers.
    if is_color:
        carrier = cover[:, :, 0].flatten()
    else:
        carrier = cover.flatten()

    # Build the 32-bit header: 16 bits for height, 16 bits for width
    header = format(secret_height, "016b") + format(secret_width, "016b")

    # Write header bits into the first 32 pixels of the carrier channel.
    # & 254 clears the last bit (LSB) of the pixel, | bit then writes
    # the header bit into that now-empty last bit. The other 7 bits
    # of the pixel -- and the other 2 color channels, if any -- are
    # left completely untouched, so the change is invisible to the eye.
    for i, bit in enumerate(header):
        carrier[i] = (carrier[i] & 254) | int(bit)

    # Write secret image bits right after the header, using the same
    # LSB substitution: clear the carrier pixel's last bit, then set
    # it to 1 if the secret pixel is white (>0) or 0 if it's black.
    flat_secret = secret.flatten()
    index = HEADER_SIZE
    for secret_pixel in flat_secret:
        bit = 1 if secret_pixel > 0 else 0
        carrier[index] = (carrier[index] & 254) | bit
        index += 1

    # Put the modified channel back into the cover image
    if is_color:
        cover[:, :, 0] = carrier.reshape(cover_height, cover_width)
        stego = cover
    else:
        stego = carrier.reshape(cover_height, cover_width)

    if cv2.imwrite(output_image_path, stego):
        print("\nBinary image hidden successfully.")
        print(f"Output Image : {os.path.basename(output_image_path)}")
        print(f"Cover type    : {'Color' if is_color else 'Grayscale'}")
        print(f"Secret size embedded: {secret_height} x {secret_width}")
    else:
        print("Error: Failed to save stego image.")


def extract_image(stego_image_path, output_image_path):
    """
    Extract the hidden binary image from a stego image.
    Works whether the stego image is color or grayscale,
    since the secret was only ever written into one channel.

    Reads the 32-bit header first to recover the secret's original
    height and width, then reads back exactly that many pixels.
    """
    stego = cv2.imread(stego_image_path, cv2.IMREAD_UNCHANGED)

    if stego is None:
        print("Error: Could not load stego image.")
        return

    is_color = stego.ndim == 3

    # The secret was written into the blue channel for color images,
    # or the only channel for grayscale images -- read back the same one.
    if is_color:
        carrier = stego[:, :, 0].flatten()
    else:
        carrier = stego.flatten()

    if len(carrier) < 32:
        print("Error: Stego image is too small to contain a valid header.")
        return

    # Read the 32-bit header back out first. & 1 isolates just the
    # last bit (LSB) of each pixel -- the same bit that was written
    # during hiding. The first 16 bits give the secret's height,
    # the next 16 bits give its width.
    header_bit_string = ""
    for i in range(32):
        header_bit_string += str(carrier[i] & 1)

    secret_height = int(header_bit_string[:16], 2)
    secret_width = int(header_bit_string[16:], 2)

    secret_pixels_needed = secret_height * secret_width

    if 32 + secret_pixels_needed > len(carrier):
        print("Error: Stego image does not contain a valid hidden image.")
        return

    extracted_flat = np.zeros(secret_pixels_needed, dtype=np.uint8)

    index = 32
    for i in range(secret_pixels_needed):
        bit = carrier[index] & 1
        extracted_flat[i] = 255 if bit else 0
        index += 1

    extracted = extracted_flat.reshape(secret_height, secret_width)

    if cv2.imwrite(output_image_path, extracted):
        print("\nBinary image extracted successfully.")
        print(f"Extracted Image : {os.path.basename(output_image_path)}")
        print(f"Extracted size  : {secret_height} x {secret_width}")
    else:
        print("Error: Failed to save extracted image.")


def main():
    while True:
        print("\nBinary Image Steganography")
        print("-" * 35)
        print("1. Hide Binary Image")
        print("2. Extract Binary Image")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            cover = "images/" + input("Enter cover image (e.g., cover.bmp): ")
            secret = "images/" + input("Enter binary secret image (e.g., 256secret.bmp): ")
            output = "images/" + input("Enter output image name (e.g., hide.bmp): ")
            hide_image(cover, secret, output)

        elif choice == "2":
            stego = "images/" + input("Enter stego image (e.g., hide.bmp): ")
            output = "images/" + input("Enter extracted image name (e.g., extracted.bmp): ")
            extract_image(stego, output)

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()