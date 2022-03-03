import socket
import sys
import pygame
from network import Network  # this will import the network class from network file
from world import World, map1, map2, empty_map
from characters import characters

pygame.font.init()

width = 1250  # width of window
height = 800  # height of window
win = pygame.display.set_mode((width, height))  # Size of window
pygame.display.set_caption("Dino Brawler")  # Cilent Name

characters = {
    "Doux": characters[0],
    "Mort": characters[1],
    "Tard": characters[2],
    "Vita": characters[3],
}

map1_image = pygame.image.load('Map Assets/Map Screenshots/Map 1.png').convert_alpha()
map2_image = pygame.image.load('Map Assets/Map Screenshots/Map 2.png').convert_alpha()

map1_image = pygame.transform.scale(map1_image, (500, 280))
map2_image = pygame.transform.scale(map2_image, (500, 280))

animation_cooldown = 100

black = (0, 0, 0)
grey = (128, 128, 128)
white = (255, 255, 255)

blue = (0, 156, 255)
red = (255, 0, 0)
yellow = (255, 174, 0)
green = (182, 255, 0)


class Button:
    def __init__(self, text, x, y, box_color, text_color):
        self.text = text
        self.x = x
        self.y = y
        self.box_color = box_color
        self.text_color = text_color
        self.width = 150
        self.height = 100

    def draw(self, screen):
        pygame.draw.rect(screen, self.box_color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("Agency FB", 40)
        text = font.render(self.text, True, self.text_color)
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


menu_buttons = (Button("Play Game", 525, 350, white, red),
                Button("Close Game", 525, 500, white, red))

character_selection_buttons = (Button("Doux", 100, 200, blue, black),
                               Button("Mort", 400, 200, red, black),
                               Button("Tard", 700, 200, yellow, black),
                               Button("Vita", 1000, 200, green, black))

map_buttons = (Button("Map 1", 280, 550, white, red),
               Button("Map 2", 820, 550, white, red))

play_again_button = Button("Main menu", 525, 550, white, red)


def update_screen(win, player, player2, chosen_animation_list, chosen_animation_list2, world):
    win.fill(grey)

    if player.ready == True and player2.ready == True:

        # draws my tiles onto the screen
        world.draw()

        # draw the character onto screen
        win.blit(chosen_animation_list[player.action][player.frame], (player.x - 10, player.y - 10))
        win.blit(chosen_animation_list2[player2.action][player2.frame], (player2.x - 10, player2.y - 10))

        # draw player health and live bars on screen
        font = pygame.font.SysFont("Agency FB", 80)
        text = font.render("P1", True, red)
        win.blit(text, (25, 700))
        text = font.render("P2", True, red)
        win.blit(text, (825, 700))
        player.update(player2, win)

    else:
        font = pygame.font.SysFont("Agency FB", 80)
        text = font.render("Waiting for Player...", True, red)
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))

    pygame.display.update()


def main():
    world = World(empty_map)

    run = True  # initiates while loop
    clock = pygame.time.Clock()

    network = Network()
    player = network.get_player()

    player.action = 0
    player.frame = 0
    last_update = pygame.time.get_ticks()

    chosen_animation_list = []
    chosen_animation_list2 = []

    while run:
        clock.tick(60)
        try:
            player2 = network.receive(player)
        except:
            run = False
            print("Couldn't get game")
            break
        player.ready = True
        if player.ready == True and player.selected_char == False:
            select_character(player)
            chosen_animation_list = characters[player.chosen_char]

        if player2.ready == True and player2.selected_char == True:
            chosen_animation_list2 = characters[player2.chosen_char]

        if player.selected_char == True and player.has_voted_on_map == False:
            vote_on_map(player)

        if player.has_voted_on_map == True and player2.has_voted_on_map == True:
            if player.decided_map == "Map 1":
                world = World(map1)
            else:
                world = World(map2)

        player.tried_to_light_attack_this_frame = False
        player.tried_to_heavy_attack_this_frame = False

        current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown:
            player.frame += 1
            last_update = current_time
            if player.frame >= len(chosen_animation_list[player.action]):
                player.frame = 0

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    player.action = 1
                    player.frame = 0
                    player.direction = "RIGHT"

                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    player.action = 10
                    player.frame = 0
                    player.direction = "LEFT"

                if (event.key == pygame.K_w or event.key == pygame.K_UP) and player.jumped == False:
                    if player.direction == "RIGHT":
                        player.action = 7

                    elif player.direction == "LEFT":
                        player.action = 16

                    player.frame = 0

                if event.key == pygame.K_j:
                    player.tried_to_light_attack_this_frame = True

                    if player.direction == "RIGHT":
                        player.action = 2

                    elif player.direction == "LEFT":
                        player.action = 11

                    player.frame = 0

                if event.key == pygame.K_k:
                    player.tried_to_heavy_attack_this_frame = True

                    if player.direction == "RIGHT":
                        player.action = 5

                    elif player.direction == "LEFT":
                        player.action = 14

                    player.frame = 0

            if event.type == pygame.KEYUP:

                if player.direction == "RIGHT":
                    player.action = 0

                elif player.direction == "LEFT":
                    player.action = 9

                player.frame = 0

            if player.current_lives == 0:
                loser_screen()
                run = False

            if player2.current_lives == 0:
                winner_screen()
                run = False

        if player.has_voted_on_map == True and player2.has_voted_on_map == True:
            player.move(win, player2, world)
            player.live_check(player, player2)

        update_screen(win, player, player2, chosen_animation_list, chosen_animation_list2, world)


