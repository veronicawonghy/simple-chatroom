import socket
import errno
import select
import sys

name = None

def start():
    # server name and port
    serverName = 'localhost'
    serverPort = 12000

    try:
        # TCP
        # Persistent (kept alive after each packet transmission)
        # Create socket
        while True:
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect((serverName,serverPort))

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
                        # the connection is rejected
                        if receivedMessage == "":
                            print("The chatroom is full!!!")
                            quit() # exit the program
                        print (receivedMessage)  

                    # read from command line
                    else:  
                        # read what user type in the command line
                        message = sys.stdin.readline().rstrip()  
                        clientSocket.send(message.encode())  

            
# Handle errors in socket programming (e.g., assigned port being occupied by other programs, client resetting the connections).
    except socket.error as e:
        if e.errno == 61:
            print("ERROR: The connection is refused. Check your server and server port #!")  
        elif e.errno == 54: 
            print("ERROR: Lost server connection, please check your server!")  
        else:
            print(e)
