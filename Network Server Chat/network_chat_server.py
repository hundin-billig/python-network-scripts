"""
Filename: network_chat_server.py
Author: Lee Dillard
Created: 04/06/2024
Purpose: A simple network chat server
"""

# Import socket library
import socket

# The server will accept a connection on any interface
SERVER_IP = ""

# Port to listen in on (non-privileged ports are > 1023)
# Listening server port
PORT = 8081

def main():
    # Create a socket object
    server_socket = socket.socket(
        socket.AF_INET,             # TCP/IP v4 address
        socket.SOCK_STREAM          # Create TCP transport layer socket
    )

    # Bind host IP/name and port number to socket
    server_socket.bind((SERVER_IP, PORT))

    # Start server socket listener
    server_socket.listen()

    print(f"Listening for incoming connections on port {PORT}...")

    # Accept a connection from a client, return socket object and IP address
    connection, address = server_socket.accept()
    print(f"Connection from {address}")

    while True:
        # Receive data into a 1024 byte buffer
        data = connection.recv(1024).decode("utf-8")

        if (data == "q"):
            # Close the connection
            connection.close
            print("Client disconnected")
            print(f"Listening for incoming connections on port {PORT}...")    

            # Ready for a new client connection
            connection, address = server_socket.accept()
            print(f"Connection from: {address}")
        else:
            # Print the client message
            print(f">> {data}")

            # Get a message from the user
            message = input("Server>> ")

            # Send message to client
            connection.send(message.encode("utf-8"))

main()