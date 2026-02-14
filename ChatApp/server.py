import socket
import threading

# connection Data
host = "127.0.0.1"  # localhost of my own PC
port = 55555  # Any unassigned high-number port

# Starting server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# List for clients and their nicknames
clients = []
nicknames = []


def broadcast(message):
    # sends message to all connected clients.
    for client in clients:
        client.send(message)
    # Deliverable: Save logs to file
    with open("chat_logs.txt", "a") as f:
        f.write(message.decode("utf-8") + "\n")


def handle(client):
    # Handle the connection for a single client.
    while True:
        try:
            # Receiving Messages from client
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing and closing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} left!".encode("utf-8"))
            nicknames.remove(nickname)
            break


def receive():
    #Listening to new connections.
    print("Server is listening...")
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        #Request and Store Nickname
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname is {nickname}")
        broadcast(f"{nickname} joined!".encode('utf-8'))
        client.send('Connected to server!'.encode('utf-8'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()
