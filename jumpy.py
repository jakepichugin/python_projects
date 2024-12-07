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
        self.playerPositionSize = pygame.Rect(400, 300, 50, 50)
        self.speed = 5
        self.velocity_y = 0
        self.goingUp = False
        self.is_on_ground = False
        self.color = GREEN

    def checkBorder(self):
        # Prevent the player from going out of bounds
        if self.playerPositionSize.x > screenX - self.playerPositionSize.width:
            self.playerPositionSize.x = screenX - self.playerPositionSize.width
        elif self.playerPositionSize.x < 0:
            self.playerPositionSize.x = 0

        if self.playerPositionSize.y > screenY - self.playerPositionSize.height:
            self.playerPositionSize.y = screenY - self.playerPositionSize.height
            self.velocity_y = 0
            self.is_on_ground = True
        elif self.playerPositionSize.y < 0:
            self.playerPositionSize.y = 0


    
    def apply_gravity(self):
        # Apply gravity, affecting vertical speed
        gravity = 0.4
        if not self.is_on_ground:
            self.velocity_y += gravity
                
        else:
            self.velocity_y = 0

    def move(self):
        
        
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.playerPositionSize.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.playerPositionSize.x += self.speed

        # Vertical movement (jumping)

            
        if keys[pygame.K_UP] and self.is_on_ground:
            self.is_on_ground = False
            self.velocity_y = -15
            print("statement was true")

        if not self.is_on_ground: 
            self.apply_gravity()

        # Move player vertically according to the velocity
        self.playerPositionSize.y += self.velocity_y

        
        # Check borders
        self.checkBorder()

obstacleWidth = 50

class Obstacle():

    def __init__(self, Xposition):
        self.PositionSize = pygame.Rect(Xposition, screenY - self.choose_height() * 50, obstacleWidth, 200)
        self.speed = 5
        
    def choose_height(self):
        return random.randint(1, 4)
        
    def move(self):

        self.PositionSize.x -= self.speed



        if self.PositionSize.x + self.PositionSize.width < 0:
            self.PositionSize.y = screenY - self.choose_height() * 50
            self.PositionSize.x = screenX  
            


class Game:
    def __init__(self):
        self.running = True
        self.player = Player()
        
        self.grounds = []
        for i in range(int(screenX/obstacleWidth) + 2):
            
            self.grounds.append(Obstacle(screenX - i * obstacleWidth))

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            screen.fill((255, 255, 255))

            
            # Move and draw each ground piece
            # experiment for when hit boxes work 
            # self.ground.PositionSize.y = screenY - self.ground.choose_height() * 50
            colliding = False
            
            collidedGround = None
            
            for ground in self.grounds:
                if self.player.playerPositionSize.colliderect(ground.PositionSize):
                    print("Colliding")
                    collidedGround = ground
                    colliding = True
                    
                    # self.player.playerPositionSize.y = self.player.playerPositionSize.y 
                ground.move()
                pygame.draw.rect(screen, (0, 0, 0), ground.PositionSize)
                
            if colliding:
                self.player.color = RED
                self.player.playerPositionSize.x -= collidedGround.speed
                # self.player.playerPositionSize.y = 
            else:
                self.player.color = GREEN
            # Draw the player
            self.player.move()
            pygame.draw.rect(screen, self.player.color, self.player.playerPositionSize)

            pygame.display.flip()

            clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.game_loop()