import pygame
import time
import random
import os
from pygame import mixer

pygame.init()
# mixer.init()
# #set up music
# mixer.music.set_volume(0.7) 
# music_option = ("retro.mp3", "quirky.mp3")
# music = random.choice(music_option)
# mixer.music.load(music)
# mixer.music.play(-1)


# create constants
screenX = 1200
screenY = 800
screen = pygame.display.set_mode((screenX, screenY))
clock = pygame.time.Clock()
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (100, 100, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)



#class for player
class Player:
    
    # initializing player variables
    def __init__(self):
        self.gameOver = False

        self.playerRect = pygame.Rect(400, 100, 50, 50)
        self.speed = 7
        self.velocity_y = 0
        
        self.is_on_ground = False
        self.color = GREEN
        self.canMove = True
        self.freeze_counter = 0
        self.blood_timer = 0
        self.isHit = False




    #Moves the player verticaly, if y velocity is -, player goes up, if + player goes down
    def apply_Ymovement(self):
        gravity = 0.4
        if not self.is_on_ground:
            self.velocity_y += gravity #keep on adding gravity, which switches the negative velocity(go up) to positive(go down)
        else:
            self.velocity_y = 0

    def startHitParticlesTimer(self):
        if not self.blood_timer == 100:
            self.blood_timer += 1
        else:
            self.blood_timer = 0
            self.isHit = False

    def startMovAgainTimer(self):
        if not self.freeze_counter == 150:
            self.freeze_counter += 1
        else:
            self.freeze_counter = 0
            self.canMove = True
            
    
    def move(self):
        
        keys = pygame.key.get_pressed()

        
        if self.canMove:
            #user key inputs
            if keys[pygame.K_LEFT]:
                self.playerRect.x -= self.speed
            if keys[pygame.K_RIGHT]:
                self.playerRect.x += self.speed

            # Vertical movement (jumping)
            if keys[pygame.K_UP] and self.is_on_ground:
                self.is_on_ground = False
                self.velocity_y = -15

                # #play sound effect
                # sound = mixer.Sound("jump.mp3")
                # sound.play()

        #do the y moving logic
        self.apply_Ymovement()

        
        # Move player vertically according to the velocity
        self.playerRect.y += self.velocity_y
 

        

class Enemy:  
    # initializing enemy variables
    def __init__(self):
        self.height = 40
        self.width = 40
        self.enemyRect = pygame.Rect(random.randint(100, 1100), -50, self.height, self.width)
        self.speed = 3
        self.velocity_y = 0
        self.is_on_ground = False
        self.color = BLUE
        self.collidingSideGround = True
        self.deleteEnemy = False

        #choose a random enemyType
        enemyTypes = ["freeze", "damage"]
        self.enemyType = random.choice(enemyTypes)

        #assign color based on type
        match self.enemyType:
            case "freeze":
                self.color = LIGHT_BLUE
                return
            case "damage":
                self.color = RED


    #Moves the enemy verticaly, if y velocity is -, enemy goes up, if + enemy goes down
    def apply_Ymovement(self):
        gravity = 0.4
        if not self.is_on_ground:
            self.velocity_y += gravity
                
        else:
            self.velocity_y = 0

    
    def move(self, player):
        
        keys = pygame.key.get_pressed()

        #move the enemy left and right towards the player,
        if player.x < self.enemyRect.x:
            self.enemyRect.x -= self.speed
        if player.x > self.enemyRect.x:
            self.enemyRect.x += self.speed

        # Vertical movement (jumping)

        #if we are on ground, and either touching a sideGround or we are within 100 pixels of the player: Jump
        if self.is_on_ground \
            and \
            (self.collidingSideGround or (self.enemyRect.y > player.y 
            and \
            ((self.enemyRect.x > player.x - 100 and self.enemyRect.x < player.x) 
            or \
            (self.enemyRect.x < player.x + 100 and self.enemyRect.x > player.x)))):
            
            self.is_on_ground = False
            self.velocity_y = -13


        #do the y moving logic
        self.apply_Ymovement()

        
        # Move player vertically according to the velocity
        self.enemyRect.y += self.velocity_y



