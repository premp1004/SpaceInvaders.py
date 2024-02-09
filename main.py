import math
import turtle
import pygame
import random
from pygame import mixer
##########################################
# intro screen/splash screen
gameState = "splash"

# Loading the songs/sound effects
pygame.mixer.pre_init(28800, -16, 2, 2048) # setup mixer to avoid sound lag
mixer.init()

try:
    mixer.music.load("media/spaceInvaders.wav")
    sound = mixer.Sound('media/laser.wav')
    sound2 = mixer.Sound('media/explosion.wav')
    sound3 = mixer.Sound('media/gameOver.wav')
    # Setting the volume
    mixer.music.set_volume(0.7)
except:
    print("couldn't load sound files")

def laserSound():
    sound = mixer.Sound('media/laser.wav')
    sound.set_volume(0.3)
    sound.play()

def explosionSound():
    sound = mixer.Sound('media/explosion.wav')
    sound.set_volume(0.1)
    sound.play()

def gameOverSound():
    sound = mixer.Sound('media/gameOver.wav')
    sound.set_volume(0.07)
    sound.play()

def backgroundMusic():
    mixer.music.set_volume(0.05)
    mixer.music.play()

# set up screen
mainScreen = turtle.Screen()
mainScreen.title("Space Invaders")
mainScreen.bgpic("spaceInvBg.png")
mainScreen.tracer(0)

# register the shapes
mainScreen.register_shape("player.gif")
mainScreen.register_shape("invaders.gif")
mainScreen.register_shape("bullet.gif")
# Work out how to do sounds
# maybe change player image

# Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

# set the score
score = 0

# drawing the score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
scorestring = "Score: %s" %score
score_pen.write(scorestring, False, align="left", font= ("Arial", 14, "normal"))
score_pen.hideturtle()

# create the player
player = turtle.Turtle()
player.color("blue")
player.shape("player.gif")
player.penup()
player.speed(0)
player.setposition(0,-250)
player.setheading(90)
playerSpeed = 15

# Multiple enemies
number_of_enemies = 6
enemies = []

for i in range(number_of_enemies):
    # create the enemy
    enemies.append(turtle.Turtle())

for enemy in enemies:
    enemy.color("red")
    enemy.shape("invaders.gif")
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-200, 200)
    y = random.randint(100, 250)
    enemy.setposition(x, y)
    enemy.hideturtle()

enemyspeed = 0.15

# create the player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("bullet.gif")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5,0.5)
bullet.hideturtle()

bulletspeed = 0.55

# define bullet state
# ready - ready to fire
# fire - bullet is firing
bulletstate = "ready"

# move the player left and right
def move_left():
    x = player.xcor()
    x -= playerSpeed
    if x < -280:
        x = -280
    player.setx(x)

def move_right():
    x = player.xcor()
    x += playerSpeed
    if x > 280:
        x = 280
    player.setx(x)

def fire_bullet():
    # Declaring bulletstate as a global if it needs to be changed
    global bulletstate
    if bulletstate == "ready":
        laserSound()
        bulletstate = "fire"
        # move the bullet to just above player
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()

def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if distance < 15:
        return True
    else:
        return False

def startGame():
    global gameState
    gameState = "game"

isPaused = False

def togglePause():
    global isPaused
    if isPaused == True:
        isPaused = False
    else:
        isPaused = True

# create keyboard bindings
mainScreen.listen()
mainScreen.onkeypress(move_left, "Left",)
mainScreen.onkeypress(move_right, "Right")
mainScreen.onkeypress(fire_bullet, "space")
mainScreen.onkeypress(startGame, "s")
mainScreen.onkeypress(togglePause, "p")

# main game loop

backgroundMusic()
while True:

    if not isPaused:
        if gameState=="splash" :
            mainScreen.bgpic("introScreen.png")
            player.hideturtle()
            bullet.hideturtle()

        elif gameState=="game" :
            mainScreen.bgpic("spaceInvBg.png")
            player.showturtle()

            for enemy in enemies :
                enemy.showturtle()
                # move the enemy
                x = enemy.xcor()
                x += enemyspeed
                enemy.setx(x)

                # move the enemy back and down
                if enemy.xcor() > 280 :

                    # moves all enemies down
                    for e in enemies :
                        y = e.ycor()
                        y -= 40
                        e.sety(y)
                    # changes direction
                    enemyspeed *= -1

                if enemy.xcor() < -280 :
                    for e in enemies :
                        y = e.ycor()
                        y -= 40
                        e.sety(y)
                    enemyspeed *= -1
                # checking for collision between bullet and enemy
                if isCollision(bullet, enemy) :
                    explosionSound()
                    # reset bullet
                    bullet.hideturtle()
                    bulletstate = "ready"
                    bullet.setposition(0, -400)
                    # reset the enemy
                    x = random.randint(-200, 200)
                    y = random.randint(100, 250)
                    enemy.setposition(x, y)
                    # update score
                    score += 10
                    if score % 150==0 and score!=0 :
                        playerSpeed += 3

                    if score % 100==0 and score!=0 :
                        bulletspeed += 0.05

                    if score % 50==0 and score!=0 :
                        if enemyspeed >=0.01:
                            enemyspeed += 0.05
                        elif enemyspeed <= -0.01:
                            enemyspeed += -0.03

                    scorestring = "Score: %s" % score
                    score_pen.clear()
                    score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))

                if isCollision(player, enemy) :
                    player.hideturtle()
                    enemy.hideturtle()
                    print("Game Over")
                    break

            # move the bullet
            if bulletstate=="fire" :
                y = bullet.ycor()
                y += bulletspeed
                bullet.sety(y)

            # Checking bullet reach top border
            if bullet.ycor() > 275 :
                bullet.hideturtle()
                bulletstate = "ready"

            # checking for collision between bullet and enemy
            if isCollision(bullet, enemy) :
                # reset bullet
                bullet.hideturtle()
                bulletstate = "ready"
                bullet.setposition(0, -400)
                # reset the enemy
                enemy.setposition(-200, 250)

            if isCollision(player, enemy) :
                player.hideturtle()
                enemy.hideturtle()
                gameOverSound()
                gameState = "gameover"

            if enemy.ycor() < -225 :

                gameOverSound()
                gameState = "gameover"

        # game over state
        else :
            # enemies/player/bullet dissapear
            for e in enemies :
                e.hideturtle()
            mixer.music.fadeout(2)
            player.hideturtle()
            bullet.hideturtle()
            # Game over screen with score
            mainScreen.bgpic("gameOverScreen.png")
            score_pen = turtle.Turtle()
            score_pen.speed(0)
            score_pen.color("white")
            score_pen.penup()
            score_pen.setposition(-80, -200)
            scorestring = "Score: %s" % score
            score_pen.write(scorestring, False, align="left", font=("Arial", 30, "normal"))
            score_pen.hideturtle()

    # if paused
    else:
        mainScreen.bgpic("pauseScreen.png")
        for e in enemies :
            e.hideturtle()
        player.hideturtle()
        bullet.hideturtle()
        mainScreen.update()

    mainScreen.update()








