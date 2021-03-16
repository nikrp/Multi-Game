# Imports
import pygame
import random
from player import Player
from projectile import WaterBalloon
from enemy import Enemy
from crate import Crate
from crate import ExplosiveCrate
from explosion import Explosion
from powerUp import PowerUp
from hud import HUD

# Make the FF enemy
# Making The Enemy's Brain
class EnemyFF():
    # Enemy Constructer Function
    def __init__(self, x, y, speed, size):
        # Make The Enemy's Variables
        self.x = x
        self.y = y
        self.pic = pygame.image.load("../assets1/Fish04_A.png")
        self.pic2 = pygame.image.load("../assets1/Fish04_B.png")
        self.speed = speed
        self.size = size
        self.hitbox = pygame.Rect(self.x, self.y, int(self.size*1.25), self.size)
        self.animationTimerMax = 14
        self.animationTimer = self.animationTimerMax
        self.animationFrame = 0

        # Shrink The Enemy Pic
        self.pic = pygame.transform.scale(self.pic, (int(self.size*1.250), self.size))
        self.pic2 = pygame.transform.scale(self.pic2, (int(self.size*1.250), self.size))

        # Flip the pic if the enemy is moving left
        if self.speed < 0:
            self.pic = pygame.transform.flip(self.pic, True, False)
            self.pic2 = pygame.transform.flip(self.pic2, True, False)

    # Enemy update function
    def update(self, screen):
        self.animationTimer -= 1
        if self.animationTimer <= 0:
            self.animationTimer = self.animationTimerMax
            self.animationFrame += 1
            if self.animationFrame > 1:
                self.animationFrame = 0
        self.x += self.speed
        self.hitbox.x += self.speed
        # pygame.draw.rect(screen, (0,0,0), self.hitbox)
        if self.animationFrame == 0:
            screen.blit(self.pic, (self.x, self.y))
        else:
            screen.blit(self.pic2, (self.x, self.y))

