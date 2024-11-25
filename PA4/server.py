import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

# Constants
SECRET = "csci466"
KEY = "0123456789ABCDEF"
HOST = 'localhost'
PORT = 8010

def decryptMessage(encryptedMessage, key):
    try:
        blockCipher = AES.new(key.encode(), AES.MODE_ECB)
        return unpad(blockCipher.decrypt(encryptedMessage), 32).decode()
    except Exception as e:
        raise Exception(f"Decryption error: {str(e)}")

def computeMac(message, secret):
    combined = (message + secret).encode()
    return hashlib.sha256(combined).hexdigest()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Server listening on port {PORT}...")

    try:
        while True:
            client_socket, address = server_socket.accept()
            print(f"Connection from {address}")
            
            try:
                while True:
                    msgLengthBytes = client_socket.recv(4)
                    if not msgLengthBytes:
                        print("Client disconnected")
                        break
                        
                    msgLength = int.from_bytes(msgLengthBytes, 'big')
                    print(f"\nReceiving message of length: {msgLength} bytes")
                    encryptedMessage = b''
                    while len(encryptedMessage) < msgLength:
                        chunk = client_socket.recv(min(msgLength - len(encryptedMessage), 1024))
                        if not chunk:
                            break
                        encryptedMessage += chunk
                    
                    print(f"Received encrypted message (hex): {encryptedMessage.hex()}")
                    receivedMac = client_socket.recv(64).decode()
                    print(f"Received MAC: {receivedMac}")
                    
                    try:
                        decryptedMessage = decryptMessage(encryptedMessage, KEY)
                        print(f"Successfully decrypted message: {decryptedMessage}")
                        computedMac = computeMac(decryptedMessage, SECRET)
                        print(f"Computed MAC: {computedMac}")
                        if receivedMac == computedMac:
                            print("Packet ACCEPTED - MACs match")
                            client_socket.send("Packet ACCEPTED".encode())
                        else:
                            print("Packet REJECTED - MACs do not match")
                            client_socket.send("Packet REJECTED".encode())
                            
                    except Exception as e:
                        errorMsg = f"Error: {str(e)}"
                        print(errorMsg)
                        client_socket.send(errorMsg.encode())
                    
            except ConnectionResetError:
                print("Client disconnected unexpectedly")
            finally:
                client_socket.close()
                
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()