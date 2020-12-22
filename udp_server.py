# Import libraries
from socket import *

# ask for server name and port?
serverPort = 12000

client_list = []
name_list = []

def broadcast(serverSocket,clientAddress, message):
    for index, client in enumerate(client_list):
        if client != clientAddress:
            try:
                serverSocket.sendto(message.encode(),client)
            except:
                print("broadcast error", client)


def remove(clientAddress):
    if clientAddress in client_list:
        message = name_list[client_list.index(clientAddress)]+" has left the chatroom..."
        print(message)
        del name_list[client_list.index(clientAddress)]
        client_list.remove(clientAddress)

def start(N):
    # UDP
    ## Create socket, port 
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(("", serverPort))
    print("The server is ready to receive")

    ## When receive a message from client
    while True:
        ## Read datagram from server socket
        receivedMessage, clientAddress = serverSocket.recvfrom(2048)
        message = receivedMessage.decode()
        # print(message)
        if (clientAddress not in client_list):
            if len(client_list)>=N:
                warningmessage = "<"+str(clientAddress[0])+","+str(clientAddress[1])+"> was blocked"
                print(warningmessage)
                serverSocket.sendto("".encode(),clientAddress)
                continue
            name = str(message).rstrip()
            # check if the name is taken
            if(name not in name_list):
                name_list.append(name)
                client_list.append(clientAddress)
                message = "Welcome, "+name+"! Now you can start sending messages!"
                serverSocket.sendto(message.encode(),clientAddress)
                # notification message
                broadcast(serverSocket,clientAddress,name+" has entered the chatroom...")
                print(name+" has entered the chatroom...")
            else:
                # ask for another name
                serverSocket.sendto("Sorry, this username has been taken, consider another one?".encode(),clientAddress)
        else:
            # client is leaving the chatroom
            if message == "bye":
                remove(clientAddress)
                continue
            else:
                ## find the name of client
                name = name_list[client_list.index(clientAddress)]
                ## wrap the message
                message = "<"+name+">"+" "+message
                ## print in server
                print(message)
                ## broadcast
                broadcast(serverSocket,clientAddress,message)