# Make the FF game in a function
def FF():
    # Start the game
    pygame.init()
    game_width = 1000
    game_height = 650
    screen = pygame.display.set_mode((game_width, game_height))
    clock = pygame.time.Clock()
    ffRunning = True

    # Load all the images for the game
    backgroundImg = pygame.image.load("../assets1/Scene_A.png")
    backgroundImg2 = pygame.image.load("../assets1/Scene_B.png")
    playerPic = pygame.image.load("../assets1/sid.png")
    playerEatingPic = pygame.image.load("../assets1/sid3open.png")
    playerPic2 = pygame.image.load("../assets1/sid2.png")

    # Make some variables for the background animation
    bgAnimationTimerMax = 25
    bgAnimationTimer = bgAnimationTimerMax
    bgAnimationFrame = 0

    # Direction of the fish
    playerFacingLeft = False

    # Speed of the player
    playerSpeed = 8

    # Size of the player
    playerStartingSize = 30
    playerSize = playerStartingSize

    # Make some variables for the position of our player
    playerStartingX = 480
    playerStartingY = 310
    player_x = playerStartingX
    player_y = playerStartingY

    # Make some variables for the player animation
    playerEatingTimerMax = 9
    playerEatingTimer= 0
    playerSwimmingTimerMax = 14
    playerSwimmingTimer = playerSwimmingTimerMax
    playerSwimmingFrame = 0

    # Player hitbox
    playerHitbox = pygame.Rect(player_x, player_y, int(playerSize*1.25), playerSize)
    playerAlive = False

    # Make some variables for the HUD (heads-up display)
    score = -1
    scoreFont = pygame.font.SysFont("myriadhebrewopentype", 30)
    scoreText = scoreFont.render("Score: "+str(score), 1, (255, 255, 255))
    playButtonPic = pygame.image.load("../assets1/BtnPlayIcon.png")
    playButtonX = game_width/2 - playButtonPic.get_width()/2
    playButtonY = game_height/2 - playButtonPic.get_height()/2 + 40
    titlePic = pygame.image.load("../assets1/Title.png")
    titleX = game_width/2 - titlePic.get_width()/2
    titleY = playButtonY - 150
     
    # Variables for the spawn rate (timer) of enemies
    enemyTimerMax = 40
    enemyTimer = enemyTimerMax

    # Make the enemy's array
    enemies = []
    enemiesToRemove = []


    # ***************** Loop Land Below *****************
    # Everything under 'while running' will be repeated over and over again
    while ffRunning:
        # Makes the game stop if the player clicks the X or presses esc
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("TEST - FF Game QUIT is pressed")
                ffRunning = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print("TEST - FF Game ESCAPE is pressed")
                ffRunning = False

        # Check to see what keys the player is pressing
        keys = pygame.key.get_pressed()
        
        # Move Right
        if keys[pygame.K_d]:
            playerFacingLeft = False
            player_x += playerSpeed
        # Move Left
        if keys[pygame.K_a]:
            playerFacingLeft = True
            player_x -= playerSpeed
        # Move Down
        if keys[pygame.K_s]:
            player_y += playerSpeed
        # Move Up
        if keys[pygame.K_w]:
            player_y -= playerSpeed
        # Get Bigger
        #if keys[pygame.K_SPACE]:
        #    playerSize += 2

        # Stop the player from leaving the screen
        if player_x < 0:
            player_x = 0
        if player_x > game_width - playerSize*1.25:
            player_x = game_width - playerSize*1.25
        if player_y < 0:
            player_y = 0
        if player_y > game_height - playerSize:
            player_y = game_height - playerSize
        
        # do the background animation timer
        bgAnimationTimer -= 1
        if bgAnimationTimer <= 0:
            bgAnimationFrame += 1
            if bgAnimationFrame > 1:
                bgAnimationFrame = 0
            bgAnimationTimer = bgAnimationTimerMax

        if bgAnimationFrame == 0:
            screen.blit(backgroundImg, (0, 0))
        else:
            screen.blit(backgroundImg2, (0, 0))

        # Spawn a new enemy whenever enemyTimer hits 0
        enemyTimer -= 1
        if enemyTimer <= 0:
            newEnemyY = random.randint(0, game_height)
            newEnemySpeed = random.randint(1, 5)
            newEnemySize = random.randint(playerSize/2, playerSize*2)
            if random.randint(0, 1) == 0:
                enemies.append(EnemyFF(-newEnemySize*2, newEnemyY, newEnemySpeed, newEnemySize))
            else:
                enemies.append(EnemyFF(game_width, newEnemyY, -newEnemySpeed, newEnemySize))
            enemyTimer = enemyTimerMax

        for enemy in enemiesToRemove:
            enemies.remove(enemy)
        enemiesToRemove = []

        # Update all enemies
        for enemy in enemies:
            enemy.update(screen)
            if enemy.x < -1000 or enemy.x > game_width + 1000:
                enemiesToRemove.append(enemy)
            
        if playerAlive:
            # Update the player hitbox
            playerHitbox.x = player_x
            playerHitbox.y = player_y
            playerHitbox.width = int(playerSize*1.25)
            playerHitbox.height = playerSize
            # pygame.draw.rect(screen, (255, 255, 255), playerHitbox)
        
            # Check to see when the player hits an Enemy
            for enemy in enemies:
                if playerHitbox.colliderect(enemy.hitbox):
                    if playerSize >= enemy.size:
                        score += enemy.size
                        playerSize += 2
                        enemies.remove(enemy)
                        playerEatingTimer = playerEatingTimerMax
                    else:
                        playerAlive = False

            # Do the player swimming animation timer
            playerSwimmingTimer -= 1
            if playerSwimmingTimer <= 0:
                playerSwimmingTimer = playerSwimmingTimerMax
                playerSwimmingFrame += 1
                if playerSwimmingFrame > 1:
                    playerSwimmingFrame = 0
        
            # Draw the player pic
            if playerEatingTimer > 0:
                playerPicSmall = pygame.transform.scale(playerEatingPic, (int(playerSize*1.25), playerSize))
                playerEatingTimer -= 1
            else:
                if playerSwimmingFrame == 0:
                    playerPicSmall = pygame.transform.scale(playerPic, (int(playerSize*1.25), playerSize))
                else:
                    playerPicSmall = pygame.transform.scale(playerPic2, (int(playerSize*1.25), playerSize))
            if playerFacingLeft:
                playerPicSmall = pygame.transform.flip(playerPicSmall, True, False)
            screen.blit(playerPicSmall, (player_x, player_y))

        # Draw the score text
        if playerAlive:
            scoreText = scoreFont.render("Score: "+str(score), 1, (255, 255, 255))
        else:
            scoreText = scoreFont.render("Final Score: "+str(score), 1, (255, 255, 255))

        if score >= 0:
            screen.blit(scoreText, (30, 30))

        # Draw the menu (when the player is not alive
        if not playerAlive:
            screen.blit(playButtonPic, (playButtonX, playButtonY))
            screen.blit(titlePic, (titleX, titleY))
            mouseX, mouseY = pygame.mouse.get_pos()
            # Check to see if the player clicks the play button
            if pygame.mouse.get_pressed()[0]:
                if mouseX > playButtonX and mouseX < playButtonX+playButtonPic.get_width():
                    if mouseY > playButtonY and mouseY < playButtonY+playButtonPic.get_height():
                        # Restart the game
                        playerAlive = True
                        score = 0
                        player_x = playerStartingX
                        player_y = playerStartingY
                        playerSize = playerStartingSize
                        for enemy in enemies:
                            enemiesToRemove.append(enemy)
            

        # Tell pygame to update the screen
        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("Fish Fights! fps: " + str(clock.get_fps()))

