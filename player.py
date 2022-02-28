import pygame
from world import World, map1, map2, width, height

win = pygame.display.set_mode((width, height))  # Size of window

selected_world = World(map1)


class Player():
    def __init__(self, x, y, width, height, health_x, health_y, lives_x, lives_y, direction):
        self.selected_char = False
        self.ready = False
        self.tried_to_light_attack_this_frame = False
        self.tried_to_heavy_attack_this_frame = False

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.vel_y = 0
        self.jumped = False
        self.in_air = True

        lives = 3
        self.current_lives = lives
        self.max_lives = lives
        self.lives_bar_length = 60
        self.live_ratio = self.max_lives / self.lives_bar_length
        self.lives_x = lives_x
        self.lives_y = lives_y

        self.current_health = 10000
        self.maximum_health = 10000
        self.health_bar_length = 250
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.health_x = health_x
        self.health_y = health_y

        self.attack_light = 50
        self.attack_heavy = 100

        self.speed = 5

        self.keys = pygame.key.get_pressed()

        self.action = 0
        self.frame = 0

        self.direction = direction

        self.chosen_char = None

    def choose_character(self, chosen_char):
        self.chosen_char = chosen_char
        if chosen_char == "Doux":
            self.current_health = 10000
            self.maximum_health = 10000
            self.attack_light = 400
            self.attack_heavy = 800
            self.speed = 5

        elif chosen_char == "Mort":
            self.current_health = 7500
            self.maximum_health = 7500
            self.attack_light = 500
            self.attack_heavy = 1000
            self.speed = 5

        elif chosen_char == "Tard":
            self.current_health = 7500
            self.maximum_health = 7500
            self.attack_light = 400
            self.attack_heavy = 800
            self.speed = 7

        elif chosen_char == "Vita":
            self.current_health = 12500
            self.maximum_health = 12500
            self.attack_light = 350
            self.attack_heavy = 700
            self.speed = 4
        self.health_ratio = self.maximum_health / self.health_bar_length

    def get_damage(self, amount):
        if self.current_health > 0:
            self.current_health -= amount
        if self.current_health <= 0:
            self.current_health = 0

    def get_health(self, amount):
        if self.current_health < self.maximum_health:
            self.current_health += amount
        if self.current_health >= self.maximum_health:
            self.current_health = self.maximum_health

    def reduce_lives(self, amount):
        self.current_lives -= amount

    def display_health(self):
        pygame.draw.rect(win, (255, 0, 0), (self.health_x, self.health_y, self.current_health / self.health_ratio, 15))
        pygame.draw.rect(win, (0, 0, 0), (self.health_x, self.health_y, self.health_bar_length, 15), 5)
        # if want health bar above player swap health.x with x - 30 and health.y with y - 30

    def display_lives(self):
        pygame.draw.rect(win, (51, 255, 51), (self.lives_x, self.lives_y, self.current_lives / self.live_ratio, 15))
        pygame.draw.rect(win, (0, 0, 0), (self.lives_x, self.lives_y, self.lives_bar_length, 15), 5)
        pygame.draw.line(win, (0, 0, 0), (self.lives_x + self.lives_bar_length / 3, self.lives_y),
                         (self.lives_x + self.lives_bar_length / 3, self.lives_y + 15), 5)
        pygame.draw.line(win, (0, 0, 0), (self.lives_x + 2 * self.lives_bar_length / 3, self.lives_y),
                         (self.lives_x + 2 * self.lives_bar_length / 3, self.lives_y + 15), 5)

    def move(self, player2):
        dx = 0
        dy = 0

        # get key presses
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_a] or self.keys[pygame.K_LEFT]:
            dx -= self.speed

        if self.keys[pygame.K_d] or self.keys[pygame.K_RIGHT]:
            dx += self.speed

        if (self.keys[pygame.K_w] or self.keys[pygame.K_UP]) and self.jumped == False and self.in_air == False:
            self.vel_y = -15
            self.jumped = True

        if not (self.keys[pygame.K_w] or self.keys[pygame.K_UP]):
            self.jumped = False
        # this is the gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # collision
        self.in_air = True
        for tile in selected_world.tile_list:
            # check for collision in x direction
            if tile[1].colliderect(self.x + dx, self.y, self.width, self.height):
                dx = 0
            # check for collision is y direction
            if tile[1].colliderect(self.x, self.y + dy, self.width, self.height):
                # check if below the ground
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                # check if above the ground
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False

        # coord
        self.x += dx
        self.y += dy

        self.update(player2)

    def live_check(self, player, player2):

        if player.current_health <= 0:
            player.reduce_lives(1)
            player.get_health(player.maximum_health)

        if player2.current_health <= 0:
            player2.reduce_lives(1)
            player2.get_health(player2.maximum_health)

    def update(self, player2):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.display_health()
        self.display_lives()
        player2.display_health()
        player2.display_lives()

        if player2.tried_to_light_attack_this_frame == True and self.rect.colliderect(player2.rect):
            self.get_damage(player2.attack_light)

        player2.tried_to_light_attack_this_frame = False

        if player2.tried_to_heavy_attack_this_frame == True and self.rect.colliderect(player2.rect):
            self.get_damage(player2.attack_heavy)
        player2.tried_to_heavy_attack_this_frame = False
