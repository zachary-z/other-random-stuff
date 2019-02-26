# Remember that air hockey game from last year?
# Well, I made a better version of it
# It has a better AI and more accurate physics
# Use the mouse to play air hockey
# If the mouse is moved too fast, it won't register collisions


from Vector import *
import pygame
import time

class puck:
    def __init__(self, pos):
        self.pos = pos
        self.vel = vec(0,0,0)
        self.acc = vec(0,0,0)

        self.radius = 20
        self.mass = 400
    def update(self, paddle):
        self.acc = vec(0,0,0)
        size = [500,800]
        # Check for a collision between paddle and puck
        d = self.pos-paddle.pos
        v = self.vel-paddle.vel
        r = self.radius+paddle.radius
        if abs(d) < r and v*d.normalize() < 0:
                # Calculate and apply force
                J = -1*v*d.normalize()*1.6/(1/self.mass+1/paddle.mass)
                F = d.normalize()*J
                self.pos = paddle.pos+d.normalize()*r
                self.acc = self.acc+F/self.mass
        if abs(self.vel) < 0.2: self.vel = vec(0,0,0)
        self.acc = self.acc-0.2*self.vel.normalize()
        self.vel = self.vel+self.acc
        self.pos = self.pos+self.vel
        # Bounce off of the edges of the table
        if self.pos[0] < self.radius:
            self.pos[0] = self.radius
            self.vel[0] = -0.9*self.vel[0]
        if self.pos[1] < self.radius:
            self.pos[1] = self.radius
            self.vel[1] = -0.9*self.vel[1]
        if self.pos[0] > 500-self.radius:
            self.pos[0] = 500-self.radius
            self.vel[0] = -0.9*self.vel[0]
        if self.pos[1] > 800-self.radius:
            self.pos[1] = 800-self.radius
            self.vel[1] = -0.9*self.vel[1]
    def draw(self, screen):
        pygame.draw.circle(screen,(0,0,0),(int(self.pos[0]),int(800-self.pos[1])),self.radius)

class paddle:
    def __init__(self, pos):
        self.pos = pos
        self.vel = vec(0,0,0)
        self.radius = 40
        self.mass = 400
    def update(self, pos):
        self.vel = pos-self.pos
        self.pos = pos
    def draw(self, screen):
        pygame.draw.circle(screen,(180,0,0),(int(self.pos[0]),int(800-self.pos[1])),self.radius)


pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((500,800))
screen.fill((255,255,255))
clock = pygame.time.Clock()

comicsans = pygame.font.SysFont('Comic Sans MS', 30)

player = paddle(vec(250,0,0))
ai = paddle(vec(250,800,0))
puck = puck(vec(250,400,0))

player_score = 0
ai_score = 0

while True:
    for event in pygame.event.get():
        if event == pygame.QUIT: break
    screen.fill((255,255,255))
    pygame.draw.line(screen, (255,0,0), (0,400), (500,400), 7)
    pygame.draw.line(screen, (180,60,0), (175,0), (325,0), 20)
    pygame.draw.line(screen, (180,60,0), (175,800), (325,800), 40)
    
    mouse = vec(pygame.mouse.get_pos()[0], min(800-pygame.mouse.get_pos()[1],400),0)
    player.update(mouse)
    player.draw(screen)

    defense = ai.pos+7*((vec(250,800,0)+150*(puck.pos-vec(250,800,0)).normalize())-ai.pos).normalize()
    if abs(defense-(vec(250,800,0)+150*(puck.pos-vec(250,800,0)).normalize())) < 10:
        defense = vec(250,800,0)+150*(puck.pos-vec(250,800,0)).normalize()
    offense = ai.pos+15*(puck.pos-ai.pos).normalize()
    if puck.pos[1] > 400:
        ai.update(offense)
    else:
        ai.update(defense)
    ai.draw(screen)
    
    if puck.pos[1] > 400:
        puck.update(ai)
    else:
        puck.update(player)
    puck.draw(screen)

    if abs(puck.pos-vec(250,0,0)) < 75 and puck.pos[1] < 40:
        puck.pos = vec(250,400,0)
        puck.vel = vec(0,0,0)
        ai_score += 1
        time.sleep(1)
    if abs(puck.pos-vec(250,800,0)) < 75 and puck.pos[1] > 760:
        puck.pos = vec(250,400,0)
        puck.vel = vec(0,0,0)
        player_score += 1
        time.sleep(1)
    score_display = comicsans.render('Home: '+str(player_score)+'| Away: '+str(ai_score), False, (0,0,0))
    screen.blit(score_display, (0,0))

    pygame.display.update()
    clock.tick(120)
    
    
        
        
                
