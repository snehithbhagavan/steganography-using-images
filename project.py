from simpleimage import SimpleImage
from cryptography.fernet import Fernet

headstart = '$#@fdgs#@123 '  # String used in decoding to check wether the image used to decode is encoded or not



def image_input():
    '''

    This function takes the image to be encoded and returns that image to encode function

    '''

    s = input("Please enter image path or press enter to use default image\n")
    if s == '':
        original = SimpleImage('default.jpeg')
    else:
        original = SimpleImage(s)
    print("Image before encoding is")
    original.show()

    return original



def generate_key():
    '''

    a key is create by using thus function
    this key is used both used to encrypt the data ,
    and also used to decrypt the data

    '''
    key = Fernet.generate_key()
    with open("cryptography.key", 'wb') as key_file:
        key_file.write(key)



def load_key():
    '''

    this function opens the key file
    and returns the key in readable format ,from the key file

    '''

    return open("cryptography.key", 'rb').read()



def pixel_count(image):
    # this function takes image as parameter and returns number of pixels present in that image
    i = 0
    for pixel in image:
        i += 1
    return i



def encrypt(message):
    '''

    This function takes the message we want to transmit as input,
    and returns the encrypted value of the message.

    '''

    key = load_key()
    # by using the generated key ,
    # the input message is encrypted using cryptography library
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    # the encrypted message is returned

    return encrypted_message



def image_encode():
    """

    This function encodes the message with the image

    """
    image = image_input()
    generate_key()
    message = input('Please enter the message to be encoded\n')
    message = str(encrypt(message))
    print("The encrypted message is\n",message)
    message = headstart + message
    if (len(message) + 3) * 3 > pixel_count(image):
        print("message is too long to encode it with image")
        return

    tmp = 0
    x = 0
    y = 0

    for ch in message:

        binary_value = format(ord(ch), '08b')  # character to binary

        # this else if ladder is to get 3 pixels from image to encode message character by character
        if (x == image.width - 2):
            p1 = image.get_pixel(x, y)
            p2 = image.get_pixel(x + 1, y)
            p3 = image.get_pixel(0, y + 1)
            x = 1
            y += 1
        elif x == image.width - 1:
            p1 = image.get_pixel(x, y)
            p2 = image.get_pixel(0, y + 1)
            p3 = image.get_pixel(1, y + 1)
            x = 2
            y += 1
        else:
            p1 = image.get_pixel(x, y)
            p2 = image.get_pixel(x + 1, y)
            p3 = image.get_pixel(x + 2, y)

        # this else if ladder is to encode character into 3 pixels
        if binary_value[0] == '0' and p1.red % 2 != 0:
            if p1.red == 255:
                p1.red -= 1
            else:
                p1.red += 1
        elif binary_value[0] == '1' and p1.red % 2 == 0:
            p1.red += 1

        if binary_value[1] == '0' and p1.green % 2 != 0:
            if p1.green == 255:
                p1.green -= 1
            else:
                p1.green += 1
        elif binary_value[1] == '1' and p1.green % 2 == 0:
            p1.green += 1

        if binary_value[2] == '0' and p1.blue % 2 != 0:
            if p1.blue == 255:
                p1.blue -= 1
            else:
                p1.blue += 1
        elif binary_value[2] == '1' and p1.blue % 2 == 0:
            p1.blue += 1

        if binary_value[3] == '0' and p2.red % 2 != 0:
            if p2.red == 255:
                p2.red -= 1
            else:
                p2.red += 1
        elif binary_value[3] == '1' and p2.red % 2 == 0:
            p2.red += 1

        if binary_value[4] == '0' and p2.green % 2 != 0:
            if p2.green == 255:
                p2.green -= 1
            else:
                p2.green += 1
        elif binary_value[4] == '1' and p2.green % 2 == 0:
            p2.green += 1

        if binary_value[5] == '0' and p2.blue % 2 != 0:
            if p2.blue == 255:
                p2.blue -= 1
            else:
                p2.blue += 1
        elif binary_value[5] == '1' and p2.blue % 2 == 0:
            p2.blue += 1

        if binary_value[6] == '0' and p3.red % 2 != 0:
            if p3.red == 255:
                p3.red -= 1
            else:
                p3.red += 1
        elif binary_value[6] == '1' and p3.red % 2 == 0:
            p3.red += 1

        if binary_value[7] == '0' and p3.green % 2 != 0:
            if p3.green == 255:
                p3.green -= 1
            else:
                p3.green += 1
        elif binary_value[7] == '1' and p3.green % 2 == 0:
            p3.green += 1

        tmp += 1

        if (tmp == len(message)):  # to decide wether the message is ended or not
            if p3.blue % 2 == 0:
                p3.blue += 1
        else:
            if p3.blue % 2 != 0:
                if p3.blue == 255:
                    p3.blue -= 1
                else:
                    p3.blue += 1

        if (x == image.width - 3):
            x = 0
            y += 1
        else:
            x += 3

    print("The modified image after encoding is ")
    image.show()
    image.pil_image.save('output.png')



