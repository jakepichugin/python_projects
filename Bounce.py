import pygame
import pgzrun
from pgzero.actor import Actor
from pgzero.keyboard import keyboard
# import math
import sys

'''
1. directly bound with size of image : rect
	size of rect for collision is computed from size of image
2. size of rect for collision is customized
3. image (transparent) - mask


4. look into pygame api to see if it support circular collision directly
5. draw circle on image - mask
6. manually: (delx**2+dely**2)**(1/2)<(r1+r2)

'''
w = pygame.key.get_pressed()
score = 0
white = (255,255,255)
def bounce():
    global x_speed
    global y_speed
    global other_speed
    global score
    moving_rect.x += x_speed
    moving_rect.y += y_speed

    #other_rect.y += other_speed
    if moving_rect.right >= screen_w:
        x_speed *= -1
    if moving_rect.bottom >= screen_h or moving_rect.top <= 0:
        y_speed *= -1
    if other_rect.bottom >= screen_h:
        other_rect.y += -7.5
    if other_rect.top <= 0:
        other_rect.y += 7.5



    if moving_rect.colliderect(other_rect):
        x_speed *= -1
        score += 1

    pygame.draw.rect(screen,(255,255,255),moving_rect)
    pygame.draw.rect(screen, (255, 255, 255), other_rect)
    pygame.draw.rect(screen, (255, 255, 255), middle)
pygame.init()
clock = pygame.time.Clock()
screen_w,screen_h = 1540,800

screen = pygame.display.set_mode((screen_w,screen_h))
moving_rect = pygame.Rect(350,350,40,40)
other_rect = pygame.Rect(20,350,30,200)
middle = pygame.Rect(500,0,10,1000)
x_speed,y_speed = 14,13
other_speed = 2




def update():
    # for event in pygame.event.get():
    #     eventDetails = None
    #     elif event.type == pygame.KEYDOWN:
    #         eventDetails = (event.type, pygame.key.name(event.key).upper())
    #     else:
    #         pass
    #         # raise Exception([event.type,"NOT HANDLED"])
    #     if eventDetails in self.registeredEventHandlers:
    #         eventHandler = self.registeredEventHandlers[eventDetails]
    #         if eventHandler is not None:
    #             eventHandler()
    #         else:
    #             pass
    #             # raise Exception([event.type,"NOT HANDLED"])
    #     else:
    #         pass
    #         # raise Exception([event.type, "NOT HANDLED"])

    global other_speed,x_speed,y_speed
    #w = pygame.key.get_pressed()

    if pygame.key.get_pressed()[pygame.K_w]:
        other_rect.y += -8
        #pygame.draw.rect(screen, (255, 0, 0), other_rect)
    elif pygame.key.get_pressed()[pygame.K_s]:
        other_rect.y += 8
        #pygame.draw.rect(screen, (255, 0, 0), other_rect)
font_name = pygame.font.match_font('arial')

def score_board(surf, text, size, x, y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface,text_rect)

def ending():
    if moving_rect.left <= 0:
        print("OOF, Try again")
        print(" ")
        print("Final score: %s" % (score))
        pygame.quit()
        sys.exit()
    elif score >= 10:
        print("You Win!")
        print(" ")
        print("Final score: %s" %(score))
        pygame.quit()
        sys.exit()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            print(score)
    screen.fill((30,30,30))
    score_board(screen, str("Score: %s"%(score)),40,1200, 10)
    update()
    bounce()
    pygame.display.flip()
    clock.tick(60)
    ending()

