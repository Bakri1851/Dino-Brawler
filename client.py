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

sprite_sheet_image = pygame.image.load('doux.png').convert_alpha()
sprite_sheet_image2 = pygame.image.load('doux2.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
sprite_sheet2 = spritesheet.SpriteSheet(sprite_sheet_image2)

# create animation list
animation_list = []
animation_steps = [4, 6, 3, 4, 7]
animation_steps2 = [4, 4, 4, 11]
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
getanimations(sprite_sheet2, animation_list, animation_steps2)


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
    frame = 0
    frame2 = 0

    last_update = pygame.time.get_ticks()
    last_update2 = pygame.time.get_ticks()

    run = True  # initiates while loop

    clock = pygame.time.Clock()

    n = Network()  # when we# connect we will get the player starting position
    player = n.getP()
    while run:
        clock.tick(60)
        player2 = n.send(player)

        current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown:
            frame += 1
            last_update = current_time
            if frame >= len(animation_list[player.action]):
                frame = 0
        print(frame)

        if current_time - last_update2 >= animation_cooldown:
            frame2 += 1
            last_update2 = current_time
            if frame2 >= len(animation_list[player2.action]):
                frame2 = 0
        print(frame)

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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.get_health(50)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.get_damage(200)

            if event.type == pygame.KEYDOWN:
                frame = 0
            if event.type == pygame.KEYUP:
                frame = 0

        player.move(player, player2)
        redrawWindow(win, player, player2, frame, frame2)


def redrawWindow(win, player, player2, frame, frame2):
    win.fill((0, 0, 0))

    # draws background onto the screen
    # win.blit(bg_img, (0, 0))

    # draws my tiles onto the screen
    world.draw()

    win.blit(animation_list[player.action][frame], (player.x - 10, player.y - 10))
    win.blit(animation_list[player2.action][frame2], (player2.x - 10, player2.y - 10))

    # draws grid onto the screen
    # draw_grid()

    # draws player characters onto the screen

    #player.draw_character(win)
    #player2.draw_character(win)

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
