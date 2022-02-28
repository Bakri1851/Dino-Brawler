import socket
from _thread import start_new_thread
from game import Game
from player import Player
import pickle

server = socket.gethostbyname(
    socket.gethostname())  # this will be my local ip address. i get it from command prompt when typing ipconfig
# 192.168.178.35
port = 5555  # this is the port I will use for the connections

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket I will use for final product

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()  # this opens up the ports to allow connections
print("Waiting for connection, Server started")  # server is now running

connected = set()  # this will store ip addresses of the connected clients
games = {}  # this will store our games
idCount = 0  # this will keep track of the current id's


def threaded_client(my_connection, player, gameId):  # conn = connection
    global idCount
    my_connection.send(pickle.dumps(games[gameId].players[player]))  # this will convert to string and send it to the player

    while True:
        try:
            data = pickle.loads(my_connection.recv(
                2048 * 10))
            if gameId in games:

                games[gameId].players[player] = data

                if not data:
                    break
                else:

                    if player == 1:
                        reply = games[gameId].players[0]
                    else:
                        reply = games[gameId].players[1]

                    my_connection.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break  # if anything else happens the loop will end so no infinite loop

    print("Lost connection")  # this will show that the connection has been

    try:
        del games[gameId]
        print("Closing game", gameId)
    except:
        pass
    idCount -= 1
    connection.close()  # this will close the connection so we can possibly reopen it in the future


while True:  # this while loop will continuously look for connections
    connection, address = s.accept()
    print("Connected to:", address)

    idCount += 1
    player = 0
    gameId = (idCount - 1) // 2

    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating new game...")
        games[gameId].ready = False
        games[gameId].players[0].id = gameId
    else:
        games[gameId].ready = True
        player = 1
        games[gameId].players[1].id = gameId

    start_new_thread(threaded_client, (connection, player, gameId))
    print(idCount)
    print(gameId)
    print(games[gameId].ready)