## Robo Invasion main block
def RI():
    global enemySpawnSpeedupTimerMax
    global hud
    global mrPlayer
    global screen
    global gameWidth, gameHeight
    global gameStarted
    onHome = False
    # Start the game
    pygame.init()
    gameWidth = 1000
    gameHeight = 650
    screen = pygame.display.set_mode((gameWidth, gameHeight))
    clock = pygame.time.Clock()
    riRunning = True

    backgroundImg = pygame.image.load("../assets/BG_Mars.png")

    # Make all the Sprite groups
    playerGroup = pygame.sprite.Group()
    projectilesGroup = pygame.sprite.Group()
    enemiesGroup = pygame.sprite.Group()
    cratesGroup = pygame.sprite.Group()
    explosionsGroup = pygame.sprite.Group()
    powerupsGroup = pygame.sprite.Group()

    # Put every Sprite class in a group
    Player.containers = playerGroup
    WaterBalloon.containers = projectilesGroup
    Enemy.containers = enemiesGroup
    Crate.conatainers = cratesGroup
    Explosion.containers = explosionsGroup
    PowerUp.containers = powerupsGroup

    enemySpawnTimerMax = 100
    enemySpawnTimer = 0
    enemySpawnSpeedupTimerMax = 400
    enemySpawnSpeedupTimer = enemySpawnSpeedupTimerMax

    gameStarted = False

    mrPlayer = Player(screen, gameWidth / 2, gameHeight / 2)

    hud = HUD(screen, mrPlayer)

    def startRIGame():
        global gameStarted
        global hud
        global mrPlayer
        global enemySpawnTimerMax
        global enemySpawnTimer
        global enemySpawnSpeedupTimer
        global enemySpawnSpeedupTimerMax
        global screen
        global gameWidth, gameHeight

        enemySpawnTimerMax = 100
        enemySpawnTimer = 0
        enemySpawnSpeedupTimer = enemySpawnSpeedupTimerMax

        gameStarted = True
        hud.state = "ingame"
        mrPlayer.__init__(screen, gameWidth / 2, gameHeight / 2)

        for i in range(0, 20):
            num = random.randint(1, 2)
            if num == 1:
                ExplosiveCrate(screen, random.randint(0, gameWidth), random.randint(0, gameHeight), mrPlayer)
            else:
                Crate(screen, random.randint(0, gameWidth), random.randint(0, gameHeight), mrPlayer)

    # ***************** Loop Land Below *****************
    # Everything under 'while running' will be repeated over and over again
    while riRunning:
        # Makes the game stop if the player clicks the X or presses esc
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("TEST - RI Game QUIT is pressed")
                riRunning = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print("TEST - RI Game ESCAPE is pressed")
                riRunning = False

        screen.blit(backgroundImg, (0, 0))

        if not gameStarted:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    print("TEST - start RI Game")
                    startRIGame()
                    break

        if gameStarted:
            # Deal with the player input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                mrPlayer.move(1, 0, cratesGroup)
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                mrPlayer.move(-1, 0, cratesGroup)
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                mrPlayer.move(0, -1, cratesGroup)
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                mrPlayer.move(0, 1, cratesGroup)
            if pygame.mouse.get_pressed()[0]:
                mrPlayer.shoot()
            if keys[pygame.K_SPACE]:
                mrPlayer.placeCrate()
            if pygame.mouse.get_pressed()[2]:
                mrPlayer.placeExplosiveCrate()

            enemySpawnSpeedupTimer -= 1
            if enemySpawnSpeedupTimer <= 0:
                if enemySpawnTimerMax > 20:
                    enemySpawnTimerMax -= 10
                    enemySpawnSpeedupTimer = enemySpawnSpeedupTimerMax

            # Make Enemy Spawning happen
            enemySpawnTimer -= 1
            if enemySpawnTimer <= 0:
                newEnemy = Enemy(screen, 0, 0, mrPlayer)
                sideToSpawn = random.randint(0, 3)  # 0=top, 1=bottom, 2=left, 3=right
                if sideToSpawn == 0:
                    newEnemy.x = random.randint(0, gameWidth)
                    newEnemy.y = -newEnemy.image.get_height()
                elif sideToSpawn == 1:
                    newEnemy.x = random.randint(0, gameWidth)
                    newEnemy.y = gameHeight + newEnemy.image.get_height()
                elif sideToSpawn == 2:
                    newEnemy.x = -newEnemy.image.get_width()
                    newEnemy.y = random.randint(0, gameHeight)
                elif sideToSpawn == 3:
                    newEnemy.x = gameWidth + newEnemy.image.get_width()
                    newEnemy.y = random.randint(0, gameHeight)
                enemySpawnTimer = enemySpawnTimerMax

            for powerup in powerupsGroup:
                powerup.update(mrPlayer)

            for projectile in projectilesGroup:
                projectile.update()

            for enemy in enemiesGroup:
                enemy.update(projectilesGroup, cratesGroup, explosionsGroup)

            for crate in cratesGroup:
                crate.update(projectilesGroup, explosionsGroup)

            for explosion in explosionsGroup:
                explosion.update()

            mrPlayer.update(enemiesGroup, explosionsGroup)

            if not mrPlayer.alive:
                if hud.state == "ingame":
                    hud.state = "gameover"
                elif hud.state == "mainmenu":
                    gameStarted = False
                    playerGroup.empty()
                    enemiesGroup.empty()
                    projectilesGroup.empty()
                    explosionsGroup.empty()
                    cratesGroup.empty()
                    powerupsGroup.empty()
