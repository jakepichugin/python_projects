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

#class for player
class Player:
    
    # initializing player variables
    def __init__(self):
        self.playerRect = pygame.Rect(400, 100, 50, 50)
        self.speed = 5
        self.velocity_y = 0
        self.is_on_ground = False
        self.color = GREEN
        self.collidingGround = False
        self.canMove = True


    #checks if im touching an edge of the screen
    def checkBorder(self):
        # Prevent the player from going out of bounds
        if self.playerRect.x > screenX - self.playerRect.width:
            self.playerRect.x = screenX - self.playerRect.width
            pygame.quit() 
        elif self.playerRect.x < 0:
            self.playerRect.x = 0
            pygame.quit() 
        if self.playerRect.y > screenY - self.playerRect.height:
            self.playerRect.y = screenY - self.playerRect.height
            self.velocity_y = 0
            self.is_on_ground = True
        elif self.playerRect.y < 0:
            self.playerRect.y = 0

    #is called when im colliding with an obstical/ground
    def collision(self, collidedObj):
        # Wall collision (left side)
        # Floor collision
        
        #if im falling fast enough(speed of 10) then I can glitch through the ground
        #So check my collision in the floor first, then with the side
        if self.velocity_y > 10:
            if self.playerRect.colliderect(collidedObj.top_wall):
                self.playerRect.bottom = collidedObj.top_wall.top + 1
                self.is_on_ground = True            
            elif self.playerRect.colliderect(collidedObj.left_wall):
                self.playerRect.right = collidedObj.left_wall.left
            elif self.playerRect.colliderect(collidedObj.right_wall):
                self.playerRect.left = collidedObj.right_wall.right
        else:
            #if im going slow, then check my side collisions first
            if self.playerRect.colliderect(collidedObj.left_wall):
                self.playerRect.right = collidedObj.left_wall.left
            elif self.playerRect.colliderect(collidedObj.right_wall):
                self.playerRect.left = collidedObj.right_wall.right
            elif self.playerRect.colliderect(collidedObj.top_wall):
                self.playerRect.bottom = collidedObj.top_wall.top + 1
                self.is_on_ground = True


    #Moves the player verticaly, if y velocity is -, player goes up, if + player goes down
    def apply_Ymovement(self):
        # Apply affecting vertical speed
        gravity = 0.4
        if not self.is_on_ground:
            self.velocity_y += gravity
                
        else:
            self.velocity_y = 0


            
    
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
                self.collidingGround = False
                self.velocity_y = -15


        #do the y moving logic
        self.apply_Ymovement()

        
        # Move player vertically according to the velocity
        self.playerRect.y += self.velocity_y

        
        # Check borders
        self.checkBorder()
        

class Enemy:  
    # initializing player variables
    def __init__(self):
        self.enemyRect = pygame.Rect(100, 400, 50, 50)
        self.speed = 3
        self.velocity_y = 0
        self.is_on_ground = False
        self.color = YELLOW
        self.collidingGround = False
        self.collidingWall = False


    #checks if im touching an edge of the screen
    def checkBorder(self):
        # Prevent the player from going out of bounds
        if self.enemyRect.x > screenX - self.enemyRect.width:
            self.enemyRect.x = screenX - self.enemyRect.width
        elif self.enemyRect.x < 0:
            self.enemyRect.x = 0
        if self.enemyRect.y > screenY - self.enemyRect.height:
            self.enemyRect.y = screenY - self.enemyRect.height
            self.velocity_y = 0
            self.is_on_ground = True
        elif self.enemyRect.y < 0:
            self.enemyRect.y = 0

    #is called when im colliding with an obstical/ground
    def collision(self, collidedObj):
        # Wall collision (left side)
        # Floor collision

        #if im falling fast enough(speed of 10) then I can glitch through the ground
        #So check my collision in the floor first, then with the side
        if self.velocity_y > 10:
            if self.enemyRect.colliderect(collidedObj.top_wall):
                self.enemyRect.bottom = collidedObj.top_wall.top + 1
                self.is_on_ground = True

            elif self.enemyRect.colliderect(collidedObj.left_wall):
                self.enemyRect.right = collidedObj.left_wall.left
                self.collidingWall = True
            elif self.enemyRect.colliderect(collidedObj.right_wall):
                self.enemyRect.left = collidedObj.right_wall.right
                self.collidingWall = True
        else:
            #if im going slow, then check my side collisions first
            if self.enemyRect.colliderect(collidedObj.left_wall):
                self.enemyRect.right = collidedObj.left_wall.left
                self.collidingWall = True
            elif self.enemyRect.colliderect(collidedObj.right_wall):
                self.enemyRect.left = collidedObj.right_wall.right
                self.collidingWall = True
            elif self.enemyRect.colliderect(collidedObj.top_wall):
                self.enemyRect.bottom = collidedObj.top_wall.top + 1
                self.is_on_ground = True



    #Moves the player verticaly, if y velocity is -, player goes up, if + player goes down
    def apply_Ymovement(self):
        # Apply affecting vertical speed
        gravity = 0.4
        if not self.is_on_ground:
            self.velocity_y += gravity
                
        else:
            self.velocity_y = 0
            
    def move(self, player):
        
        keys = pygame.key.get_pressed()
        #move the player according to left and right
        if player.x < self.enemyRect.x:
            self.enemyRect.x -= self.speed
        if player.x > self.enemyRect.x:
            self.enemyRect.x += self.speed

        # Vertical movement (jumping)
            
        if self.is_on_ground and (self.collidingWall or self.enemyRect.y < player.y):
            self.is_on_ground = False
            self.collidingGround = False
            self.velocity_y = -15

        #do the y moving logic
        self.apply_Ymovement()

        # Move player vertically according to the velocity
        self.enemyRect.y += self.velocity_y

        
        # Check borders
        self.checkBorder()
        
        

     
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
    #moves the player randomly, making it more difficult of the player
    print("")


