import socket
from _thread import *
from player import *
import pickle
import sys

server = socket.gethostbyname(
    socket.gethostname())  # this will be my local ip address. i get it from command prompt when typing ipconfig
port = 5555  # this is the port I will use for the connections

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket I will use for final product

player1 = Player(400, 350, 48, 48, (255, 0, 0), 10000, 100, 100)
player2 = Player(810, 350, 48, 48, (0, 0, 255), 10000, 900, 100)
players = [player1, player2]

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()  # this opens up the ports to allow connections
print("Waiting for connection, Server started")  # server is now running

connected = set()  # this will store ip addresses of the connected clients
games = {}  # this will store our games
idCount = 0  # this will keep track of the current id's

'''
def threaded_client(my_conn, player):  # conn = connection
    my_conn.send(pickle.dumps(players[player]))  # this will convert to string and send it to the player
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

    print("Lost connection")  # this will show that the connection has been

    conn.close()  # this will close the connection so we can possibly reopen it in the future


currentPlayer = 0
while True:  # this while loop will continiously look for connections
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
'''


def threaded_client(my_conn, player, gameId):  # conn = connection
    global idCount
    my_conn.send(pickle.dumps(players[player]))  # this will convert to string and send it to the player
    while True:
        try:
            data = pickle.loads(my_conn.recv(
                2048))
            players[player] = data
            if gameId in games:
                reply = games[gameId]

                if not data:
                    break
                else:
                    if player == 1:
                        reply = players[0]
                    else:
                        reply = players[1]

                   # print("Received:", data)  # this will print the data that was received
                    #print("Sending :", reply)  # this will print the data that was sent

                    my_conn.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break  # if anything else happens hte loop will end so no infinite loop

    print("Lost connection")  # this will show that the connection has been

    try:
        del games[gameId]
        print("Closing game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()  # this will close the connection so we can possibly reopen it in the future


while True:  # this while loop will continiously look for connections
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2
    if idCount % 2 == 1:
        games[gameId] = players[0]
        print("Creating new game...")
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))