#moves accross the top of the screen (not a ground)
class Wall():
    def __init__(self):
        HEIGHT = 525
        self.speed = 5
        self.Xposition = 0
        self.wallRect = pygame.Rect(self.Xposition, 50, 50, HEIGHT)
        
    def move(self):
        self.wallRect.x += self.speed


     
#making a variable accesable everywhere, with the width of the obstacles
#variable accessed in main class
obstacleWidth = 100

class Floor():

    #initializing all variables needed for Obstacles
    def __init__(self, Xposition):
        #base of each obstacle
        self.PositionSize = pygame.Rect(Xposition, screenY - self.choose_height() * 50, obstacleWidth, 200)
        self.speed = 5
        
        #extra walls used for collisions:
        self.left_wall = pygame.Rect(self.PositionSize.left, self.PositionSize.y + 10, 10, 200) 
        self.top_wall = pygame.Rect(self.PositionSize.left + 5, self.PositionSize.y, obstacleWidth - 10, 10)
        self.right_wall = pygame.Rect(self.PositionSize.right - 10, self.PositionSize.y + 10, 10, 200)
        
        
    #making the height of each object random
    def choose_height(self):
        return random.randint(1, 4)
            
    
    def move(self):

        #moving base obstacle
        self.PositionSize.x -= self.speed

        #moving secondary walls with the base
        self.left_wall.x = self.PositionSize.left
        self.top_wall.x = self.PositionSize.x + 5
        self.right_wall.x = self.PositionSize.right - 10
        
        #resetting the position of obstacles when reached the edge of the screen
        if self.PositionSize.x + self.PositionSize.width < 0:
            self.PositionSize.y = screenY - self.choose_height() * 50

            #moving the secondary walls with the base
            self.left_wall.y = self.PositionSize.y + 10
            self.top_wall.y = self.PositionSize.y
            self.right_wall.y = self.PositionSize.y + 10
            self.PositionSize.x = screenX  

   
class Weather():
    def __init__(self):
        self.weatherCounter = 0
        self.weatherTypes = ["rainy", "normal", "snow"]

        self.weatherParticles = []
        self.weatherType = random.choice(self.weatherTypes)
        self.particleColor = WHITE
        
    def changeWeather(self):
        self.weatherType = random.choice(self.weatherTypes)
        #depending on the weather different items are to be made/removed
        match self.weatherType:     
            case 'normal':
                self.weatherParticles = []
            case 'rainy':
                self.particleColor = BLUE
                #creating an initial particle, so updateWeather() detects that its raining
                self.weatherParticles.append(Particles(5 * 120, -50))
            case 'snow':
                self.particleColor = WHITE
                #creating an initial particle, so updateWeather() detects that its raining
                self.weatherParticles.append(Particles(5 * 120, -50))
                
    def updateWeather(self):
        if not self.weatherParticles == []:

            #spawns in 6 particle generators above the screen, particles fall accross like rain or snow
            for i in range(6):
                self.weatherParticles.append(Particles(i * 250, -100))
            
            for particle in self.weatherParticles:
                #checking to remove particle, if it reached end of its lifespan
                if particle.shouldRemove():
                    self.weatherParticles.remove(particle)
                
                #physics between rain and snow are different
                if self.weatherType == 'snow':
                    particle.move(True)
                else:
                    particle.move(False)

                #drawing each particle
                pygame.draw.rect(screen, (self.particleColor), particle.particleRect)
        
