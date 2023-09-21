import pygame
import sys
import random
pygame.font.init()


class Ball():
    def __init__(self,size,speedX,speedY):
        self.r = pygame.Rect((SIZE-size)/2,(SIZE-size)/2,size,size)
        self.speedX = speedX
        self.speedY = speedY

BLACK = (0,0,0)
WHITE = (255,255,255)

SIZE = 1000
WIN = pygame.display.set_mode((SIZE,SIZE))
pygame.display.set_caption("Pong")
FONT = pygame.font.SysFont("None",40)


SPEED = 5
players = [pygame.Rect(20,SIZE/2-100,20,200),pygame.Rect(SIZE-30,SIZE/2-100,20,200)]
points = [0,0]
walls = [pygame.Rect(0,-1,SIZE,1),pygame.Rect(0,SIZE,SIZE,1)]


def draw_window(ball):
    WIN.fill(BLACK)

    pygame.draw.rect(WIN,WHITE,players[0])
    pygame.draw.rect(WIN,WHITE,players[1])
    pygame.draw.rect(WIN,WHITE,ball.r)
    PNT = [FONT.render(str(points[0]),1,WHITE), FONT.render(str(points[1]),1,WHITE)]
    WIN.blit(PNT[0],((SIZE/2-PNT[0].get_width()-20,20)))
    WIN.blit(PNT[1],((SIZE/2+20,20)))
    pygame.draw.line(WIN, WHITE, [SIZE/2, 0], [SIZE/2, SIZE], 5)
    pygame.display.update() 

def movement(ball,keys_pressed):
        ball.r.x += ball.speedX
        ball.r.y += ball.speedY
        if abs(ball.speedY) <= 0.5:
            ball.speedY = random.uniform(-2*SPEED/3,2*SPEED/3)


        if keys_pressed[pygame.K_w] and players[0].y > 0:
            players[0].y -= SPEED
        if keys_pressed[pygame.K_s] and players[0].y < SIZE - players[0].height:
            players[0].y += SPEED
        if keys_pressed[pygame.K_UP] and players[1].y > 0:
            players[1].y -= SPEED
        if keys_pressed[pygame.K_DOWN] and players[1].y < SIZE - players[1].height:
            players[1].y += SPEED
       
def check_bounce(ball,keys_pressed):
    for wall in walls:
        if ball.r.colliderect(wall):
            ball.speedY *= -1

    for player in players:
        if ball.r.colliderect(player):
            if ball.r.x<SIZE/2:
                ball.r.x = player.x+player.width
                if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_s]:
                    ball.speedY = ball.speedY*(0.5+((player.y+player.height/2)-(ball.r.y+ball.r.height/2))/player.height/2)
            else:
                ball.r.x=player.x-ball.r.width
                if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_DOWN]:
                    ball.speedY = ball.speedY*(0.5+((player.y+player.height/2)-(ball.r.y+ball.r.height/2))/player.height/2)
            ball.speedX *= -1


def gameLoop(clock,ball):
    while True:
        clock.tick(144)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys_pressed = pygame.key.get_pressed()
        movement(ball,keys_pressed)
        draw_window(ball)
        check_bounce(ball,keys_pressed)
        
        if ball.r.x > SIZE:
            points[0] += 1
            break
        elif ball.r.x < -ball.r.width:
            points[1] += 1
            break

def main():
    turn = 1
    clock = pygame.time.Clock()
    while(points[0]<10 and points[1]<10):
        players[0].x = 20
        players[0].y = SIZE/2-40
        players[1].x = SIZE-30
        players[1].y = SIZE/2-40
        ball = Ball(20,2*SPEED/3 if turn%2 else -2*SPEED/3,random.uniform(-2*SPEED/3,2*SPEED/3))
        gameLoop(clock,ball)    
        del ball
        turn += 1


main()