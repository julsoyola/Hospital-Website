# this is just for the encryption

import socket
import hashlib
import hmac

def send_encrypted_message(message):
    # Define the server address and port to establish a socket connection
    HOST = 'localhost'
    PORT = 8888

    try:
        # Establish a socket connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

            # Create an HMAC key (you should use a secret key here)
            secret_key = b'secret_key'

            # Create an HMAC message
            hmac_obj = hmac.new(secret_key, message.encode(), hashlib.sha3_512)
            hmac_message = hmac_obj.digest()

            # Encrypt the HMAC message (you need to implement this part)
            # encrypted_hmac_message = encrypt_function(hmac_message)

            # Send the encrypted HMAC message
            # s.sendall(encrypted_hmac_message)

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False



