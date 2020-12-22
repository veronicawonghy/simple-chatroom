# Import libraries
import socket
import select
import sys

# server name and port
serverName = 'localhost'
serverPort = 12000

name = None

def start():
    print("Welcome to the chatroom! Please choose a username:")
    try:
        # UDP
        # Create socket
        clientSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        
        while True:
                # the input from command line , from socket
                sockets_list = [sys.stdin, clientSocket]  

                # get the list of sockets
                # non blocking
                # select.select(rlist, wlist, xlist[, timeout])¶
                read_sockets, w, e = select.select(sockets_list,[],[])  
  
                for sock in read_sockets:  
                    # if server sends msg and in the rlist waiting
                    if sock == clientSocket:  
                        receivedMessage = sock.recv(1024).decode()
                        # receivedMessage, serverAddress = clientSocket.recvfrom(2048)

                        # the connection is rejected
                        if receivedMessage == "":
                            print("The chatroom is full!!!")
                            quit() # exit the program
                        print (receivedMessage)  

                    # read from command line
                    else:  
                        # read what user type in the command line
                        message = sys.stdin.readline().rstrip()  
                        if message == "bye":
                            print("leaving the chatroom...")
                            clientSocket.sendto(message.encode(),(serverName, serverPort))
                            # close the socket
                            clientSocket.close()
                            quit() # exit the program
                        clientSocket.sendto(message.encode(),(serverName, serverPort)) 

    # Handle errors in socket programming
    except socket.error as e:
        print(e)