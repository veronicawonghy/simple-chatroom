# Import libraries
from socket import *
import threading

client_list = []
name_list = []

def createNewThread(connectionSocket, clientAddress):
    # greeting message
    connectionSocket.sendall("Welcome to the chatroom! Please choose a username:".encode())
    
    # loop until user uses an unique username
    while True:
        name = str(connectionSocket.recv(1024).decode()).rstrip()
        # check if the name is taken
        if(name not in name_list):
            name_list.append(name)
            message = "Welcome, "+name+"! Now you can start sending messages!"
            connectionSocket.sendall(message.encode())
            # notification message
            broadcast(connectionSocket,name+" has entered the chatroom...")
            print(name+" has entered the chatroom...")
            break
        # ask for another name
        connectionSocket.sendall("Sorry, this username has been taken, consider another one?".encode())

    # loop until connection close
    while True:
        ## When receive a message from client, read
        receivedMessage = connectionSocket.recv(1024).decode()
        
        if receivedMessage == "":
            connectionSocket.close()
            remove(connectionSocket)
            break

        message = "<"+name+">"+" "+receivedMessage
        print(message)

        ## broadcast
        broadcast(connectionSocket,message)

def broadcast(clientAddress,message):
    for index, client in enumerate(client_list):
        if client != clientAddress:
            try:
                client.sendall(message.encode())
            except:
                client.close()
                remove(client)

def remove(connectionSocket):
    if connectionSocket in client_list:
        message = name_list[client_list.index(connectionSocket)]+" has left the chatroom..."
        print(message)
        del name_list[client_list.index(connectionSocket)]
        client_list.remove(connectionSocket)

def start(N):
    # ask for server name and port?
    serverPort = 12000
    
    try:
        # TCP
        ## Persistent server (kept alive)
        ## create socket
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.bind(("",serverPort))

        ## wait for incoming connection request
        serverSocket.listen(1)
        print ('The server is ready to receive')

        while True:
            connectionSocket, clientAddress = serverSocket.accept()
            if len(client_list)>=N:
                message = "<"+str(clientAddress[0])+","+str(clientAddress[1])+"> was blocked"
                print(message)
                connectionSocket.close()
                continue
            client_list.append(connectionSocket)
            thread = threading.Thread(target=createNewThread, args=(connectionSocket, clientAddress,))
            thread.start()

    except Exception as e:
        print(e)
        
