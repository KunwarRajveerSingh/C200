import socket # ip + port
from threading import Thread # this is for to connect multiple client to the server

# create a socket for the server to listen to the clients and bind it to the port and ip address 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #tcp server AF_inet = ipv4, SOCK_STREAM = tcp

# giving the ip address and port number to the server
ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port)) # bind the server to the port and ip address 
server.listen() # to listen to the client and accept the connection

#  list to store all the clients that will connect to the server 
list_of_clients = []
nicknames = [] 

print("Server has started...")

# to receive the message from the client and broadcast it to all the clients except the sender client 
def clientthread(conn, nickname):
    conn.send("Welcome to this chatroom!".encode('utf-8')) # send message to client we use encode when we send message
    while True:
        try:
            message = conn.recv(2048).decode('utf-8') # we use decode when we receive message
            if message:
                print (message)

                broadcast(message, conn)
            else:
                remove(conn)
                remove_nickname(nickname)
        except:
            continue

# remove the client from the list when they are disconnected or the message is empty
def remove(conn):
    if conn in list_of_clients:
        list_of_clients.remove(conn)

def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)

# to broadcast the message to all the clients except the sender client
def broadcast(message, conn):
    for clients in list_of_clients:
        if clients != conn:
            try:
                clients.send(message.encode('utf-8'))
            except:
                remove(clients)

# to start the server and to accept the client and start the thread for the client
while True:
    conn, addr = server.accept()
    conn.send("NICKNAME".encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    nicknames.append(nickname)
    list_of_clients.append(conn)
    print(conn, addr)
    print (addr[0] + " connected")
    message = "{} connected".format(nickname)
    print(message)
    broadcast(message, conn)
    new_thread = Thread(target = clientthread,args=(conn,nickname))
    new_thread.start()

