# PID controller
import pygame
import random
import math

dt = 1
integral = 0
lasterror = 0
setpoint = 100
value = 400

points = []

def function(t):
    # return 100+30*math.sin((t/10))
    return 100+(50*(t/100)+(t/100)**2-1.5*(t/100)**3)/10

for t in range(0,1000,dt):
    setpoint = function(t)
    # print('time: '+str(t))
    error = setpoint-value
    # print('error: '+str(error))
    derivative = (error-lasterror)/dt
    # print('derivative: '+str(derivative))
    integral += (error*dt)
    # print('integral: '+str(integral))
    value += (0.1*error)+(0.001*integral)+(0.05*derivative)+3*(0.5-random.uniform(0,1))
    points.append(int(value))

pygame.init()
screen = pygame.display.set_mode((1000,400))
screen.fill((255,255,255))

# pygame.draw.line(screen, (0,0,255), (0,100), (400,100), 2)

for t in range(1,len(points)):
    p1 = (t*dt,function(t*dt))
    p2 = ((t-1)*dt,function((t-1)*dt))
    pygame.draw.line(screen, (0,0,255), p1, p2, 2)

for t in range(1,len(points)):
    p1 = (t*dt,points[t])
    p2 = ((t-1)*dt,points[t-1])
    pygame.draw.line(screen, (255,0,0), p1, p2, 2)

pygame.display.update()
