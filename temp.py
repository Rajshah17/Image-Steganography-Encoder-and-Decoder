import numpy as np

from PIL import Image

def hide_message_in_image(image_path, message):
    # open the image and convert it to a numpy array
    image = Image.open(image_path)
    image_array = np.array(image)

    # convert the message to a binary string
    binary_message = ''.join(format(ord(c), '08b') for c in message)

    # make sure the message will fit in the image
    image_shape = np.array(image).shape[:2]
    max_message_length = np.product(image_shape) - 8
    if len(binary_message) > max_message_length:
        raise ValueError(f'Message too long to hide in image (max length: {max_message_length})')

    # add a stop bit to the message to indicate where it ends
    binary_message += '00000000'

    # flatten the image array into a 1D array
    flat_image_array = image_array.ravel()

    # modify the least significant bit of each pixel value to store a bit of the message
    for i, bit in enumerate(binary_message):
        pixel_index = i * 8
        if pixel_index >= len(flat_image_array):
            break
        if bit == '1':
            flat_image_array[pixel_index] |= 1
        else:
            flat_image_array[pixel_index] &= ~1

    # reshape the modified array back into an image and save it
    modified_image_array = flat_image_array.reshape(image_array.shape)
    modified_image = Image.fromarray(modified_image_array)
    modified_image.save(f'{image_path.split(".")[0]}-modified.png')

# def extract_hidden_message(image_path):
#     # open the image and convert it to a numpy array
#     image = Image.open(image_path)
#     image_array = np.array(image)

#     # extract the message from the least significant bit of each pixel value
#     binary_message = ''
#     for pixel_value in image_array.flat:
#         binary_message += str(pixel_value & 1)

#     # find the stop bit and extract the message
#     stop_bit_index = binary_message.find('00000000')
#     if stop_bit_index == -1:
#         raise ValueError('Stop bit not found in image')
#     binary_message = binary_message[:stop_bit_index]

#     # convert the binary message to ASCII
#     message = ''
#     for i in range(0, len(binary_message), 8):
#         message += chr(int(binary_message[i:i+8], 2))

#     return message

def extract_message_from_image(image_path):
    # open the image and convert it to a numpy array
    image = Image.open(image_path)
    image_array = np.array(image)

    # extract the message from the least significant bit of each pixel value
    binary_message = ''
    for pixel_value in image_array.flat:
        binary_message += str(pixel_value & 1)

    # find the stop bit and extract the message
    stop_bit_index = binary_message.find('00000000')
    if stop_bit_index == -1:
        raise ValueError('Stop bit not found in image')
    binary_message = binary_message[:stop_bit_index]

    # convert the binary message to ASCII
    message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))

    return message


if __name__ == '__main__':
    # prompt the user for input
    input_path = input('Enter input image file name: ')
    message = input('Enter message to hide: ')

    # hide the message within the image
    hide_message_in_image(input_path, message)

    # extract the message from the image
    extracted_message = extract_message_from_image(f'{input_path.split(".")[0]}-modified.png')
    print('Extracted message:', extracted_message)

# def convert_to_unicode(string):
#     # convert the string to a byte string using the ISO-8859-1 encoding
#     byte_string = string.encode('iso-8859-1')

#     # decode the byte string as UTF-8
#     unicode_string = byte_string.decode('utf-8')

#     return unicode_string


# m1 = extracted_message
# unicode_message = convert_to_unicode(m1)
# print(unicode_message)
