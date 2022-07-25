import pygame
import random
import math

pygame.init()
screen = pygame.display.set_mode((800, 800))

# CHANGING TITLE FROM PYGAME TO SPACE INVADERS
pygame.display.set_caption("SPACE INVADERS")

# BACK GROUND
background = pygame.image.load('cartoon-colorful-galaxy-background_52683-63413.png')

# PLAYER
playerIMG = pygame.image.load('spaceship2.png')
playerX = 360
playerY = 700
change_x = 0

# ALIEN (ENEMY)
numb_of_alien = 5
alienImg = []
alienX = []
alienY = []
change_alienX = []
change_alienY = []
for i in range(numb_of_alien):
    alienImg.append(pygame.image.load('alien.png'))
    alienX.append(random.randint(100, 700))
    alienY.append(random.randint(50, 200))
    change_alienX.append(2.5)
    change_alienY.append(40)

# MISSILE
missileIMG = pygame.image.load('missile.png')
missileX = 0
missileY = 700
change_missileX = 0
change_missileY = -8
# STATE OF THE MISSILE -- READY MEANS YOU CANT SEE IT ON SCREEN -- FIRE MEANS YOU CAN
missile_state = "ready"

# SCORE STSYEM
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# GAME OVER TEXT
over_font = pygame.font.Font('freesansbold.ttf', 256)


def game_over():
    over_font = font.render("GAME OVER  FINAL SCORE " + str(score_value), True, (255, 255, 255))
    screen.blit(over_font, (250, 300))


def show_score(x, y):
    score = font.render("SCORE :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def alien(x, y, i):
    screen.blit(alienImg[i], (x, y))


def player(x, y):
    screen.blit(playerIMG, (x, y))


def fire_missile(x, y):
    global missile_state
    missile_state = "fire"
    screen.blit(missileIMG, (x + 16, y + 10))


def isCollision(alienX, alienY, missileX, missileY):
    distance = math.sqrt((math.pow(alienX - missileX, 2)) + (math.pow(alienY - missileY, 2)))
    if distance <= 25:
        return True
    else:
        return False


# GAME LOOP
run = True
while run:
    # background color (RGB)
    screen.fill((245, 245, 245))
    # BACKGROUND IMAGE
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        # TO QUIT GAME
        if event.type == pygame.QUIT:
            run = False

        # MOVEMENT MECHANICS OF THE SPACESHIP ( MOVING LEFT AND RIGHT )
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                change_x = -5
            if event.key == pygame.K_RIGHT:
                change_x = 5
            if event.key == pygame.K_SPACE:
                if missile_state == "ready":
                    missileX = playerX
                    fire_missile(missileX, missileY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                change_x = 0
    # MOVEMENT OF BULLET
    if missileY <= 0:
        missileY = 700
        missile_state = "ready"
    if missile_state == "fire":
        fire_missile(missileX, missileY)
        missileY = missileY + change_missileY

    # TO MAKE BOUNDARIES
    if playerX <= 0:
        playerX = 0
    if playerX >= 750:
        playerX = 750
    # BOUNDARIES OF ALIEN AND MOVEMENT
    for i in range(numb_of_alien):
        # GAME OVER
        if alienY[i] >= 600:
            for j in range(numb_of_alien):
                alienY[j] = 2000
            game_over()
            break

        alienX[i] = alienX[i] + change_alienX[i]
        if alienX[i] >= 700:
            change_alienX[i] = -2.5
            alienY[i] = alienY[i] + change_alienY[i]
        if alienX[i] <= 0:
            change_alienX[i] = 2.5
            alienY[i] = alienY[i] + change_alienY[i]
        collision = isCollision(alienX[i], alienY[i], missileX, missileY)
        # COLLISION CHECKING
        if collision:
            missileY = 700
            missile_state = "ready"
            score_value = score_value + 1
            alienX[i] = random.randint(100, 700)
            alienY[i] = random.randint(50, 200)

        alien(alienX[i], alienY[i], i)

    playerX = playerX + change_x  # POSITION OF SPACESHIP AFTER PRESSING KEYS
    player(playerX, playerY)  # FINAL POSITION OF THE SPACESHIP
    show_score(textX, textY)
    pygame.display.update()
