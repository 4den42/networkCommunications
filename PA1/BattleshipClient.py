import socket
import sys
def print_board(hits, misses):
    # Create a board with '?' for all cells
    board = [['?' for _ in range(6)] for _ in range(6)]
    
    # Mark hits with 'X' and misses with 'O'
    for (row, col) in hits:
        board[row][col] = 'X'  # Mark hits with 'X'
    for (row, col) in misses:
        board[row][col] = 'O'  # Mark misses with 'O'
 # Print the board
    for row in board:
        print(' '.join(row))
    print()

def main(port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()

    try:
        client_socket.connect((host, port))
    except ConnectionRefusedError:
        print(f"Connection to {host}:{port} refused. Is the server running?")
        return

    guesses = 0
    global misses
    global hits  # Keep track of hits
    hits = set()
    misses = set()

    while True:
        print_board(hits,misses)  # Display the board with hits and misses
        guess = input("Enter your guess (row col): ")
        try:
            row, col = map(int, guess.split())
            if row < 0 or row > 5 or col < 0 or col > 5:
                print("Please enter numbers between 0 and 5.")
                continue
            if (row, col) in hits:
                print("You already guessed that!")
                continue
            
            guesses += 1
   #         hits.add((row, col))  # Add the guess to the hits set
            client_socket.send(guess.encode())
            response = client_socket.recv(1024).decode()
            print(response)

            # Check if it's a hit and update the hits set accordingly
            if response == "Hit":
                hits.add((row, col))
                print(f"You hit a battleship at ({row}, {col})!")
            elif response == "Miss":
                misses.add((row, col))
                print(f"You missed at ({row}, {col}).")

            if response == "Game Over":
                print(f"You've sunk all the battleships in {guesses} turns!")
                break
        except ValueError:
            print("Invalid input. Please enter two integers.")

    client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python client.py [PORT_NUMBER]")
        sys.exit(1)

    port_number = int(sys.argv[1])
    main(port_number)