#        print("TEST - RI before hud update")

        hud.update()

        # Tell pygame to update the screen
        pygame.display.flip()
        clock.tick(40)
        pygame.display.set_caption("Robo Invasion fps: " + str(clock.get_fps()))
# end of Robo Invasion

# Start the multigame window
pygame.init
gameWidth = 1000
gameHeight = 650
screen = pygame.display.set_mode((gameWidth, gameHeight))
clock = pygame.time.Clock()
running = True

backgroundImage = pygame.image.load("../assets2/home_page.png")
title = pygame.image.load("../assets2/title.png")
ffGamePic = pygame.image.load("../assets2/fishfights.png")
riGamePic = pygame.image.load("../assets2/roboinvasion.png")
ffInstructPic = pygame.image.load("../assets2/ffinstruct.png")
riInstructPic = pygame.image.load("../assets2/riinstruct.png")
onHome = True
inGame = False

while running:
    # Makes the players game stop if the player clicks the X or presses esc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    if onHome == True:
        screen.blit(backgroundImage, (0, 0))
        screen.blit(title, (250, 100))
        screen.blit(ffGamePic, (0, 200))
        screen.blit(riGamePic, (gameWidth/2, 200))
        screen.blit(ffInstructPic, (100, 550))
        screen.blit(riInstructPic, (600, 550))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
        FF()
        print(f"TEST - Running after FF - {running}")
    elif keys[pygame.K_2]:
        RI()
        print(f"TEST - Running after RI - {running}")

    # Get the caption and fps
    pygame.display.flip()
    clock.tick(40)
    pygame.display.set_caption("Multi Game! BOOM fps: " + str(clock.get_fps()))
