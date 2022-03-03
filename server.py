import socket
from _thread import start_new_thread
from game import Game
import pickle

server = socket.gethostbyname(
    socket.gethostname())  # this will be my local ip address. i get it from command prompt when typing ipconfig
port = 5555  # this is the port I will use for the connections

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket I will use for final product

try:
    socket.bind((server, port))
except socket.error as error:
    str(error)

socket.listen()  # this opens up the ports to allow connections
print("Waiting for connection, Server started")  # server is now running

games = {}  # this will store our games
id_count = 0  # this will keep track of the current id's


def threaded_client(my_connection, player, game_id):  # conn = connection
    global id_count
    my_connection.send(pickle.dumps(games[game_id].players[player]))
    # this will convert to string and send it to the player

    while True:
        try:
            data = pickle.loads(my_connection.recv(
                2048 * 10))
            if game_id in games:

                games[game_id].players[player] = data

                if not data:
                    break
                else:
                    if player == 1:
                        reply = games[game_id].players[0]
                    else:
                        reply = games[game_id].players[1]

                    my_connection.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break  # if anything else happens the loop will end so no infinite loop

    print("Lost connection")  # this will show that the connection has been lost

    try:
        del games[game_id]
        print("Closing game", game_id)
    except:
        pass
    id_count -= 1
    connection.close()  # this will close the connection so we can possibly reopen it in the future


while True:  # this while loop will continuously look for connections
    connection, address = socket.accept()
    print("Connected to:", address)

    id_count += 1
    player = 0
    game_id = (id_count - 1) // 2

    if id_count % 2 == 1:
        games[game_id] = Game(game_id)
        print("Creating new game...")
    else:
        player = 1

    start_new_thread(threaded_client, (connection, player, game_id))