def decrypt_message(encrypted_msg):
    '''

    :param encrypted_msg:  takes the encrypted message as input
    :return: the decrypted value of the encrypted message

    '''

    key = load_key()
    f = Fernet(key)
    decrypted_msg = f.decrypt(encrypted_msg)
    return decrypted_msg.decode()



def image_decode():
    '''

    This function is used for decoding the image.
    It check whether a message is encoded inside the image or not ,
    if image is encoded , then it calls decrypt function ,
    and prints the message.

    '''

    s = input("Please enter the path of the image to decode\n")
    new_image = SimpleImage(s)
    # while decoding the image ,the binary format of the characters is added this binary_num string
    binary_num = ''
    # while decoding the image , the characters are added to the message_1 string
    message_1 = ''
    for pixel in new_image:
        r = pixel.red
        b = pixel.blue
        g = pixel.green
        # Checking RGB value for each pixel
        # If the value is even , that means the message was encoded as '0'
        # ,so '0' is concatenated to the binary_num
        # if the number is odd . that means the message was encoded as '1'
        # ,so '1' is concatenated to the binary_num
        if r % 2 == 0:
            binary_num += '0'
        else:
            binary_num += '1'
        if g % 2 == 0:
            binary_num += '0'
        else:
            binary_num += '1'
        if b % 2 == 0:
            binary_num += '0'
        else:
            binary_num += '1'
        if len(binary_num) == 9:
            # for every time the binary_num 's length becomes 9 letters ,
            # it means ,we went through 3 pixels,
            # so we convert it into the respective character
            message_1 += chr(int(binary_num[:8], 2))

            if binary_num[8] == '1':
                # the last character in the binary_num is odd,
                # which means that the message ends there,hence we break
                break

            if len(message_1) == len(headstart):
                # to check whether the message is encoded inside the image or not

                if message_1 != headstart:

                    # if the headstart doesnt match ,
                    # then the image doesnt have any encoded message inside
                    print('No message was previously encoded with this image before')
                    return

            # after the necessary information is deducted from the binary_num ,
            # the string is again made empty ,for the next 3 pixels.
            binary_num = ''

    # converting message_1 from str to bytes
    message_1 = message_1[len(headstart) + 2:-1]
    message = bytes(message_1, 'utf-8')

    try:
        message = decrypt_message(message)
        print("The message which was encoded with this image is\n", message)
    except:
        print("No message was previously encoded with this image before")




def main():

    a = int(input("Press\n1)ENCODE\n2)DECODE\n"))

    while True:
        if a == 1:
            image_encode()
            break
        elif a == 2:
            image_decode()
            break
        else:
            print("Please enter a valid number")



if __name__ == '__main__':

    print("THIS PROGRAM ALLOWS YOU TO ENCRYPT A MESSAGE AND THEN ENCODE IT INTO AN IMAGE.")
    print("THE SAME CAN BE DECODED AND DECRYPTED USING THIS PROGRAM")

    main()
