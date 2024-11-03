import socket
import random
import sys
import time

class Packet:
    def __init__(self,Data, Source, Destination):
        self.data = Data
        self.source = Source
        self.destination = Destination
    def __str__(self):
        return f"Packet from {self.source} to {self.destination} with data: {self.data}"

def Join_Ring(send_port, rec_port, buffer_size, head_node, node_num):
    buffer = [Packet(f"Initial packet {i}", node_num, random.choice([1, 2, 3])) for i in range(buffer_size)]
    if head_node:
        time.sleep(2)  # Give other nodes time to start
        print(f"Node {node_num}: I am the head node. Initializing token.")
        print("Sending packet out to internet...")
        if buffer:
            print(f"Sending packet: {buffer.pop(0)}")
        print(f"Updated Buffer Size: {len(buffer)}")
        sys.stdout.flush()
        Send_Token(send_port)

    while True:
        print(f"Node {node_num}: Waiting to receive token on port {rec_port}. Head Node: {head_node}. Buffer Size: {len(buffer)}")
        sys.stdout.flush()
        if Rec_Token(rec_port):
            if buffer:
                print(f"Node {node_num}: Sending packet to internet...")
                print(f"Sending packet: {buffer.pop(0)}")
                print(f"Updated Buffer Size: {len(buffer)}")
                sys.stdout.flush()
                Send_Token(send_port)
                Maybe_Add_To_Buffer(buffer, 0.25, node_num)
            else:
                print(f"Node {node_num}: Nothing to send, sending token to next node's port: {send_port}")
                sys.stdout.flush()
                Send_Token(send_port)
                Maybe_Add_To_Buffer(buffer, 0.25, node_num)

def Maybe_Add_To_Buffer(buffer, probability, node_num):
    if random.random() < probability:
        new_packet = Packet("Hello weary traveler", node_num, random.choice([1, 2, 3])) #Added weary traveler for morale boost
        buffer.append(new_packet)
        print(f"Packet added to buffer: {new_packet}")

 
def Send_Token(send_port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sendSock:
            sendSock.connect(('localhost', send_port))
            sendSock.sendall(b'TOKEN')
        print(f"Token sent to port {send_port}")
    except Exception:
        print(f"Error sending token to port {send_port}: {Exception}")

def Rec_Token(rec_port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as recSock:
            recSock.bind(('localhost', rec_port))
            recSock.listen(1)
            print(f"Listening on port {rec_port}")
            conn, addr = recSock.accept()
            with conn:
                token = conn.recv(1024)
                if token:
                    print(f"Token received on port {rec_port} from {addr}")
                    return True
    except Exception:
        print(f"Error receiving token on port {rec_port}: {Exception}")
    return False

if __name__ == "__main__":  #Want to be ran as a script
    if len(sys.argv) != 6:
        print("Invalid input, try as follows: python node.py <send_port> <rec_port> <buffer_size> <is_head> <node_num>") #insturctions for use
        sys.exit(1)
    else:
      send_port = int(sys.argv[1])
      rec_port = int(sys.argv[2])
      buffer_size = int(sys.argv[3])
      is_head = int(sys.argv[4]) == 1
      node_num = int(sys.argv[5])
      Join_Ring(send_port, rec_port, buffer_size, is_head, node_num)