"""
Filename: network_chat_client.py
Author: Lee Dillard
Created: 04/06/2024
Purpose: A simple network chat client
"""
import socket

# Use 127.0.0.1 if you are running the server program
# on the same computer you are running the client program
# Change the IP address if the server program
# is on another computer
SERVER_IP = "127.0.0.1"

# specify the destination port
PORT = 8081

def main():
    # Create TCP/IP IPV4 socket
    client_socket = socket.socket(
        socket.AF_INET,             # TCP/IP v4 address
        socket.SOCK_STREAM          # Create TCP socket
    )

    # Connect to the server on a specified IP address and port
    client_socket.connect((SERVER_IP, PORT))

    while True:
        # Get message from user
        message = input("Client>> ")

        if (message == 'q'):
            # Send byte encoded message to server
            client_socket.send(message.encode("utf-8"))

            client_socket.close()
            quit()

        else:
            # Send byte encoded message to server
            client_socket.send(message.encode("utf-8"))

            # Receive response from server
            message = client_socket.recv(1024)

            # Print decoded byte message
            print(f">> {message.decode('utf-8')}")

main()