import pymongo
import math
from tkinter import *
from tkinter import font
from turtle import distance
import pygame
import random
import pygame_gui

pygame.init()
game_active = False

# create the screen / game window
screen = pygame.display.set_mode((800, 600))
# background
background = pygame.image.load('background.png')

level2_background = pygame.image.load('level2_background.jpg')

# TITLE AND ICON
pygame.display.set_caption("SPACE INVADER")

icon = pygame.image.load('bird.png')
pygame.display.set_icon(icon)
# adding player image
playerImg = pygame.image.load('player.png')

bulletImg = pygame.image.load('bullet.png')
game_over_font = pygame.font.Font('freesansbold.ttf', 100)
font = pygame.font.Font('freesansbold.ttf', 30)
bulletX = 0
bulletY = 480

bullet_state = "ready"

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

enemy_speed = 2
for i in range(num_of_enemies):

    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(enemy_speed)
    enemyY_change.append(40)

score_value = 0

font = pygame.font.Font('freesansbold.ttf', 30)
textX = 10
textY = 10

# USER TEXT INPUT
base_font = pygame.font.Font(None, 32)
user_text = ''
input_box = pygame.Rect(330, 200, 140, 32)


clock = pygame.time.Clock()


def player_name(u, x, y):
    user_name = font.render("Astronaut :"+u, True, (255, 255, 255))

    screen.blit(user_name, (x, y))


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):

    screen.blit(playerImg, (x, y))


def enemy(x, y, i):

    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"

    screen.blit(bulletImg, (x+33, y+10))


def isCollision(enemyX, enemyY, bulletX, bulletY):

    distance = (math.sqrt(math.pow(enemyX-bulletX, 2)) +
                (math.pow(enemyY-bulletY, 2)))
    if distance < 40:
        return True
    else:
        return False


def score():
    global score_value
    score_value = score_value+1
    return score_value