class Particles():

    
    def __init__(self, xposition, yposition):
        #particle rectangle, size is a bit random
        self.particleRect = pygame.Rect(xposition, yposition, random.randint(5, 10), random.randint(5, 10))

        #each particle moves either left or right
        self.speed = random.randint(-2, 2)
        self.velocity_y = random.randint(-5, 0)
        
        self.lifeSpan = 500 #game ticks
        self.life_countdown = 0


    def move(self, isSnow):
        self.particleRect.x += self.speed
        
        #changing physics based on if particle is snow
        if not isSnow:
            gravity = 0.4
        else:
            gravity = 0.05

        # Moves particle vertically according to the velocity
        self.velocity_y += gravity
        self.particleRect.y += self.velocity_y


    def shouldRemove(self):
        if self.life_countdown == self.lifeSpan:
            self.life_countdown = 0
            return True
        else: 
            self.life_countdown += 1            

class CollisionHandler:
    def __init__(self):
        self.playerHasCollided = False
        self.enemyHasCollided = False
        
        #keep track of what is colliding
        self.collidingPlayer = False
        self.collidingEnemy = False
        
        #contains arrays of objects that have collided
        self.entityCollidedGrounds = []
        self.enemyCollidedGrounds = []

# collisions with the window edge
    def windowCollisions(self, entity, entityRect, playerDieOnTouch, isWall):
        #
        if not isWall:
            #right screen edge
            if entityRect.x > screenX - entityRect.width:

                #stops entity from going past the screen
                entityRect.x = screenX - entityRect.width
                #if player touches edge, game over
                if playerDieOnTouch == True:
                    entity.gameOver = True
                #moves the enemy up, to avoid bugs
                entityRect.y = -200

            #left screen edge
            elif entityRect.x < 0:

                #stops entity from going past the screen
                entityRect.x = 0
                #if player touches edge, game over
                if playerDieOnTouch == True:
                    entity.gameOver = True
                #moves the enemy up, to avoid bugs
                entityRect.y = -200

            #if an entity go's through the ground, it stays above the bottom of the screen
            if entityRect.y > screenY - entityRect.height:
                entityRect.y = screenY - entityRect.height
                entity.velocity_y = 0
                entity.is_on_ground = True
            elif entityRect.y < 0:
                entityRect.y = 0

        #for the wall, should move back to the other side
        elif isWall:
            if entityRect.x > screenX:
                entityRect.x = -50


    
    def checkforGroundCollisions(self, grounds, entity, entityRect):
        self.entityHasCollided = False
        self.enemyHasCollided = False

        #checking through every ground and their sub grounds for collisions
        for ground in grounds:
            #for player
            if self.checkSubGroundCollisions(entityRect, entity, ground):
                self.entityCollidedGrounds.append(ground) #save collided grounds
                self.entityHasCollided = True #remembering there has been a collision

        #checking if player collided with a ground(s)
        if self.entityHasCollided: 
            #for every ground we collided with call the ground collision handler
            #to figure out what to do and how we are colliding
            for collidedGround in self.entityCollidedGrounds:
                self.groundCollisionHandler(collidedGround, entity, entityRect)
        else:
            entity.is_on_ground = False 


    def checkSubGroundCollisions(self, entityRect, entity, mainGround):
        if entityRect.colliderect(mainGround.left_wall) \
                        or entityRect.colliderect(mainGround.top_wall) \
                        or entityRect.colliderect(mainGround.right_wall):
                    return True

    

        
    def enemyCanJumpWallCollisions(self, grounds, enemy):
        for ground in grounds:
            if enemy.enemyRect.colliderect(ground.left_wall) or enemy.enemyRect.colliderect(ground.right_wall):
                enemy.collidingSideGround = True
                return True


    
    def wallCollisions(self, wall, entity, entityRect):
        if entityRect.colliderect(wall.wallRect) and entityRect.left < wall.wallRect.left:
            entityRect.right = wall.wallRect.left
            
        elif entityRect.colliderect(wall.wallRect) and entityRect.right > wall.wallRect.right:
            entityRect.left = wall.wallRect.right

            
    
    
    def groundCollisionHandler(self, collidedGround, entity, entityRect):
        if entity.velocity_y > 15:
            if entityRect.colliderect(collidedGround.top_wall):
                entityRect.bottom = collidedGround.top_wall.top + 1
                entity.is_on_ground = True
                
            elif entityRect.colliderect(collidedGround.left_wall):
                entityRect.right = collidedGround.left_wall.left
                entity.collidingWall = True
            elif entityRect.colliderect(collidedGround.right_wall):
                entityRect.left = collidedGround.right_wall.right
                entity.collidingWall = True
        else:
            #if im going slow, then check my side collisions first
            if entityRect.colliderect(collidedGround.left_wall):
                entityRect.right = collidedGround.left_wall.left
                self.collidingWall = True
            elif entityRect.colliderect(collidedGround.right_wall):
                entityRect.left = collidedGround.right_wall.right
                entity.collidingWall = True
            elif entityRect.colliderect(collidedGround.top_wall):
                entityRect.bottom = collidedGround.top_wall.top + 1
                entity.is_on_ground = True
                
    def checkEnemyPlayerCollision(self, enemy, player, enemyType):
        if enemyType == "freeze":
            if player.playerRect.colliderect(enemy.enemyRect):
                player.canMove = False
                enemy.deleteEnemy = True
                # sound = mixer.Sound("pop.mp3")
                # sound.play()
                return True
                
        elif enemyType == "damage":
            if player.playerRect.colliderect(enemy.enemyRect):
                player.playerRect.height -= 10
                player.isHit = True
                enemy.deleteEnemy = True
                # sound = mixer.Sound("pop.mp3")
                # sound.play()
                return True

