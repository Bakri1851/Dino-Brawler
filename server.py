import socket
from _thread import *
from player import *
import pickle
import sys


server = "127.0.0.1"  # this will be my local ip address. i get it from command prompt when typing ipconfig
port = 5555  # this is the port I will use for the connections

# Home IP address = 192.168.178.35
# Hotspot IP address  = 172.20.10.2

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket I will use for final product

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()  # this opens up the ports to allow connections
print("Waiting for connection, Server started")  # server is now running
player1 = Player(400, 350, 48, 48, (255, 0, 0), 10000, 100, 100)
player2 = Player(810, 350, 48, 48, (0, 0, 255), 10000, 900, 100)
players = [player1, player2]

connected = set()  # this will store ip addresses of the connected clients
games = {}  # this will store our games
idCount = 0  # this will keep track of the current id's


def run_server(my_server, my_port, s):
    try:
        s.bind((my_server, my_port))  # looks for certain connections
    except socket.error as e:
        str(e)

    def threaded_client(my_conn, player):  # conn = connection
        my_conn.send(pickle.dumps(players[player]))  # this will convert to string and send it to the player
        reply = ""
        while True:
            try:
                data = pickle.loads(my_conn.recv(
                    2048))
                players[player] = data

                if not data:
                    print("Disconnected")
                    break
                else:
                    if player == 1:
                        reply = players[0]

                    else:
                        reply = players[1]

                    print("Received:", data)  # this will print the data that was received
                    print("Sending :", reply)  # this will print the data that was sent

                my_conn.sendall(pickle.dumps(reply))
            except:
                break  # if anything else happens hte loop will end so no infinite loop

        print("Lost connection")  # this will show that the connection has been lost
        conn.close()  # this will close the connection so we can possibly reopen it in the future

    currentPlayer = 0
    while True:  # this while loop will continiously look for connections
        conn, addr = s.accept()
        print("Connected to:", addr)

        start_new_thread(threaded_client, (conn, currentPlayer))
        currentPlayer += 1


run_server(server, port, s)
