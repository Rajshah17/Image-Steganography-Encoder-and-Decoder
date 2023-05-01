from PIL import Image

def encode_image(image_filename, message):
    # Open image and convert to RGB format
    img = Image.open(image_filename).convert('RGB')
    width, height = img.size

    # Convert message to binary string
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    # Check if message is too long to encode in the image
    max_message_size = width * height * 3 // 8
    if len(binary_message) > max_message_size:
        raise ValueError('Message too long to encode in the image')
      
    # Add delimiter to end of message to indicate end of message
    binary_message += '00000000'

    # Encode message in image
    pixel_index = 0
    for char in binary_message:
        x = pixel_index % width
        y = pixel_index // width
        r, g, b = img.getpixel((x, y))
        if char == '0':
            # Set least significant bit to 0
            r &= 0b11111110
        else:
            # Set least significant bit to 1
            r |= 0b00000001
        img.putpixel((x, y), (r, g, b))
        pixel_index += 1

    # Save encoded image
    encoded_filename = image_filename.split('.')[0] + '_output.png'
    img.save(encoded_filename)
    return encoded_filename

# Example usage
image_filename = input("Enter file name ")
message = input("Enter message to be encoded ")
encoded_filename = encode_image(image_filename, message)
print(f'Encoded image saved as {encoded_filename}')

