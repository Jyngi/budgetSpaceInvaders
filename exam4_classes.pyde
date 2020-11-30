# I made this program with Objects to see if I could. If a function version is preferred, I can submit that as well. 
# Instantiate class UFO with attributes for x coordinate, opacity for collision and image
class ufo(object):
    def __init__(self, index):
        self.x = WIDTH_UFO/2 + (index * 75)
        self.opacity = 255
        self.imgShip = loadImage('enemy.png')
    def display(self):
        # As long as a ufo has not been hit by a bullet, display ufo
        global y
        if self.opacity != 0:
            fill(0,0,0,0)
            noStroke()
            rect(self.x,y, WIDTH_UFO, HEIGHT_UFO)
            imageMode(CENTER)
            image(self.imgShip,self.x,y)
    def ufoMovement(self):
        # Move the UFO a set number of pixels left or right depending on the state
        global pulseTimer, ufoState
        if ufoState == 'left':
            self.x += -1
        if ufoState == 'right':
            self.x += 1
        for bullet in bulletArray:
            bullet.collision(self);
    def ufoBoundsDetection(self):
        # Code to bounce the set of ufo's back and forth. A sin equation could've been used, but couldn't figure that out
        global ufoState, yCounter, runOnce
        if self.x + 51 >= 960:
            ufoState = 'left'
            yCounter += 1
        if self.x <= 0:
            ufoState = 'right'
            yCounter += 1
    def moveY(self):
        # If the yCounter increments increase the Y of all the ufo's down by 10 pixels
        global yCounter, runOnce, y
        if yCounter % 2 == 1 and runOnce == 0:
            runOnce = 1
            y += 10
        if yCounter % 2 != 1 and runOnce == 1:
            y += 10
            runOnce = 0
    def distanceCheck(self):
        # For some reason UFO's will slowly grow apart without this ufo check. Checks every frame if the UFO's are apart by a set number of pixels. If not it sets the them to that range
        distanceCheckArray = []
        for ufo in drawnUFO:
            distanceCheckArray.append(ufo.x) 
        tempX = distanceCheckArray[0]
        tempArray = 0
        for ufo in drawnUFO:
            if tempArray != 0:
                ufo.x = tempX + (75 * tempArray)
            tempArray += 1
 
class bullets(object):
    #Initial object bullets with an x coord/ycoord from the player. 
    def __init__(self, x):
        self.x = x
        self.y = playerY
        self.bulletImage = loadImage('bullet.png')
    def display(self):
        # Display Bullets
        fill(0,0,0,0)
        image(self.bulletImage,self.x,self.y)
        rect(self.x,self.y,10,10)
    def move(self):
        # bullets move automatically 2 pixels upwards
        self.y += -2;
    def collision(self, ufoOBJ):
        # If a ufo has not been destroyed yet (updated through opacity) and a bullet collides set that UFO's opacity to 0 and also increment energy for super by a random value between 17 and 22
        global y, drawnUFO, regenCounter, energy
        if ufoOBJ.opacity != 0:
            if self.x <= ufoOBJ.x + 25 and self.x>= ufoOBJ.x - 25:
                if self.y <= y + 10 and self.y >= y - 10:
                    ufoOBJ.opacity = 0
                    for i in range(random.randint(17,22)):
                        energy += 1
    def bulletBoundsDetection(self,index):
        # Deletes out of Bounds bullets
        if self.y + 50 <= 0:
            bulletArray.pop(index)
            
import random    
WIDTH = 960
HEIGHT = WIDTH
WIDTH_UFO = 50
HEIGHT_UFO = 20
bulletCooldown = 60
drawnUFO = []
timerUFO = 0
pulseTimer = 0
ufoState = 'right'
yCounter = 0
runOnce  = 0
y = HEIGHT_UFO
playerX = WIDTH/2
playerY = HEIGHT - 100
playerInput = [False, False, False]
hSpeed = 2
bulletArray = []
fireTimer = 0
energy = 0
superState = False
imgPlayer = loadImage('player.png')
imgShip = loadImage('enemy.png')
imgBullet = loadImage('bullet.png')
stars = []



