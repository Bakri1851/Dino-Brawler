import socket
from _thread import start_new_thread
from game import Game
from player import Player
import pickle

server = socket.gethostbyname(
    socket.gethostname())  # this will be my local ip address. i get it from command prompt when typing ipconfig
port = 5555  # this is the port I will use for the connections

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket I will use for final product

player1 = Player(400, 350, 48, 48, 10000, 100, 725, 100, 755, "RIGHT")
player2 = Player(810, 350, 48, 48, 10000, 900, 725, 900, 755, "LEFT",)
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


def threaded_client(my_connection, player, gameId, idCount):  # conn = connection
    my_connection.send(pickle.dumps(players[player]))  # this will convert to string and send it to the player
    #for x in range(0, 2):
    #    players[x] = player
    while True:
        try:
            data = pickle.loads(my_connection.recv(
                2048 * 10))
            players[player] = data
            if gameId in games:

                if not data:
                    break
                else:

                    if player == 1:
                        reply = players[0]
                    else:
                        reply = players[1]

                    my_connection.sendall(pickle.dumps(reply))


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
    connection.close()  # this will close the connection so we can possibly reopen it in the future


while True:  # this while loop will continuously look for connections
    connection, address = s.accept()
    print("Connected to:", address)

    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2

    if idCount % 2 == 1:
        games[gameId] = Game(gameId, players)
        print("Creating new game...")
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (connection, p, gameId, idCount))
    print(idCount)
    print(gameId)
    print(games[gameId].ready)