def game_loop(game_active):

    playerX = 370
    playerY = 480
    playerX_change = 0
    global player_speed
    player_speed = 4
    global enemy_speed
    enemy_speed = 2
    global num_of_enemies

    # adding bullet image
    # ready state - u cant see the bullet on the screen
    # fire- the bullet is currently moving and it can be seen on the screen

    bulletX = 0
    bulletY = 480
    bulletY_change = 8
    global bullet_state
    bullet_state = "ready"
    global score_value
    score_value = 0

    global user_text

    textX = 10
    textY = 10
    #base_font = pygame.font.Font(None, 32)
    #user_text = ''
    #input_box = pygame.Rect(330, 200, 140, 32)
    #box_colour = pygame.Color('lightskyblue3')

    # GAME LOOP
    running = True
    while running:

        if game_active:
            # RGB cordinates red green blue
            screen.fill((0, 0, 0))
            # background image
            screen.blit(background, (0, 0))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    exit()

                # IF KEYSTROKE IS PRESSED THEN CHECK WHETHER ITS RIGHT KEY OR LEFT KEY
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_LEFT:

                        playerX_change = -player_speed

                    if event.key == pygame.K_RIGHT:

                        playerX_change = +player_speed

                    if event.key == pygame.K_UP:
                        if bullet_state == "ready":  # so that we can press the shooting key only when it is in ready condition that is when a bullet is fired and gone >0
                            # get the current x cordinate of the spaceship
                            bulletX = playerX
                            fire_bullet(bulletX, bulletY)

                if (event.type == pygame.KEYUP):
                    if event.key == pygame.K_LEFT:

                        playerX_change = 0
                    elif event.key == pygame.K_RIGHT:
                        playerX_change = 0

        if game_active:
            # checking for boundries of spaceship so it doesnt go out of bounds
            playerX += playerX_change
            # algorithm for player

            if playerX < 0:
                playerX = 0
            elif playerX >= 736:
                playerX = 736
            # alorithm for enemy
            for i in range(num_of_enemies):
                enemyX[i] += enemyX_change[i]

                # game over:
                if enemyY[i] > 350:
                    for j in range(num_of_enemies):
                        enemyY[j] = 2000

                        game_active = False

                if enemyX[i] < 0:

                    enemyX_change[i] = enemy_speed
                    enemyY[i] += enemyY_change[i]

                elif enemyX[i] >= 736:

                    enemyX_change[i] = -enemy_speed
                    enemyY[i] += enemyY_change[i]

                # collision
                collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
                if collision:
                    bulletY = 480
                    bullet_state = "ready"
                    a = score()

                    if a % 10 == 0:
                        enemy_speed = enemy_speed+2
                        player_speed = player_speed+2

                    enemyX[i] = random.randint(0, 735)
                    enemyY[i] = random.randint(50, 150)
                enemy(enemyX[i], enemyY[i], i)

            # bullet movement
            if bulletY < 0:
                bulletY = 480
                bullet_state = "ready"

            if bullet_state == "fire":
                fire_bullet(bulletX, bulletY)
                bulletY -= bulletY_change

            player(playerX, playerY)
            show_score(textX, textY)
            player_name(user_text, 470, 10)
            #text_surface = base_font.render(user_text, True, (255, 255, 255))
            #Screen.blit(text_surface, (input_box))
        else:
            game_over = font.render("GAME OVER :(", True, (255, 255, 255))
            restart = pygame.image.load('restart.png').convert_alpha()
            restart_rect = restart.get_rect(center=(350, 320))

            # MAIN MENU ICON
            home = pygame.image.load('home.png').convert_alpha()
            home_rect = home.get_rect(center=(450, 320))

            screen.fill('pink')
            screen.blit(restart, restart_rect)
            screen.blit(game_over, (300, 240))
            screen.blit(home, home_rect)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if restart_rect.collidepoint(mouse_pos):
                        if pygame.mouse.get_pressed():
                            for i in range(num_of_enemies):

                                enemyX[i] = random.randint(0, 735)
                                enemyY[i] = random.randint(50, 150)
                                enemy(enemyX[i], enemyY[i], i)

                                score_value = 0
                                player_speed = 4
                                enemy_speed = 2
                                game_active = True
                    if home_rect.collidepoint(mouse_pos):
                        if pygame.mouse.get_pressed():
                            main_menu()

        pygame.display.update()
        clock.tick(60)

        pass


def main_menu():
    # INPUT TEXT
    base_font = pygame.font.Font(None, 32)
    global user_text

    input_box = pygame.Rect(330, 195, 140, 32)
    box_colour = pygame.Color('lightskyblue3')
    input_box_active = False

    start_button = pygame.image.load('start_button.png').convert_alpha()
    start_button_rect = start_button.get_rect(center=(400, 300))

    exit_button = pygame.image.load('exit.png').convert_alpha()
    exit_button_rect = exit_button.get_rect(center=(400, 350))

    while True:
        screen.fill('pink')

        pygame.draw.rect(screen, box_colour, input_box, 2)
        text_surface = base_font.render(user_text, True, (231, 84, 128))
        screen.blit(text_surface, (input_box))
        screen.blit(start_button, start_button_rect)
        screen.blit(exit_button, exit_button_rect)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):
                    if pygame.mouse.get_pressed():
                        for i in range(num_of_enemies):

                            enemyX[i] = random.randint(0, 735)
                            enemyY[i] = random.randint(50, 150)
                            enemy(enemyX[i], enemyY[i], i)

                        game_active = True
                        game_loop(game_active)
                        start_time = pygame.time.get_ticks()
                if exit_button_rect.collidepoint(mouse_pos):
                    if pygame.mouse.get_pressed():
                        exit()
                if input_box.collidepoint(event.pos):
                    input_box_active = True

            if event.type == pygame.KEYDOWN:
                if input_box_active == True:

                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode

        pygame.display.update()
        clock.tick(60)


main_menu()