def loser_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill(black)
        font = pygame.font.SysFont("Agency FB", 60)
        loser_text = font.render("YOU LOSE!!!", True, red)
        win.blit(loser_text, (525, 350))

        play_again_button.draw(win)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:

                pos = pygame.mouse.get_pos()
                if play_again_button.click(pos):
                    menu_screen()
                    run = False


def winner_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill(black)
        font = pygame.font.SysFont("Agency FB", 60)
        winner_text = font.render("YOU WIN!!!", True, (255, 255, 0))
        win.blit(winner_text, (525, 350))

        play_again_button.draw(win)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:

                pos = pygame.mouse.get_pos()
                if play_again_button.click(pos):
                    menu_screen()
                    run = False


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill(grey)

        font = pygame.font.SysFont("Agency FB", 120)
        winner_text = font.render("DINO BRAWL", True, (0, 255, 0))
        win.blit(winner_text, (400, 150))

        for button in menu_buttons:
            button.draw(win)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                pos = pygame.mouse.get_pos()
                for button in menu_buttons:
                    if button.click(pos):
                        if button.text == "Play Game":
                            run = False
                        elif button.text == "Close Game":
                            sys.exit()

    main()


def vote_on_map(player):
    run = True
    clock = pygame.time.Clock()

    while run:

        clock.tick(60)
        win.fill(black)

        font = pygame.font.SysFont("Agency FB", 110)
        choose_character_text = font.render("VOTE ON MAP", True, red)
        win.blit(choose_character_text, (425, 25))

        win.blit(map1_image, (105, 200))
        win.blit(map2_image, (645, 200))

        for button in map_buttons:
            button.draw(win)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for map_choice in map_buttons:
                    if map_choice.click(pos):
                        player.chosen_map = map_choice.text
                        player.has_voted_on_map = True
                        run = False


def select_character(player):
    run = True
    clock = pygame.time.Clock()

    last_update = pygame.time.get_ticks()
    frame = 0
    while run:

        clock.tick(60)
        win.fill(black)

        current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown:
            frame += 1
            last_update = current_time
            if frame >= 6:
                frame = 0

        font = pygame.font.SysFont("Agency FB", 110)
        choose_character_text = font.render("CHOOSE YOUR CHARACTER", True, white)
        win.blit(choose_character_text, (175, 25))

        font = pygame.font.SysFont("Agency FB", 40)

        doux_desc_health = font.render("Health: Normal", True, blue)
        doux_desc_attack = font.render("Attack: Normal", True, blue)
        doux_desc_speed = font.render("Speed: Normal ", True, blue)

        mort_desc_health = font.render("Health: Low", True, red)
        mort_desc_attack = font.render("Attack: High", True, red)
        mort_desc_speed = font.render("Speed: Normal", True, red)

        tard_desc_health = font.render("Health: Low", True, yellow)
        tard_desc_attack = font.render("Attack: Normal", True, yellow)
        tard_desc_speed = font.render("Speed: High", True, yellow)

        vita_desc_health = font.render("Health: High", True, green)
        vita_desc_attack = font.render("Attack: Low", True, green)
        vita_desc_speed = font.render("Speed: Low", True, green)

        win.blit(doux_desc_health, (100, 450))
        win.blit(doux_desc_attack, (100, 500))
        win.blit(doux_desc_speed, (100, 550))

        win.blit(mort_desc_health, (400, 450))
        win.blit(mort_desc_attack, (400, 500))
        win.blit(mort_desc_speed, (400, 550))

        win.blit(tard_desc_health, (700, 450))
        win.blit(tard_desc_attack, (700, 500))
        win.blit(tard_desc_speed, (700, 550))

        win.blit(vita_desc_health, (1000, 450))
        win.blit(vita_desc_attack, (1000, 500))
        win.blit(vita_desc_speed, (1000, 550))

        win.blit(pygame.transform.scale(characters["Doux"][1][frame], (144, 144)), (105, 300))
        win.blit(pygame.transform.scale(characters["Mort"][1][frame], (144, 144)), (405, 300))
        win.blit(pygame.transform.scale(characters["Tard"][1][frame], (144, 144)), (705, 300))
        win.blit(pygame.transform.scale(characters["Vita"][1][frame], (144, 144)), (1005, 300))

        for button in character_selection_buttons:
            button.draw(win)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for character in character_selection_buttons:
                    if character.click(pos):
                        player.choose_character(character.text)
                        player.selected_char = True
                        run = False


while True:
    menu_screen()
