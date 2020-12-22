# Import libraries
from socket import *
import tcp_server, udp_server

# Let the user set the maximum number of users in chatroom
N = int(input("What is the maximum number of users in chatroom? "))

# Let the user to choose which protocol to use in runtime
selected_protocol = None
while selected_protocol not in {"UDP", "TCP"}:
    selected_protocol = input("What protocol (UDP or TCP) do you want to use? ",).upper()
    if selected_protocol not in {"UDP", "TCP"}:
        print("Please either type UDP or TCP! Try again! ")
print("Ok! You selected",selected_protocol)

if selected_protocol == 'TCP':
    tcp_server.start(N)

if selected_protocol == 'UDP':
    udp_server.start(N)