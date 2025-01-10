import pygame
import time
import random

pygame.init()

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
        self.playerRect = pygame.Rect(400, 100, 50, 50)
        self.speed = 5
        self.velocity_y = 0
        self.is_on_ground = False
        self.color = GREEN
        self.canMove = True
        self.time_counter = 0
        



    #Moves the player verticaly, if y velocity is -, player goes up, if + player goes down
    def apply_Ymovement(self):
        # Apply affecting vertical speed
        gravity = 0.4
        if not self.is_on_ground:
            self.velocity_y += gravity
                
        else:
            self.velocity_y = 0

            
    def startMovAgainTimer(self):
        if not self.time_counter == 150:
            self.time_counter += 1
        else:
            self.time_counter = 0
            self.canMove = True
            
    
    def move(self):
        
        keys = pygame.key.get_pressed()

        #move the player according to left and right
        if self.canMove: 
            if keys[pygame.K_LEFT]:
                self.playerRect.x -= self.speed
            if keys[pygame.K_RIGHT]:
                self.playerRect.x += self.speed

            # Vertical movement (jumping)

                
            if keys[pygame.K_UP] and self.is_on_ground:
                self.is_on_ground = False
                # self.collidingGround = False
                self.velocity_y = -15
        else:
            self.startMovAgainTimer()
            

        #do the y moving logic
        self.apply_Ymovement()

        
        # Move player vertically according to the velocity
        self.playerRect.y += self.velocity_y

        

        

class Enemy:  
    # initializing player variables
    def __init__(self):
        self.enemyRect = pygame.Rect(100, 400, 50, 50)
        self.speed = 3
        self.velocity_y = 0
        self.is_on_ground = False
        self.color = LIGHT_BLUE
        self.collidingSideGround = True
        self.deleteEnemy = False


    #Moves the player verticaly, if y velocity is -, player goes up, if + player goes down
    def apply_Ymovement(self):
        # Apply affecting vertical speed
        gravity = 0.4
        if not self.is_on_ground:
            self.velocity_y += gravity
                
        else:
            self.velocity_y = 0

#
    
    def move(self, player):
        
        keys = pygame.key.get_pressed()

        #move the player according to left and right
        if player.x < self.enemyRect.x:
            self.enemyRect.x -= self.speed
        if player.x > self.enemyRect.x:
            self.enemyRect.x += self.speed

        # Vertical movement (jumping)

 
        if self.is_on_ground \
            and \
            (self.collidingSideGround or (self.enemyRect.y > player.y 
            and \
            ((self.enemyRect.x > player.x - 100 and self.enemyRect.x < player.x) 
            or \
            (self.enemyRect.x < player.x + 100 and self.enemyRect.x > player.x)))):
            
            self.is_on_ground = False
            # self.collidingGround = False
            self.velocity_y = -15


        #do the y moving logic
        self.apply_Ymovement()

        
        # Move player vertically according to the velocity
        self.enemyRect.y += self.velocity_y

        
class Wall():
    def __init__(self):
        height = 500
        self.speed = 5
        self.direction = 1
        self.Xposition = 0
        self.wallRect = pygame.Rect(self.Xposition, 50, 50, height)
        
    def move(self):
        if self.direction == 1:
            self.wallRect.x += self.speed
        else:
           self.wallRect.x -= self.speed


    
             

     
#making a variable accesable everywhere, with the width of the obstacles
obstacleWidth = 70

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
            self.left_wall.y = self.PositionSize.y + 10
            self.top_wall.y = self.PositionSize.y
            self.right_wall.y = self.PositionSize.y + 10
            self.PositionSize.x = screenX  

#work in progress feature    
class Weather():
    def __init__(self):
        self.weatherCounter = 0
        self.rainy = False
        self.normal = True
        self.weatherType = ["rainy", "normal"]
        self.rainParticles = []
        self.numberOfRain = 0

        
    def changeWeather(self):
        
        match random.choice(self.weatherType):     
            case 'normal':
                print('normal')
                self.rainParticles = []
            case 'rainy':
                
                print('rainy')
                
                self.rainParticles.append(Particles(5 * 120, -50))
                
        print("tem")
    def updateRain(self):
        if not self.rainParticles == []:
            for i in range(13):
                self.rainParticles.append(Particles(i * 100, 0))
            
            for particle in self.rainParticles:
                if particle.shouldRemove():
                    self.rainParticles.remove(particle)
                particle.move()
                pygame.draw.rect(screen, (BLUE), particle.particleRect)
        
            

