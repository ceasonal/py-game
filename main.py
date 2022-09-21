import pygame
import random
import math

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("gameimg/background.png")

# Title & Icon
pygame.display.set_caption("Asteroid Defense")
icon = pygame.image.load("gameimg/shipIcon.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("gameimg/shipMain.png")
playerX = 370
playerY = 480
playerX_change = 0

# Asteroids
asteroidImg = []
enemyX = []
asteroidX = []
asteroidY = []
asteroidX_change = []
asteroidY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    asteroidImg.append(pygame.image.load("gameimg/asteroid.png"))
    asteroidX.append(random.randint(0, 735))
    asteroidY.append(random.randint(50, 50))
    asteroidX_change.append(4)
    asteroidY_change.append(40)

# Beams
# Ready - cant see beam on screen
# Fire - beam is moving
beamImg = pygame.image.load("gameimg/testbeam.png")
beamX = 0
beamY = 480
beamX_change = 0
beamY_change = 10
beam_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game over text
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

gameover = False
def scoreboard(x,y):
    score = font.render("Score: "+ str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
def game_over():
    global gameover
    over_text= font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (310, 250))
    restart_text = font.render("PRESS BACKSPACE TO RESTART", True, (255, 255, 255))
    screen.blit(restart_text, (150, 300))
    gameover = True
def player(x, y):
    screen.blit(playerImg, (x, y))
def asteroid(x, y, i):
    screen.blit(asteroidImg[i], (x, y))
def fire_beam(x, y):
    global beam_state
    beam_state = "fire"
    screen.blit(beamImg, (x + 16, y + 10))
def isCollision(asteroidX, asteroidY, beamX, beamY):
    distance = math.sqrt((math.pow(asteroidX - beamX, 2)) + (math.pow(asteroidY - beamY, 2)))
    if distance < 27:  # distance b/w beam and asteroid
        return True


# Game Loop
running = True
while running:
    # RGB Color
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    # playerX += 0.1 #makes img move right auto

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            # print("A keystore is pressed")#if any other keystore is pressed
            if event.key == pygame.K_LEFT:
                playerX_change = -5
                # print("Left arrow is pressed")
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
                # print("Right arrow is pressed")
            if event.key == pygame.K_SPACE:
                if beam_state == "ready":
                    beamX = playerX
                    fire_beam(beamX, beamY)
                    fire_beam(playerX, beamY)
            # Restart game
            if event.key == pygame.K_BACKSPACE and gameover:
                print("back is pressed")
                asteroidImg = []
                enemyX = []
                asteroidX = []
                asteroidY = []
                asteroidX_change = []
                asteroidY_change = []
                num_of_enemies = 6
                for i in range(num_of_enemies):
                    asteroidImg.append(pygame.image.load("gameimg/asteroid.png"))
                    asteroidX.append(random.randint(0, 735))
                    asteroidY.append(random.randint(50, 50))
                    asteroidX_change.append(4)
                    asteroidY_change.append(40)
                score_value = 0
                gameover = False


        # If event.type == pygame.KEYUP:
        #     if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
        #         playerX_change = 0
        #         # print("Keystore has been released")

    playerX += playerX_change  # move player position
    if playerX <= 0:  # create/set boundaries
        playerX = 0
    elif playerX >= 737:  # ship width = 800-63 =737
        playerX = 737

    # Asteroid movement
    asteroidX += asteroidX_change
    for i in range(num_of_enemies):
        # Game Over
        if asteroidY[i] > 100:
            for j in range(num_of_enemies):
                asteroidY[j] = 2000
            game_over()
            break

        asteroidX[i] += asteroidX_change[i]
        if asteroidX[i] <= 0:  # create/set boundaries
            asteroidX_change[i] = 4
            asteroidY[i] += asteroidY_change[i]
        elif asteroidX[i] >= 736:  # astroid width = 800-64 =736
            asteroidX_change[i] = -4
            asteroidY[i] += asteroidY_change[i]

        # Collision
        collision = isCollision(asteroidX[i], asteroidY[i], beamX, beamY)
        if collision:
            beamY = 480
            beam_state = "ready"
            score_value += 1
            print(score_value)
            asteroidX[i] = random.randint(0, 735)
            asteroidY[i] = random.randint(50, 50)

        asteroid(asteroidX[i], asteroidY[i], i)


    # Beam movement
    if beamY <= 0:
        beamY = 480
        beam_state = "ready"

    if beam_state == "fire":
        fire_beam(beamX, beamY)
        beamY -= beamY_change


    player(playerX, playerY)
    scoreboard(textX,textY)
    pygame.display.update()