#main part of the game
class Game:
    #initializing all of our objects
    def __init__(self):
        self.running = True
        self.player = Player()
        self.enemy = None
        self.weather = Weather()
        #makig all the obstacles in one array,
        self.grounds = []
        self.time_counter = 0
        self.has_collided = False
        self.counter = 0
        
        #choosing the number of obstacles that fill the screen
        for i in range(int(screenX/obstacleWidth) + 2):
            
            self.grounds.append(Floor(screenX - i * obstacleWidth))
        
    def game_loop(self):
        while self.running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            screen.fill((255, 255, 255))
            
            
            if self.enemy == None:
                
                if self.counter == 300:
                    self.enemy = Enemy()
                    self.counter = 0
                else:
                    self.counter += 1
                    
            
            
            collidingPlayer = False
            collidingEnemy = False
            
            
            
            collidedGroundsPlayer = []
            collidedGroundsEnemy = []
            
            def check_collisons(mainObj, collidingObj):
                if mainObj.colliderect(collidingObj.left_wall) \
                        or mainObj.colliderect(collidingObj.top_wall) \
                        or mainObj.colliderect(collidingObj.right_wall):
                    return True
            
            for ground in self.grounds: # going through every ground
                #checking for collsions with the secondary grounds
                if check_collisons(self.player.playerRect, ground): 
                    #saving which main ground we collided with
                    collidedGroundsPlayer.append(ground)
                    collidingPlayer = True
                if not self.enemy == None:
                    if check_collisons(self.enemy.enemyRect, ground):
                        collidedGroundsEnemy.append(ground)
                        collidingEnemy = True
                #moving the main ground, which will move the secondary ones with it
                ground.move()

                #drawing all the grounds, drawing secondary isnt nessasery, but its easier for debugging
                pygame.draw.rect(screen, (0, 0, 225), ground.left_wall)
                pygame.draw.rect(screen, (0, 225, 225), ground.top_wall)
                pygame.draw.rect(screen, (225, 0, 225), ground.right_wall)
                pygame.draw.rect(screen, (0, 0, 0), ground.PositionSize) #draw the main ground before the secondary ones too see them
                
            if collidingPlayer: # if we did collide with a ground do this
                for collidedground in collidedGroundsPlayer: #for every ground that we collided with
                    self.player.collision(collidedground) #call players collision checks         
            else:# we did not collide
                self.player.is_on_ground = False
                self.player.collidingGround = False
            
            if not self.enemy == None:
                if collidingEnemy:
                    for collidedground in collidedGroundsEnemy: #for every ground that we collided with
                        self.enemy.collision(collidedground) #call enemy collision checks   
                else:# we did not collide
                    self.enemy.is_on_ground = False
                    self.enemy.collidingGround = False
                    self.enemy.collidingWall = False
            

            
            if not self.enemy == None:
                if self.player.playerRect.colliderect(self.enemy.enemyRect):
                    self.has_collided = True
                    self.enemy = None

                
            if self.has_collided and not self.time_counter == 150:
                    self.player.canMove = False
                    self.time_counter += 1
            else:
                self.has_collided = False
                self.player.canMove = True
                self.time_counter = 0
                
            #move the player
            self.player.move()
            pygame.draw.rect(screen, self.player.color, self.player.playerRect)         
            
            if not self.enemy == None: 
                self.enemy.move(self.player.playerRect)
                # Draw the player
    
                pygame.draw.rect(screen, self.enemy.color, self.enemy.enemyRect)

            pygame.display.flip()

            clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.game_loop()