#main part of the game
class Game:
    #initializing all of our objects
    def __init__(self):
        self.running = True

        self.player = Player()
        self.enemy = None
        self.weather = Weather()
        self.handleCollisions = CollisionHandler()
        self.particles = []
        self.grounds = []
        self.wall = Wall()


        
        self.time_counter = 0
        self.weather_counter = 0
        self.has_collided = False
        self.enemySpawn_Counter = 0
        self.deleteEnemy = False
        self.makeFreezeParticales = False
        self.previousEnemyColor = None
        self.my_font = pygame.font.SysFont('Vederna', 70)

        self.timer_timer = 0
        self.timer_seconds = 1
        self.timer_minutes = 0
        self.timer_text = self.my_font.render(f'{self.timer_minutes}:{self.timer_seconds}', False, (BLUE))

        self.secondsToWait = 15
        self.maxDiff = 0
        
        #choosing the number of obstacles that fill the screen
        for i in range(int(screenX/obstacleWidth) + 2):
            
            self.grounds.append(Floor(screenX - i * obstacleWidth))

    def callCollisions(self):
        self.handleCollisions.windowCollisions(self.player, self.player.playerRect, True, False)
        self.handleCollisions.checkforGroundCollisions(self.grounds, self.player, self.player.playerRect)

        if not self.enemy == None:

            self.handleCollisions.wallCollisions(self.wall, self.enemy, self.enemy.enemyRect)
            self.handleCollisions.windowCollisions(self.enemy, self.enemy.enemyRect, False, False)     
            
            #needs to be before calling checkforGroundCollisions() because that functions moves enemy so its no longer colliding
            #for enemyCanJumpWallCollisions enemy needs to be colliding with wall
            
            if self.handleCollisions.enemyCanJumpWallCollisions(self.grounds, self.enemy):
                self.enemy.collidingSideGround = True
            else:
                self.enemy.collidingSideGround = False
            
            self.handleCollisions.checkEnemyPlayerCollision(self.enemy, self.player, self.enemy.enemyType) 
            
            self.handleCollisions.checkforGroundCollisions(self.grounds, self.enemy, self.enemy.enemyRect) #needs to be after checking if colliding with player
        self.handleCollisions.windowCollisions(self.wall, self.wall.wallRect, False, True)
        
        self.handleCollisions.wallCollisions(self.wall, self.player, self.player.playerRect)

    def lvlChanger(self):
        self.secondsToWait -= 1
        if not self.maxDiff == 4:
            if self.secondsToWait == 0:
                for ground in self.grounds:
                    ground.speed += 0.5
                    self.maxDiff += 1
                self.secondsToWait = 15


    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if not self.player.gameOver:
                if self.timer_seconds == 60:
                    self.timer_minutes += 1
                    self.timer_seconds = 0
                    self.timer_text = self.my_font.render(f'{self.timer_minutes}:{self.timer_seconds}', False, (random.randint(0, 230), random.randint(0, 230), random.randint(0, 230)))
                if not self.timer_timer == 60:
                    self.timer_timer += 1
                else:
                    self.timer_text = self.my_font.render(f'{self.timer_minutes}:{self.timer_seconds}', False, (random.randint(0, 230), random.randint(0, 230), random.randint(0, 230)))
                    self.timer_timer = 0
                    self.timer_seconds += 1
                    self.lvlChanger()
                



                screen.fill(BLACK)
                if self.enemy:
                    if self.enemy.deleteEnemy:
                        
                        self.enemy = None
                
                if self.enemy == None:
                    if self.enemySpawn_Counter == 500:
                        self.enemy = Enemy()
                        self.previousEnemyColor = self.enemy.color 
                        self.enemy.deleteEnemy = False
                        self.enemySpawn_Counter = 0
                    else:  
                        self.enemySpawn_Counter += 1
                
                if self.weather_counter == 600:
                    self.weather.changeWeather()
                    self.weather_counter = 0
                    print("test")
                else:
                    self.weather_counter += 1    
                
                self.callCollisions()
                        
                        
                if (not self.player.canMove):
                    self.player.startMovAgainTimer()
                    self.particles.append( Particles(self.player.playerRect.x + self.player.playerRect.width / 2, self.player.playerRect.y + self.player.playerRect.height /2))
                if self.player.isHit:
                    self.player.startHitParticlesTimer()
                    self.particles.append( Particles(self.player.playerRect.x + self.player.playerRect.width / 2, self.player.playerRect.y + self.player.playerRect.height /2))


                if self.player.playerRect.height <= 0:
                    self.player.gameOver = True
                
                


                #move the player
                self.player.move()
                pygame.draw.rect(screen, self.player.color, self.player.playerRect)         
                self.weather.updateWeather()
                self.wall.move()
                pygame.draw.rect(screen, (WHITE), self.wall.wallRect)     

                if not self.enemy == None: 
                    self.enemy.move(self.player.playerRect)
                    pygame.draw.rect(screen, self.enemy.color, self.enemy.enemyRect)
                
                
                for ground in self.grounds: # going through every ground
                    ground.move()
                    #drawing all the grounds, drawing secondary isnt nessasery, but its easier for debugging
                    pygame.draw.rect(screen, (0, 0, 225), ground.left_wall)
                    pygame.draw.rect(screen, (0, 225, 225), ground.top_wall)
                    pygame.draw.rect(screen, (225, 0, 225), ground.right_wall)
                    pygame.draw.rect(screen, (WHITE), ground.PositionSize) #draw the main ground before the secondary ones too see them
                
                for particle in self.particles:
                    if particle.shouldRemove():
                        self.particles.remove(particle)
                    particle.move(False)
                    pygame.draw.rect(screen, (self.previousEnemyColor), particle.particleRect)

                screen.blit(self.timer_text, (1100,760))   
            else:
                # mixer.music.load("quirky.mp3")
                # mixer.music.play() 
                self.enemy = None
                self.weather = None
                self.handleCollisions = None
                self.particles = None
                self.grounds = None
                self.wall = None

                

                gameOver_text = self.my_font.render(f'Game Over', False, (RED))
                finalTime_text = self.my_font.render(f'{self.timer_minutes}:{self.timer_seconds}', False, (RED))

                screen.fill(BLACK)  
                screen.blit(gameOver_text, (450, 300))
                screen.blit(finalTime_text, (550, 400))
            
            pygame.display.flip()

            clock.tick(60)

        pygame.quit()
    def killEnemy(self):
        self.enemy = None

if __name__ == "__main__":
    game = Game()
    game.game_loop()