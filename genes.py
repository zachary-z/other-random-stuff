# This teaches rockets to avoid a barrier and fly towards a target
# Each generation, the rockets get more accurate
# After about 20 generations, most of the rockets consistently get close
# The commented code is for evolving 'to be or not to be' from random characters

import random
import pygame
import math
from Vector import *

'''
global letters
letters = ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*():;/?,.<>\[]{}-_=+'

class DNA:
    def __init__(self):
        self.genes = [random.choice(letters) for i in range(18)]
        self.phrase = ''
        for char in self.genes:
            self.phrase += char
        self.target = 'to be or not to be'
        self.fitness = 0
    def get_fitness(self):
        score = 0
        for i in range(len(self.genes)):
            if self.genes[i] == self.target[i]:
                score += 1
        self.fitness = float(score/len(self.genes))
    def crossover(self, partner):
        child = DNA()
        for i in range(len(self.genes)):
            if random.random() > 0.5:
                child.genes[i] = self.genes[i]
            else:
                child.genes[i] = partner.genes[i]
        return child
    def mutate(self):
        for i in range(len(self.genes)):
            if random.random() > 0.99:
                self.genes[i] = random.choice(letters)
        self.phrase = ''
        for char in self.genes:
            self.phrase += char
'''

class rocketDNA:
    def __init__(self):
        self.genes = [self.random_force() for i in range(140)] #list of normalized, random vectors
        self.target = vec(200,300,0)
        self.fitness = 0
        self.stopped = False
        self.finished = False

        self.pos = vec(200,50,0)
        self.vel = vec(0,0,0)
        self.acc = vec(0,0,0)
        self.heading = math.pi/2

        self.record_distance = 500
        self.finish_time = 0
    def random_force(self):
        angle = random.random()*2*math.pi
        force = random.random()*0.4
        return vec(force*math.cos(angle), force*math.sin(angle), 0)
    def get_fitness(self):
        self.fitness = 1000000/(self.record_distance*self.finish_time)
        if self.stopped: self.fitness *= 0.1
        if self.finished: self.fitness *= 3
    def crossover(self, partner):
        child = rocketDNA()
        for i in range(len(self.genes)):
            if random.random() > 0.5:
                child.genes[i] = self.genes[i]
            else:
                child.genes[i] = partner.genes[i]
        return child
    def mutate(self):
        for i in range(len(self.genes)):
            if random.random() > 0.95:
                self.genes[i] = self.random_force()
    def update(self, step):
        self.acc = self.acc+self.genes[step]
        self.heading = math.atan2(self.vel[1], self.vel[0])
        self.vel = self.vel+self.acc
        if not self.stopped and not self.finished:
            self.pos = self.pos+self.vel
            if abs(self.pos-self.target) < 20:
                self.finished = True
            else:
                self.finish_time += 1
            self.record_distance = min(abs(self.pos-self.target), self.record_distance)
        self.acc = self.acc*0

    def draw(self, screen):
        '''
        h = self.heading
        p1 = self.pos+vec(5*math.cos(h), 5*math.sin(h), 0)
        p1 = (p1[0], 400-p1[1])
        p2 = self.pos+vec(5*math.cos(h-math.pi*4/5), 5*math.cos(h-math.pi*4/5), 0)
        p2 = (p2[0], 400-p2[1])
        p3 = self.pos+vec(5*math.cos(h+math.pi*4/5), 5*math.cos(h+math.pi*4/5), 0)
        p3 = (p3[0], 400-p3[1])
        pygame.draw.polygon(screen, (255,0,0), [p1, p2, p3], 0)
        '''
        pygame.draw.circle(screen, (255,0,0), (int(self.pos[0]), int(400-self.pos[1])), 3)

class obstacle:
    def __init__(self, location, width, height):
        self.loc = location
        self.w = width
        self.h = height
    def contains(self, rocket):
        if self.loc[0] < rocket.pos[0] and self.loc[0]+self.w > rocket.pos[0]:
            if self.loc[1] < rocket.pos[1] and self.loc[1]+self.h > rocket.pos[1]:
                rocket.stopped = True
                return True
        return False
    def draw(self, screen):
        p1 = (self.loc[0], 400-self.loc[1])
        p2 = (self.loc[0]+self.w, 400-self.loc[1])
        p3 = (self.loc[0]+self.w, 400-self.loc[1]-self.h)
        p4 = (self.loc[0], 400-self.loc[1]-self.h)
        pygame.draw.polygon(screen, (150,150,150), [p1, p2, p3, p4], 0)
        
obstacles = [obstacle(vec(150,150,0), 100, 20)]               
population = [rocketDNA() for i in range(100)]
pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((400,400))
screen.fill((255,255,255))

done = False

while not done:
    for x in range(50):
        mating_pool = []
        for i in range(len(population[0].genes)):
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    done = True
            screen.fill((255,255,255))
            for o in obstacles:
                o.draw(screen)
                for rocket in population:
                    o.contains(rocket)
            pygame.draw.circle(screen, (128,128,128), (200,100), 20)
            for rocket in population:
                rocket.update(i)
                rocket.draw(screen)
            pygame.display.update()
            clock.tick(60)

        for rocket in population:
            rocket.get_fitness()
            for j in range(max(int(rocket.fitness), 0)):
                mating_pool.append(rocket)
        # print(len(mating_pool))
        new_population = []
        for i in range(len(population)):
            a = random.choice(mating_pool)
            b = random.choice(mating_pool)
            c = a.crossover(b)
            c.mutate()
            new_population.append(c)
        population = new_population
        
      
'''
population = [DNA() for i in range(1000)]

for x in range(50):
    mating_pool = []
    for phrase in population:
        phrase.get_fitness()
        for j in range(int(100*phrase.fitness)):
            mating_pool.append(phrase)
    new_population = []
    for i in range(len(population)):
        a = random.choice(mating_pool)
        b = random.choice(mating_pool)
        c = a.crossover(b)
        c.mutate()
        new_population.append(c)
    population = new_population
    
population = sorted(population, key=lambda x: x.fitness)
for i in range(20):
    print(population[199-i].phrase)

class rocket:
    def __init__(self):
        self.pos = vec(0,0,0)
        self.vel = vec(0,0,0)
        self.acc = vec(0,0,0)

        self.dna = DNA()
        self.fitness = 0
    def apply_force(self, f):
        self.acc = self.acc + f
    def update(self, generation):
        self.acc = self.acc + self.dna.genes[generation]
        self.vel = self.vel + self.acc
        self.pos = self.pos + self.vel
        self.acc = self.acc * 0
    def determine_fitness(target):
        return 1/(abs(self.pos-target)**2)

class DNA:
    def __init__(self):
        self.genes = []
        maxforce = 0.1
        for i in range(100):
            angle = random.random()*2*math.pi
            force = vec(math.cos(angle), math.sin(angle), 0)
            self.genes.append(force*random.random()*maxforce)

class Population:
    def __init__(self):
        self.mutation_rate = 0.01
        self.population = []
        self.mating_pool = []
        self.generations = 0
    def fitness(self):
        for r in self.population:
            r.fitness = r.determine_fitness(vec(300,200))
    def selection(self):
        return None
    def reproduction(self):
        return None
    def live(self):
        for r in self.population:
            r.update(self.generations)
        

def run(rockets):
    for i in range(100):
        for r in rockets:
            r.apply_force(r.dna.genes[i])
            r.update()
'''   