def setup():
    global imgPlayer, imgShip, imgBullet
    frameRate(120)
    size(WIDTH,HEIGHT)
    populateArray()
    imgPlayer = loadImage('player.png')
    imgShip = loadImage('enemy.png')
    imgBullet = loadImage('bullet.png')
    
    # Draw updates players, ufo and bullets every frame
def draw():
    global drawnUFO, playerOBJ, playerX, playerY, bulletArray, fireTimer, playerInput, imgPlayer,imgShip,imgBullet
    ellipseMode(CENTER)
    rectMode(CENTER)
    background(0)
    super()
    backgroundStars()
    
    for ufoCount in drawnUFO:
        ufoCount.display()
        ufoCount.ufoMovement()
        ufoCount.ufoBoundsDetection()
        ufoCount.moveY()
        ufoCount.distanceCheck()
        for shot in bulletArray:
            shot.collision(ufoCount)
            
    index = 0
    for shot in bulletArray:
        shot.display()
        shot.move()
        shot.bulletBoundsDetection(index)
        # shot.bulletTrail()
        index += 1
    # This makes it so that if space bar is held down and right/left input is given it'll continue to fire bullets.     
    if playerInput[2] == True and fireTimer >= bulletCooldown:
        fireTimer = 0
        fireBullets()
        
    ufoRegen()
    
    fill(255,0,0)
    image(imgPlayer,playerX,playerY)
    playerMovement();
    fireTimer += 1

# Populate an array with UFO object
def populateArray():
    for i in range(5):
        drawnUFO.append(ufo(i))
# If the number of ufo's that have been hit having the value of 0 exceeds that of the length of the UFO list, then regenerate UFO's
def ufoRegen():
    global drawnUFO, y
    ufoDestroyed = sum(ufo.opacity == 0 for ufo in drawnUFO)
    if ufoDestroyed == len(drawnUFO) or y >= HEIGHT/2:
        drawnUFO = []
        y = HEIGHT_UFO
        populateArray()
# If the energy value exceeds/is under certain values switch between super states    
def super():
    global bulletCooldown, energy, superState
    rectMode(CORNERS)
    stroke(255,255,255)
    fill(0,0,0,0)
    rect(25,25,50,300)
    fill(255,255,255)
    if energy < 300:
        rect(25,25,50,25+energy)
    if energy >= 300:
        superState = True
    if superState == True:
        bulletCooldown = 0
        energy += -1 
        if energy <= 0:
            superState = False
            bulletCooldown = 60
    textMode(CENTER)
    textSize(20)
    text('Super',15,15)
    text('Meter',15,320)            
    
# Key Input Reader    
def keyPressed():
    global playerInput, fireTimer, energy
    if key == 'a' or key == 'A' or keyCode == LEFT:
        playerInput[0] = True
    if key == 'd' or key == 'D':
        playerInput[1] = True
    if keyCode == LEFT:
       playerInput[0] = True 
    if keyCode == RIGHT:
        playerInput[1] = True
    if key == ' ':
        playerInput[2] = True
        if fireTimer >= bulletCooldown:
            fireTimer = 0
            fireBullets()
    if key == 'c' or key == 'C':
        energy = 301

def keyReleased():
    global playerInput
    if key == 'a' or key == 'A':
        playerInput[0] = False
    if key == 'd' or key == 'D':
        playerInput[1] = False   
    if keyCode == LEFT:
        playerInput[0] = False
    if keyCode == RIGHT:
        playerInput[1] = False
    if key == ' ':
        playerInput[2] = False

# Player Movement
def playerMovement():
    global playerX, playerY, playerInput, hSpeed
    hPLRMovement = -playerInput[0] + playerInput[1]
    hSpeed = 2
    if playerX + hSpeed >= WIDTH:
        playerX = WIDTH - 10    
    if playerX - hSpeed <= 0:
        playerX = 10
    
    playerX += hSpeed * hPLRMovement
    
# appends object Bullets to array bulletArray
def fireBullets():
    global playerX, bulletArray
    bulletArray.append(bullets(playerX));

def backgroundStars():
    global stars
    stars.append([random.randrange(50,WIDTH-50),-100])
    for x,y in stars:
        rectMode(CORNER)
        fill(255)
        rect(x,y,3,3)
    for star in stars:
        star[1] += 2
        if star[1] > HEIGHT:
            stars.pop(0)
    
        
