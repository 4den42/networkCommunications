import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import random

# Constants
SECRET = "csci466"
KEY = "0123456789ABCDEF"
HOST = 'localhost'
PORT = 8010

def encryptMessage(message, key):
    try:
        blockCipher = AES.new(key.encode(), AES.MODE_ECB)
        return blockCipher.encrypt(pad(message.encode(), 32))
    except Exception as e:
        raise Exception(f"Encryption error: {str(e)}")

def computeMac(message, secret):
    combined = (message + secret).encode()
    return hashlib.sha256(combined).hexdigest()

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print(f"Connecting to {HOST}:{PORT}...")
        client_socket.connect((HOST, PORT))
        print("Connected successfully!")
        
        while True:
            # Get message from user
            message = input("\nEnter message to send (or 'quit' to exit): ")
            if message.lower() == 'quit':
                break
                
            try:
                # 1. Encrypt the message
                encryptedMessage = encryptMessage(message, KEY)
                print(f"\nOriginal message: {message}")
                print(f"Encrypted message (hex): {encryptedMessage.hex()}")
                
                # 2. Compute MAC (H(m+s))
                originalMac = computeMac(message, SECRET)
                mac = originalMac
                print(f"Original MAC: {originalMac}")
                
                # 3. Determine if message should be corrupted (50% chance)
                isCorrupted = random.random() <= 0.50
                if isCorrupted:
                    print("\nMessage corrupted! Tampering with the message...")
                    tamperedMessage = "tampered_" + message
                    mac = computeMac(tamperedMessage, SECRET)
                    print(f"New MAC after tampering: {mac}")
                
                # 4. Send message length first
                msgLength = len(encryptedMessage)
                print(f"Sending message length: {msgLength} bytes")
                client_socket.send(msgLength.to_bytes(4, 'big'))
                
                # 5. Send encrypted message
                print("Sending encrypted message...")
                client_socket.send(encryptedMessage)
                
                # 6. Send MAC
                print("Sending MAC...")
                client_socket.send(mac.encode())
                
                # 7. Wait for server response
                print("\nWaiting for server response...")
                response = client_socket.recv(1024).decode()
                print(f"Server response: {response}")
                
            except Exception as e:
                print(f"\nError occurred: {str(e)}")
                break
                
    except ConnectionRefusedError:
        print("\nError: Could not connect to server. Is the server running?")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
    finally:
        print("\nClosing connection...")
        client_socket.close()

if __name__ == "__main__":
    main()