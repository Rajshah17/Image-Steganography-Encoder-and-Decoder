from PIL import Image

def decode_image(encoded_image_filename):
    # Open encoded image and convert to RGB format
    encoded_img = Image.open(encoded_image_filename).convert('RGB')
    width, height = encoded_img.size

    # Decode message from image
    binary_message = ''
    pixel_index = 0
    while True:
        x = pixel_index % width
        y = pixel_index // width
        r, g, b = encoded_img.getpixel((x, y))
        if r & 0b00000001 == 0:
            # Least significant bit is 0, add 0 to binary message
            binary_message += '0'
        else:
            # Least significant bit is 1, add 1 to binary message
            binary_message += '1'
        pixel_index += 1
        # Check for delimiter at end of message
        if binary_message[-8:] == '00000000':
            break

    # Convert binary message to string
    message = ''
    for i in range(0, len(binary_message)-8, 8):
        message += chr(int(binary_message[i:i+8], 2))

    return message

# Example usage
encoded_image_filename = input("Enter image path: ")
message = decode_image(encoded_image_filename)
print(f'Decoded message: {message}')