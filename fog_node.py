
"""
 Python3 Fog node Simulator
 Simulates a Fog server which
 accepts connections a and transmits
 collision information to participants
 It stores a list of active clients and 
 their locations

Created by: savavel
Last Edited: 10 May, 2018
"""


from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import _thread
import time
import datetime
import json
from queue import Queue

# Configure host and ports
host = '0.0.0.0'
port = 1234
buf = 1024

addr = (host, port)

# Setup server socket
serversocket = socket(AF_INET, SOCK_STREAM)
serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serversocket.bind(addr)
serversocket.listen(10)

# Create a dictionary of clients and their parameters
clients = {}
flags = {}


"""
 Handler thread which checks the payload
 of every received request from a client and
 assigns their parameters such as location and speed
"""
def handler(clientsocket, clientaddr):
    print("Accepted connection from: ", clientaddr)
    while True:
        bin_data = clientsocket.recv(buf)
        data_utf8 = bin_data.decode("utf8").rstrip()
        if "disconnect" in data_utf8 or "" == data_utf8:
            print("Disconnect: "+ str(clientaddr[1]))
            break

        data = json.loads(data_utf8)
        
        # assign location and speed to the clients
        if "location" in data:
            if clientsocket in clients:
                clients[clientsocket]['location'] = data['location']
                clientsocket.send(json.dumps({"location": data['location']}).encode("utf8"))
        if "speed" in data:
            if clientsocket in clients:
                clients[clientsocket]['speed'] = data['speed']
                clientsocket.send(json.dumps({"speed": data['speed']}).encode("utf8"))

        # Checks if there is collision info in the payload
        if "collision" in data:
            if clientsocket in clients:
                clients[clientsocket]['speed'] = data['speed']
                clients[clientsocket]['location'] = data['collision']

            clientsocket.send(json.dumps({"collision": data['collision']}).encode("utf8"))
            latitude,longitude = clients[clientsocket]['location'].split(',')

            # Alert all clients in the vicinity about the collision
            for client in clients:
                client_lat,client_lon = clients[client]['location'].split(',')
                if client_lat == latitude and client_lon == longitude:
                    print(client)
                    client.send(json.dumps({"collision": data['collision']}).encode("utf8"))

    # Remove client socket from dictionary if disconnected
    # and close thread
    del clients[clientsocket]
    clientsocket.close()
    return


# Periodically send a timestamp to vehicles 
# to check whether they are active
def push():
    while True:
        for socket in clients:
            socket.send(json.dumps({"time": str(datetime.datetime.now())}).encode("utf8"))
        time.sleep(10)

# Start the periodic pinging thread
_thread.start_new_thread(push, ())

# Begin listening for connections
while True:
    try:
        print("Server is listening for connections\n")
        clientsocket, clientaddr = serversocket.accept()
        clients[clientsocket] = {"location": "", "speed": ""}
        # Create thread when there is a new connection
        thread = _thread.start_new_thread(handler, (clientsocket, clientaddr))
    except KeyboardInterrupt:
        print("Closing server socket...")
        serversocket.close()
