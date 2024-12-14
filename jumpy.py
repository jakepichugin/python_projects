import pygame
import time
import random

pygame.init()

screenX = 1200
screenY = 800
screen = pygame.display.set_mode((screenX, screenY))
clock = pygame.time.Clock()
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
class Player:
    
    def __init__(self):
        self.playerRect = pygame.Rect(400, 100, 50, 50)
        self.speed = 5
        self.velocity_y = 0
        self.is_on_ground = False
        self.color = GREEN
        self.collidingGround = False
        # -1 means going left, 1 going right, 0 still
        self.dirX = 0

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

    def collision(self, collidedObj):
        # Wall collision (left side)
        # Floor collision
        if self.velocity_y > 10:
            if self.playerRect.colliderect(collidedObj.top_wall):
                self.playerRect.bottom = collidedObj.top_wall.top + 1
                self.is_on_ground = True
                print("Floor Detected")
            
            elif self.playerRect.colliderect(collidedObj.left_wall):
                self.playerRect.right = collidedObj.left_wall.left
            elif self.playerRect.colliderect(collidedObj.right_wall):
                self.playerRect.left = collidedObj.right_wall.right
        else:
            
            if self.playerRect.colliderect(collidedObj.left_wall):
                self.playerRect.right = collidedObj.left_wall.left
            elif self.playerRect.colliderect(collidedObj.right_wall):
                self.playerRect.left = collidedObj.right_wall.right
            elif self.playerRect.colliderect(collidedObj.top_wall):
                self.playerRect.bottom = collidedObj.top_wall.top + 1
                self.is_on_ground = True
                print("Floor Detected")


    def apply_Ymovement(self):
        # Apply affecting vertical speed
        gravity = 0.4
        if not self.is_on_ground:
            self.velocity_y += gravity
                
        else:
            self.velocity_y = 0


    
    def move(self):
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.dirX = -1
            self.playerRect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.dirX = 1
            self.playerRect.x += self.speed

        # Vertical movement (jumping)

            
        if keys[pygame.K_UP] and self.is_on_ground:
            self.is_on_ground = False
            self.collidingGround = False
            self.velocity_y = -15



        self.apply_Ymovement()

        
        # Move player vertically according to the velocity
        self.playerRect.y += self.velocity_y

        
        # Check borders
        self.checkBorder()
        

obstacleWidth = 70

class Obstacle():

    def __init__(self, Xposition):
        self.PositionSize = pygame.Rect(Xposition, screenY - self.choose_height() * 50, obstacleWidth, 200)
        self.speed = 10
        self.left_wall = pygame.Rect(self.PositionSize.left, self.PositionSize.y + 10, 10, 200)
        self.top_wall = pygame.Rect(self.PositionSize.left + 5, self.PositionSize.y, obstacleWidth - 10, 10)
        self.right_wall = pygame.Rect(self.PositionSize.right - 10, self.PositionSize.y + 10, 10, 200)
        
        
    def choose_height(self):
        return random.randint(1, 4)
            
    
    def move(self):

        self.PositionSize.x -= self.speed
        self.left_wall.x = self.PositionSize.left
        self.top_wall.x = self.PositionSize.x + 5
        self.right_wall.x = self.PositionSize.right - 10
        
        if self.PositionSize.x + self.PositionSize.width < 0:
            self.PositionSize.y = screenY - self.choose_height() * 50
            self.left_wall.y = self.PositionSize.y + 10
            self.top_wall.y = self.PositionSize.y
            self.right_wall.y = self.PositionSize.y + 10
            self.PositionSize.x = screenX  
            
class Weather():
    def __init__(self, ):
        self.speed = 0
    
    def displayWeather(self):
        print("sdasfdsfjd")
    



class Game:
    def __init__(self):
        self.running = True
        self.player = Player()
        self.weather = Weather()
        self.grounds = []
        for i in range(int(screenX/obstacleWidth) + 2):
            
            self.grounds.append(Obstacle(screenX - i * obstacleWidth))

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            screen.fill((255, 255, 255))
            self.weather.displayWeather()
            # if random.randint(1, 60) == 2:
            #     self.weather.speed = random.randint(-9, 9)
            
            self.player.playerRect.x += self.weather.speed
            
            
            # Move and draw each ground piece
            # experiment for when hit boxes work 
            # self.ground.PositionSize.y = screenY - self.ground.choose_height() * 50
            colliding = False
            
            collidedGrounds = []
            
            for ground in self.grounds:
                if self.player.playerRect.colliderect(ground.left_wall) \
                        or self.player.playerRect.colliderect(ground.top_wall) \
                        or self.player.playerRect.colliderect(ground.right_wall):
                    
                    collidedGrounds.append(ground)
                    colliding = True
                    
                    
                    # self.player.playerPositionSize.y = self.player.playerPositionSize.y 
                ground.move()

                pygame.draw.rect(screen, (0, 0, 225), ground.left_wall)
                pygame.draw.rect(screen, (0, 225, 225), ground.top_wall)
                pygame.draw.rect(screen, (225, 0, 225), ground.right_wall)
                pygame.draw.rect(screen, (0, 0, 0), ground.PositionSize)
                
            if colliding:
                self.player.color = GREEN
                # self.player.is_on_ground = True
                for collidedground in collidedGrounds:
                    self.player.collision(collidedground)
            else:
                self.player.is_on_ground = False
                print("falling")
                self.player.color = GREEN
                self.player.collidingGround = False
            # Draw the player
            self.player.move()
            pygame.draw.rect(screen, self.player.color, self.player.playerRect)

            pygame.display.flip()

            clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.game_loop()