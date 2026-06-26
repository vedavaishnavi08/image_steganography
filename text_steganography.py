import os
import cv2
import random


def hide_message(image_path, secret_message, secret_key, output_image):
    """
    Hide a secret message inside an image using
    Least Significant Bit (LSB) steganography.
    """
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Could not load '{os.path.basename(image_path)}'.")
        return

    # Add delimiter to mark end of message
    secret_message += "#"

    height, width, _ = image.shape
    total_pixels = height * width
    required_bits = len(secret_message) * 8

    # Check image capacity
    if required_bits > total_pixels:
        print("Error: Secret message is too large for this image.")
        return

    # Generate pseudo-random pixel positions
    # sample size must match extract_message's sample size (total_pixels),
    # otherwise the same seed produces a DIFFERENT ordering and extraction breaks.
    random.seed(secret_key)
    positions = random.sample(range(total_pixels), total_pixels)

    index = 0
    # Embed message
    for character in secret_message:
        binary_character = format(ord(character), "08b")
        for bit in binary_character:
            position = positions[index]
            row = position // width
            col = position % width

            blue_channel = image[row][col][0]
            # Clear LSB
            blue_channel &= 254
            # Insert secret bit
            blue_channel |= int(bit)
            image[row][col][0] = blue_channel

            index += 1

    if cv2.imwrite(output_image, image):
        print("\nMessage hidden successfully!")
        print(f"Output Image : {os.path.basename(output_image)}")
    else:
        print("Error: Failed to save image.")


def extract_message(image_path, secret_key):
    """
    Extract a hidden message from a stego image.
    """
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Could not load '{os.path.basename(image_path)}'.")
        return

    height, width, _ = image.shape
    total_pixels = height * width

    random.seed(secret_key)
    positions = random.sample(range(total_pixels), total_pixels)

    message = ""
    index = 0

    while True:
        binary_character = ""
        for _ in range(8):
            if index >= len(positions):
                print("Error: Hidden message could not be extracted.")
                return

            position = positions[index]
            row = position // width
            col = position % width

            blue_channel = image[row][col][0]
            binary_character += str(blue_channel & 1)
            index += 1

        character = chr(int(binary_character, 2))

        if character == "#":
            break

        message += character

    print("\nExtracted Message")
    print("-" * 30)
    print(message)


def main():
    while True:
        print("\nText Steganography")
        print("-" * 30)
        print("1. Hide Message")
        print("2. Extract Message")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            image_path = "images/" + input("Enter cover image (e.g., cover.bmp): ")
            message = input("Enter secret message: ")
            key = int(input("Enter secret key: "))
            output_image = "images/" + input("Enter output image (e.g., hide.bmp): ")
            hide_message(image_path, message, key, output_image)

        elif choice == "2":
            image_path = "images/" + input("Enter stego image (e.g., hide.bmp): ")
            key = int(input("Enter secret key: "))
            extract_message(image_path, key)

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()