import pygame
from network import Network  # this will import the network class from network file
from world import *
import pickle
import spritesheet

pygame.font.init()

width = 1250  # width of window
height = 700  # height of window
win = pygame.display.set_mode((width, height))  # Size of window
pygame.display.set_caption("MultiplayerTest")  # Cilent Name

# When connecting each player is allocated a different position on the map. The client will send new information and the other client position will be sent back to show movement

tile_size = 50

bg_img = pygame.image.load(
    r"C:\Users\Bakri\PycharmProjects\Coursework\Game Assets\Map Assets\2 Background\Background3.png")  # will load up background
world = World(world_data)

sprite_sheet_image = pygame.image.load('loki.png').convert_alpha()

sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

# create animation list
animation_list = []
animation_steps = [4, 6, 3, 4, 7, 4, 4, 4, 11]
action = 0
animation_cooldown = 125
step_counter = 0


def getanimations(sprite_sheet, animation_list, animation_steps):
    step_counter = 0
    for animation in animation_steps:
        temp_img_list = []
        for _ in range(animation):
            temp_img_list.append(sprite_sheet.get_image(step_counter, 24, 24, 3, (0, 0, 0)))
            step_counter += 1
        animation_list.append(temp_img_list)


getanimations(sprite_sheet, animation_list, animation_steps)


def draw_grid():
    for line in range(0, 30):
        pygame.draw.line(win, (255, 255, 255), (0, line * tile_size), (width, line * tile_size))
        pygame.draw.line(win, (255, 255, 255), (line * tile_size, 0), (line * tile_size, height))


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((0, 0, 0))
        font = pygame.font.SysFont("Agency FB", 60)
        text = font.render("Join Game", True, (255, 0, 0))
        win.blit(text, (525, 350))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()


def main():
    run = True  # initiates while loop

    clock = pygame.time.Clock()

    n = Network()  # when we connect we will get the player starting position
    player = n.getP()

    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            player2 = n.send(player)
        except:
            run = False
            print("Couldn't get game")
            break

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

                pygame.quit()

            if player.current_health <= 0:
                loser_screen()
                run = False
            if player2.current_health <= 0:
                winner_screen()
                run = False
            redrawWindow(win, player, player2)
        player.move()
        player.attack(player, player2)
        redrawWindow(win, player, player2)


def redrawWindow(win, player, player2):
    win.fill((0, 0, 0))
    '''
    if not (player2.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", False, (255, 0, 0), True)
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:
    '''
    win.fill((0, 0, 0))
    # draws background onto the screen
    # win.blit(bg_img, (0, 0))

    # draws my tiles onto the screen
    world.draw()

    # draws grid onto the screen
    # draw_grid()

    # draws player characters onto the screen

    player.draw_character(win, animation_list)
    player2.draw_character(win, animation_list)

    player.display_health()
    player2.display_health()

    player.update()
    player2.update()
    pygame.display.update()


def loser_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((0, 0, 0))
        font = pygame.font.SysFont("Agency FB", 60)
        loser_text = font.render("YOU LOSE!!!", True, (255, 0, 0))
        win.blit(loser_text, (525, 350))
        play_again_text = font.render("Play Again???", True, (255, 255, 255))
        win.blit(play_again_text, (505, 550))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu_screen()


def winner_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((0, 0, 0))
        font = pygame.font.SysFont("Agency FB", 60)
        winner_text = font.render("YOU WIN!!!", True, (255, 255, 0))
        win.blit(winner_text, (525, 350))
        play_again_text = font.render("Play Again???", True, (255, 255, 255))
        win.blit(play_again_text, (505, 550))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu_screen()

                run = False


while True:
    menu_screen()
