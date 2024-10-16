import socket
import random
import sys

# Declare the global variable at the top if needed
ship_positions = set()

def generate_board():
    global ship_positions  # Declare it as global here if you're modifying it
    board = [['?' for _ in range(6)] for _ in range(6)]
    ships = [(4, 'X'), (3, 'X'), (2, 'X')]

    for length, identifier in ships:
        on_board = False
        while not on_board:
            placed = random.choice(['H', 'V'])
            row = random.randint(0, 5)
            col = random.randint(0, 5)

            if placed == 'H' and col + length <= 6:
                if all(board[row][col + i] == '?' for i in range(length)):
                    for i in range(length):
                        board[row][col + i] = identifier
                        ship_positions.add((row, col + i))
                    on_board = True
            elif placed == 'V' and row + length <= 6:
                if all(board[row + i][col] == '?' for i in range(length)):
                    for i in range(length):
                        board[row + i][col] = identifier
                        ship_positions.add((row + i, col))
                    on_board = True
    return board

def main(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(1)
    board = generate_board()
    print("Battleship board generated!")

    connection, addr = server_socket.accept()
    print(f"Connected by {addr}")

    hits = set()
    while True:
        try:
            for row in board:
                print(' '.join(row))

            data = connection.recv(1024).decode()
            if not data:
                print("No data received; closing connection.")
                break

            row, col = map(int, data.split())
            if (row, col) in hits:
                response = "Already guessed"
            else:
                hits.add((row, col))
                if board[row][col] == 'X':
                    response = "Hit"
                    board[row][col]= 'X'
                else:
                    response = "Miss"
                    board[row][col]= 'O'
                
                if ship_positions.issubset(hits):
                    connection.send("Game Over".encode())
                    print("All ships have been sunk! Game Over.")
                    break

            connection.send(response.encode())

        except (ValueError, IndexError):
            response = "Invalid guess. Please enter row and column between 0 and 5."
            connection.send(response.encode())
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    connection.close()
    server_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py [PORT_NUMBER]")
        sys.exit(1)

    port_number = int(sys.argv[1])
    main(port_number)
