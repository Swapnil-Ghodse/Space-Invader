'''
SpaceShip Logo Image :- Icons made by <a href="https://www.flaticon.com/authors/skyclick" title="Skyclick">Skyclick</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
Spaceship in game :- Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
EnemyShip in game :- Icons made by <a href="https://www.flaticon.com/authors/smashicons" title="Smashicons">Smashicons</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
Background Image :- <a href='https://www.freepik.com/vectors/background'>Background vector created by pikisuperstar - www.freepik.com</a>
Bullet Image :- Icons made by <a href="https://www.flaticon.com/authors/those-icons" title="Those Icons">Those Icons</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>

'''

import pygame
from pygame import mixer

import random
import math

# Initialize
pygame.init()

# Create Screen
# (Width, Height)
# (0, 0) => top-left of the Window || (800, 600) => bottom-right
screen = pygame.display.set_mode((800, 600))

# Title and Window
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# background
backgroundImg = pygame.image.load("background.png")

# music
mixer.music.load("music/background.wav")
mixer.music.play(-1)

# Player
playerImg = pygame.image.load("space-invaders.png")
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX, enemyY = [], []
enemyX_change, enemyY_change = [], []
num_of_enemies = 4

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("invader2.png"))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(20)

# bullet
bulletImg = pygame.image.load("bullet.png")
bulletX, bulletY = 0, 480
bulletX_change, bulletY_change = 3, 10
# READY state means is not visible
# FIRE state means Bullet is moving
bullet_state = 'ready'

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 16)

textX = 10
textY = 10

#  Game Over
gameOver = pygame.font.Font("freesansbold.ttf", 64)

def game_over_text():
    over = gameOver.render("Game Over", True, (255, 255, 255))
    screen.blit(over, (225, 200))

def show_score(textX, textY):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (textX, textY))

# functions
def player(X, Y):
    screen.blit(playerImg, (X, Y))


def enemy(X_e, Y_e, i):
    screen.blit(enemyImg[i], (X_e, Y_e))


def fire_bullet(X, Y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (X + 16, Y + 10))


def isCollision(bulletX, bulletY, enemyX, enemyY):
    distance = math.sqrt((bulletX - enemyX)**2 + (bulletY - enemyY)**2)
    if distance <= 27:
        return True
    return False


# Game Loop
running = True

score = 0
while running:
    # screen color will update
    screen.fill((255, 255, 255))
    # background image
    screen.blit(backgroundImg, (0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:  # or event.type == (pygame.K_AT + pygame.K_F4):
            running = False
        # main character movement
        if event.type == pygame.KEYDOWN:
            print("Key Stroke is PRESSED")
            if event.key == pygame.K_LEFT:
                playerX_change = -5

            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                playerX_change = 5
                print("RIGHT is pressed")

            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bullet_sound = mixer.Sound("music/laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            playerY_change = 0
            playerX_change = 0
            print("KEY Stroke is RELEASED")

    # player() function will bw called to draw PlayerImg on Canvas
    playerX += playerX_change
    playerY += playerY_change

    # setting boundries
    # images are considered from (0, 0), not from centre.
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[i] = 1000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX[i] = 736
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("music/explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            print(score)
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    #bullet Movement

    # reset bullet
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    # bullet movement
    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change



    # player will be drawn
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

'''
    After loading the background image, movements of the game character might get slow
    due to the Background image as it takes tim time to load image and iteration slows down.
'''