class CollisionHandler:
    def __init__(self):
        self.playerHasCollided = False
        self.enemyHasCollided = False
        self.particleHasCollided = False
        
        self.collidingPlayer = False
        self.collidingEnemy = False
        self.collidingParticle = False
         
        self.playerCollidedGronds = []
        self.enemyCollidedGrounds = []
        self.particleCollidedGrounds = []
        
        self.time_counter = 0
    def windowCollisions(self, entity, entityRect, playerDieOnTouch, isWall):
        # Prevent the entity from going out of bounds
        if not isWall:
            if entityRect.x > screenX - entityRect.width:
                entityRect.x = screenX - entityRect.width
                if playerDieOnTouch == True:
                    pygame.quit() 
            elif entityRect.x < 0:
                entityRect.x = 0
                if playerDieOnTouch == True:
                    pygame.quit() 
            if entityRect.y > screenY - entityRect.height:
                entityRect.y = screenY - entityRect.height
                entity.velocity_y = 0
                entity.is_on_ground = True
            elif entityRect.y < 0:
                entityRect.y = 0
        elif isWall:
            if entityRect.x > screenX:
                entityRect.x = -50


    
    def checkforGoundCollisions(self, grounds, player, enemy, particles):
        self.playerHasCollided = False
        self.enemyHasCollided = False
        for ground in grounds:
            if self.checkSubWallCollisions(player.playerRect, player, ground):
                self.playerCollidedGronds.append(ground)
                self.playerHasCollided = True
            if not enemy == None:
                if self.checkSubWallCollisions(enemy.enemyRect, enemy, ground):
                    self.enemyCollidedGrounds.append(ground)
                    self.enemyHasCollided = True
            # if not particles == None:
            #     for particle in particles:
            #         if self.checkSubWallCollisions(particle.particleRect, particle, ground):
            #             self.particleCollidedGrounds.append(ground)
            #             self.particleHasCollided = True

        
        if self.playerHasCollided: #player collided with a ground(s)
            for collidedGround in self.playerCollidedGronds:
                self.groundCollisions(collidedGround, player, player.playerRect)
        else:
            player.is_on_ground = False 
            
        if not enemy == None:    
            if self.enemyHasCollided:
                for collidedGround in self.enemyCollidedGrounds:
                    self.groundCollisions(collidedGround, enemy, enemy.enemyRect)
            else:
                enemy.is_on_ground = False
        # if not enemy == None:
        #     if self.particleHasCollided:
        #         for collidedGround in self.particleCollidedGrounds:
        #             for particle in particles:
        #              self.groundCollisions(collidedGround, particle, particle.particleRect)
    def checkSubWallCollisions(self, entityRect, entity, mainGround):
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

            
    
    
    def groundCollisions(self, collidedGround, entity, entityRect):
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
                
    def checkEnemyPlayerCollision(self, enemy, player):
        if player.playerRect.colliderect(enemy.enemyRect):
            player.canMove = False
            enemy.deleteEnemy = True
            return True
            
            
class Particles():
    def __init__(self, xposition, yposition):
        self.particleRect = pygame.Rect(xposition, yposition, random.randint(5, 10), random.randint(5, 10))
        self.dirX = random.randint(-2, 2)
        self.velocity_y = random.randint(-5, 0)
        self.lifeSpan = 500 #game ticks
        self.is_on_ground = False
        self.counter = 0
    def move(self):
        
        self.particleRect.x += self.dirX
        
        gravity = 0.4
        
        self.velocity_y += gravity
        
        # Move player vertically according to the velocity
        self.particleRect.y += self.velocity_y
    def shouldRemove(self):
        if self.counter == self.lifeSpan:
            self.counter = 0
            return True
        else: 
            self.counter += 1
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
        self.time_counter = 0
        self.weather_counter = 0
        self.has_collided = False
        self.enemySpawn_Counter = 0
        self.wall = Wall()
        self.deleteEnemy = False
        self.makeFreezeParticales = False
        self.previousEnemyColor = None
        
        #choosing the number of obstacles that fill the screen
        for i in range(int(screenX/obstacleWidth) + 2):
            
            self.grounds.append(Floor(screenX - i * obstacleWidth))

    def game_loop(self):
        while self.running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            screen.fill(BLACK)
            if self.enemy:
                if self.enemy.deleteEnemy:
                    
                    self.enemy = None
            
            if self.enemy == None:
                if self.enemySpawn_Counter == 500:
                    self.enemy = Enemy()
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
            
            self.handleCollisions.windowCollisions(self.player, self.player.playerRect, True, False)
            
            if not self.enemy == None:
                self.previousEnemyColor = self.enemy.color 
                self.handleCollisions.windowCollisions(self.enemy, self.enemy.enemyRect, False, False)
                
                if self.handleCollisions.enemyCanJumpWallCollisions(self.grounds, self.enemy):
                    self.enemy.collidingSideGround = True
                else:
                    self.enemy.collidingSideGround = False

                    
            
            self.handleCollisions.checkforGoundCollisions(self.grounds, self.player, self.enemy, self.particles)
            
            
            
            self.handleCollisions.windowCollisions(self.wall, self.wall.wallRect, False, True)
            
            self.handleCollisions.wallCollisions(self.wall, self.player, self.player.playerRect)
            


            
            collidingPlayer = False
            collidingEnemy = False
            
            collidedGroundsPlayer = []
            collidedGroundsEnemy = []
            
            
            
            
   
            if not self.enemy == None:
                self.handleCollisions.checkEnemyPlayerCollision(self.enemy, self.player)
                # if self.handleCollisions.checkEnemyPlayerCollision(self.enemy, self.player):
                #     self.makeFreezeParticales = True
                    
                    
            if not self.player.canMove:
            #WORK IN PRORESS
                self.particles.append( Particles(self.player.playerRect.x + self.player.playerRect.width / 2, self.player.playerRect.y + self.player.playerRect.height /2))
            
            
            
            
            #move the player
            self.player.move()
            pygame.draw.rect(screen, self.player.color, self.player.playerRect)         
            self.weather.updateRain()
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
                particle.move()
                pygame.draw.rect(screen, (self.previousEnemyColor), particle.particleRect)

                
            
            pygame.display.flip()

            clock.tick(60)

        pygame.quit()
    def killEnemy(self):
        self.enemy = None

if __name__ == "__main__":
    game = Game()
    game.game_loop()