import pygame
import random
import math

class vec:
    def __init__(self, *args):
        self.array = [arg for arg in args]
        self.x = 0
        self.y = 0
        self.z = 0
        self.setxyz()
    def setxyz(self):
        try: self.x = self.array[0]
        except IndexError: self.x = 0
        try: self.y = self.array[1]
        except IndexError: self.y= 0
        try: self.z = self.array[2]
        except IndexError: self.z = 0
    def __str__(self):
        string = 'Vector: ('
        for i in range(len(self.array)-1):
            string += str(self.array[i])
            string += ','
        string += str(self.array[-1])+')'
        return string
    def __neg__(self):
        self.array = [-coord for coord in self.array]
        self.setxyz()
    def __add__(self, other):
        newarray = [self.array[i]+other.array[i] for i in range(len(self.array))]
        return vec(*newarray)
    def __iadd__(self, other):
        self.array = [self.array[i]+other.array[i] for i in range(len(self.array))]
        self.setxyz()
    def __sub__(self, other):
        newarray = [self.array[i]-other.array[i] for i in range(len(self.array))]
        return vec(*newarray)
    def __isub__(self, other):
        self.array = [self.array[i]-other.array[i] for i in range(len(self.array))]
        self.setxyz()
    def __mul__(self, other):
        if type(self) == type(other):
            return sum([self.array[i]*other.array[i] for i in range(len(self.array))])
        else:
            newarray = [self.array[i]*other for i in range(len(self.array))]
            return vec(*newarray)
    def __rmul__(self, other):
        if type(self) == type(other):
            return sum([self.array[i]*other.array[i] for i in range(len(self.array))])
        else:
            newarray = [self.array[i]*other for i in range(len(self.array))]
            return vec(*newarray)
    def __xor__(self, other):
        if len(self.array) == 3 and len(other.array) == 3:
            newarray = [self.array[1]*other.array[2] - self.array[2]*other.array[1],
                        self.array[2]*other.array[0] - self.array[0]*other.array[2],
                        self.array[0]*other.array[1] - self.array[1]*other.array[0]]
            return vec(*newarray)
    def __truediv__(self, other):
        newarray = [self.array[i]/other for i in range(len(self.array))]
        return vec(*newarray)
    def __len__(self):
        return len(self.array)
    def __abs__(self):
        return math.sqrt(sum([value**2 for value in self.array]))
    def __getitem__(self, i):
        return self.array[i]
    def __setitem__(self, i, value):
        self.array[i] = value
    def dist(self, other):
        return abs(self-other)
    def angle(self):
        return math.atan2(self.array[1], self.array[0])
    def normalize(self):
        return self/abs(self)


class Boid:
    def __init__(self, pos, heading):
        self.heading = heading
        self.acc = vec(0,0,0)
        self.vel = 3*vec(math.cos(heading), math.sin(heading),0)
        self.pos = pos
        self.sight = 30
    def alignment(self, flock):
        runningtotal = 0
        for boid in flock:
            if self.pos.dist(boid.pos) < self.sight:
                angle = math.atan2(boid.pos.y-self.pos.y, boid.pos.x-self.pos.x)
                runningtotal += angle-self.heading
        return runningtotal/len(boids)
    def seperation(self, flock):
        runningtotal = vec(0,0,0)
        for boid in flock:
            if self.pos.dist(boid.pos) < self.sight:
                runningtotal += -1*self.pos.dist(boid.pos)**2*(self.pos-boid.pos).normalize()
        return runningtotal/len(boids)
    def cohesion(self, flock):
        runningtotal = vec(0,0,0)
        for boid in flock:
            if self.pos.dist(boid.pos) < self.sight:
                runningtotal += (boid.pos-self.pos)
        return runningtotal/len(boids)
    def flee(self, predators):
        runningtotal = vec(0,0,0)
        for predator in predators:
            if self.pos.dist(predator.pos) < self.sight:
                runningtotal += (self.pos-predator.pos)
        return runningtotal/len(predators)
    def attack(self, preys):
        minimum = preys[0]
        minimumdist = 10000000
        for prey in preys:
            if self.pos.dist(prey.pos) < minimumdist:
                minimum = prey
        return math.atan2(minimum.pos.y-self.pos.y, minimum.pos.x-self.pos.x)-self.heading
    def update(self, flock, predators, preys):
        self.heading += 1.0*self.alignment(flock)
        self.heading += 1.0*self.attack(preys)
        self.acc += 1.0*self.seperation(flock)
        self.acc += 1.0*self.cohesion(flock)
        self.acc += 1.0*self.flee(predators)
        self.vel += 1.0*self.acc
        self.pos += self.vel
        self.acc = vec(0,0,0)

class Boid2:
    def __init__(self, heading, pos):
        self.heading = heading
        self.acc = vec(0,0,0)
        self.vel = vec(5*math.cos(heading), 5*math.sin(heading), 0)
        self.pos = pos
        self.max_speed = 3
    def within_sight(self, boid, radius):
        if self.pos.dist(boid.pos) < radius:
            return True
        return False
        # angle = self.heading+math.pi-(self.pos-boid.pos).angle()
    def alignment(self, boids):
        average_heading = 0
        for boid in boids:
            if self.within_sight(boid, 100):
                average_heading += boid.heading
        self.heading = average_heading/len(boids)
    def cohesion(self, boids):
        average_position = vec(0,0,0)
        average_velocity = vec(0,0,0)
        for boid in boids:
            if self.within_sight(boid, 70):
                average_position = average_position+boid.pos-self.pos
                average_velocity = average_velocity+boid.vel-self.vel
        self.acc = self.acc+(average_position/len(boids))/20
        self.acc = self.acc+(average_velocity/len(boids))/5
    def seperation(self, boids):
        average_position = vec(0,0,0)
        for boid in boids:
            if self.within_sight(boid, 10):
                average_position = average_position+self.pos-boid.pos
        self.acc = self.acc+(average_position/len(boids))/2
    def scatter(self, boids, predator):
        average_position = vec(0,0,0)
        for boid in boids:
            if self.within_sight(boid, 100) and abs(self.pos-predator.pos) < 20:
                average_position = average_position+self.pos-boid.pos
        # self.acc = self.acc+(average_position/len(boids))/50
        if abs(self.pos-predator.pos) < 30:
            self.acc = self.acc+(self.pos-predator.pos)/5
    def attractor(self, pos=vec(200,200,0), k=1):
        self.acc = self.acc+(pos-self.pos)/100*k
    def bounding_box(self):
        if self.pos[0] < 0: self.pos[0] = 400
        if self.pos[1] < 0: self.pos[1] = 400
        # if self.pos.z < 10: self.vel.z = 5
        if self.pos[0] > 400: self.pos[0] = 0
        if self.pos[1] > 400: self.pos[1] = 0
        # if self.pos.z > 390: self.vel.z = -5
    def update(self, boids, predators):
        self.alignment(boids)
        self.cohesion(boids)
        self.seperation(boids)
        self.attractor(pos=vec(200,200,0), k=0.5)
        # self.attractor(pos=vec(150,150,0), k=2)
        # self.attractor(pos=vec(250,150,0), k=-1)
        # self.attractor(pos=vec(150,250,0), k=-1)
        # self.attractor(pos=vec(250,250,0), k=2)
        for predator in predators: self.scatter(boids, predator)
        self.vel = self.vel+self.acc
        self.bounding_box()
        if abs(self.vel) > self.max_speed: self.vel = self.max_speed*self.vel/abs(self.vel)
        self.pos = self.pos+self.vel
        self.acc = vec(0,0,0)
    def draw(self, screen):
        pygame.draw.circle(screen, (200,200,200), (int(self.pos[0]), int(400-self.pos[1])), 2)
        
class Predator:
    def __init__(self, heading, pos):
        self.heading = heading
        self.acc = vec(0,0,0)
        self.vel = vec(7*math.cos(heading), 7*math.sin(heading), 0)
        self.pos = pos

        self.max_speed = 4
    def bounding_box(self):
        if self.pos[0] < 0: self.pos[0] = 400
        if self.pos[1] < 0: self.pos[1] = 400
        # if self.pos.z < 10: self.vel.z = 5
        if self.pos[0] > 400: self.pos[0] = 0
        if self.pos[1] > 400: self.pos[1] = 0
        # if self.pos.z > 390: self.vel.z = -5
    def seperate(self, predators):
        average_position = vec(0,0,0)
        for predator in predators:
            if abs(self.pos-predator.pos) < 20:
                average_position = average_position+self.pos-predator.pos
        self.acc = self.acc+(average_position/len(predators))/3
    def cohesion(self, boids):
        average_position = vec(0,0,0)
        for boid in boids:
            if abs(self.pos-boid.pos) < 100:
                average_position = average_position+boid.pos-self.pos
        self.acc = self.acc+(average_position/len(boids))/50
    def update(self, boids, predators):
        distance = 1000
        closest = None
        for boid in boids:
            if abs(self.pos-boid.pos) < distance:
                distance = abs(self.pos-boid.pos)
                closest = boid
        self.heading = math.atan2(closest.pos[1]-self.pos[1], closest.pos[0]-self.pos[0])
        self.acc = 3*vec(math.cos(self.heading), math.sin(self.heading), 0)
        self.seperate(predators)
        self.cohesion(boids)
        self.vel = self.vel+self.acc
        # self.vel = vec(7*math.cos(self.heading), 7*math.sin(self.heading), 0)
        if abs(self.vel) > self.max_speed: self.vel = self.max_speed*self.vel/abs(self.vel)
        self.pos = self.pos+self.vel
        self.acc = vec(0,0,0)

        self.bounding_box()
    def draw(self, screen):
        pygame.draw.circle(screen, (255,0,0), (int(self.pos[0]), int(400-self.pos[1])), 2)

        
'''
class Flock:
    def __init__(self, boids):
        self.boids = boids
    def update(self, predators=[], preys=[]):
        for i in range(len(self.boids)):
            flock = self.boids[0:i]+self.boids[i+1:-1]
            self.boids[i].update(flock, predators, preys)
'''

class Bullet:
    def __init__(self, pos, heading):
        self.heading = heading
        self.vel = vec(10*math.cos(heading), 10*math.sin(heading), 0)
        self.pos = pos
    def update(self):
        self.pos = self.pos+self.vel
    def draw(self, screen):
        pygame.draw.circle(screen, (0,255,0), (int(self.pos[0]), int(400-self.pos[1])), 1)

class Turret:
    def __init__(self, pos, heading, d):
        self.pos = pos
        self.heading = heading
        self.range = d
        self.charging = random.randint(0,19)
    def aim_at_whole(self, flock):
        average_position = vec(0,0,0)
        count = 0
        for boid in flock:
            if abs(self.pos-boid.pos) < self.range:
                average_position = average_position+boid.pos
                count += 1
        if count == 0: self.heading = math.pi
        else:
            average_position = average_position/count
            self.heading = math.atan2(average_position[1]-self.pos[1], average_position[0]-self.pos[0])
    def aim_at_closest(self, flock):
        closest_distance = 1000
        closest_boid = None
        for boid in flock:
            distance = abs(self.pos-boid.pos)
            if distance < closest_distance and distance < self.range:
                closest_boid = boid
        if closest_boid == None:
            self.heading = math.pi
        else:
            self.heading = math.atan2(closest_boid.pos[1]-self.pos[1], closest_boid.pos[0]-self.pos[0])
    def update(self, flock):
        self.charging += 1
        if self.charging >= 10:
            self.charging = 0
        self.aim_at_closest(flock)
    def draw(self, screen):
        p1 = (int(20*math.cos(160*math.pi/180+self.heading)+self.pos[0]), int(400-20*math.sin(160*math.pi/180+self.heading)+self.pos[1]))
        p2 = (int(20*math.cos(200*math.pi/180+self.heading)+self.pos[0]), int(400-20*math.sin(200*math.pi/180+self.heading)+self.pos[1]))
        p3 = (int(20*math.cos(340*math.pi/180+self.heading)+self.pos[0]), int(400-20*math.sin(340*math.pi/180+self.heading)+self.pos[1]))
        p4 = (int(20*math.cos(380*math.pi/180+self.heading)+self.pos[0]), int(400-20*math.sin(380*math.pi/180+self.heading)+self.pos[1]))
        pygame.draw.polygon(screen, (200,200,200), [p1, p2, p3, p4])
        
           
pygame.init()
screen = pygame.display.set_mode((400,400))
screen.fill((255,255,255))
clock = pygame.time.Clock()

boids = []
for i in range(10):
    b = Boid2(random.random()*math.pi*2, vec(random.randint(0,400), random.randint(0,400), 0))
    boids.append(b)
predators = []
for i in range(10):
    p = Predator(random.random()*math.pi*2, vec(random.randint(0,400), random.randint(0,400), 0))
    predators.append(p)
turrets = [Turret(vec(0,0,0), 0, 600),
           # Turret(vec(0,400,0), 0, 300),
           Turret(vec(400,0,0), 0, 600)]
           # Turret(vec(400,400,0), 0, 300)
bullets = []

done = False
while not done:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            done = True
    screen.fill((0,0,0))

    dead_boids = []
    dead_bullets = []
    for turret in turrets:
        turret.update(boids)
        turret.draw(screen)
        if turret.charging == 0:
            b = Bullet(turret.pos, turret.heading)
            bullets.append(b)
    for bullet in bullets:
        bullet.update()
        bullet.draw(screen)
        if bullet.pos[0] >= 400 or bullet.pos[0] <= 0 or bullet.pos[1] >= 400 or bullet.pos[1] <= 0:
            dead_bullets.append(bullet)
    for predator in range(len(predators)):
        other_predators = predators[0:predator]+predators[predator+1:-1]
        predators[predator].update(boids, other_predators)
        predators[predator].draw(screen)
    for boid in range(len(boids)):
        other_boids = boids[0:boid]+boids[boid+1:-1]
        boids[boid].update(other_boids, bullets+predators)
        boids[boid].draw(screen)
        for predator in predators:
            if abs(predator.pos-boids[boid].pos) < 4:
                dead_boids.append(boids[boid])
        for bullet in bullets:
            if abs(bullet.pos-boids[boid].pos) < 10:
                dead_boids.append(boids[boid])
                dead_bullets.append(bullet)
                pygame.draw.circle(screen, (255,127,0), (int(bullet.pos[0]), int(400-bullet.pos[1])), 10)
    for boid in list(set(dead_boids)):
        boids.remove(boid)
        b = Boid2(random.random()*math.pi*2, vec(random.randint(0,400), random.randint(0,400), 0))
        boids.append(b)
    for bullet in list(set(dead_bullets)):
        bullets.remove(bullet)

    pygame.display.update()
    clock.tick(60)
        







'''
flock = []
for i in range(25):
    b = Boid2(random.random()*math.pi*2, vec(random.randint(0,400), random.randint(0,400), 0))
    flock.append(b)
ps = []
for i in range(3):
    p = Predator(random.random()*math.pi*2, vec(random.randint(0,400), random.randint(0,400), 0))
    ps.append(p)
bullets = []
bullet_timer = 0
done = False

while not done:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            done = True
    screen.fill((0,0,0))
    # pygame.draw.circle(screen, (255,0,0), (150,150), 3)
    # pygame.draw.circle(screen, (255,0,0), (250,250), 3)
    # pygame.draw.circle(screen, (0,0,255), (150,250), 3)
    # pygame.draw.circle(screen, (0,0,255), (250,150), 3)
    bullet_timer += 1
    if bullet_timer > 20:
        bullet_timer = 0
        boid_com = vec(0,0,0)
        for boid in flock:
            # if abs(boid.pos) < 400:
            boid_com = boid_com+(boid.pos)/len(flock)
        b1 = Bullet(vec(0,0,0), math.atan2(boid_com[1], boid_com[0]))
        b2 = Bullet(vec(400,0,0), math.atan2(boid_com[1], boid_com[0]-400))
        b3 = Bullet(vec(0,400,0), math.atan2(boid_com[1]-400, boid_com[0]))
        b4 = Bullet(vec(400,400,0), math.atan2(boid_com[1]-400, boid_com[0]-400))
        bullets = bullets+[b1, b2, b3, b4]
    for b in bullets:
        if b.pos[0] > 400 or b.pos[1] > 400 or b.pos[0] < 0 or b.pos[1] < 0:
            bullets.remove(b)

    
    # pygame.draw.circle(screen, (255,0,0), (200,200), 3)
    dead = []
    dead2 = []
    for i in range(len(flock)):
        newflock = flock[0:i]+flock[i+1:-1]
        flock[i].update(newflock, predators=bullets)
        pygame.draw.circle(screen, (200,200,200), (int(flock[i].pos[0]), int(400-flock[i].pos[1])), 1)
        for p in ps:
            if abs(flock[i].pos-p.pos) < 4:
                dead.append(flock[i])
        for b in bullets:
            if abs(flock[i].pos-b.pos) < 17:
                dead.append(flock[i])
                dead2.append(b)
    dead = list(set(dead))
    dead2 = list(set(dead2))
    for b in dead:
        flock.remove(b)
        flock.append(Boid2(random.random()*math.pi*2, vec(random.randint(0,400), random.randint(0,400), 0)))
    for b in dead2:
        pygame.draw.circle(screen, (255,128,0), (int(b.pos[0]), int(400-b.pos[1])), 9)
        bullets.remove(b)
    for i in range(len(ps)):
        newps = ps[0:i]+ps[i+1:-1]
        ps[i].update(flock, newps)
        pygame.draw.circle(screen, (255,0,0), (int(ps[i].pos[0]), int(400-ps[i].pos[1])), 2)
    for b in bullets:
        b.update()
        pygame.draw.circle(screen, (0,255,0), (int(b.pos[0]), int(400-b.pos[1])), 1)
    pygame.display.update()
    pygame.display.flip()
    clock.tick(60)

Two sides: E and R

R boids:
RX: speed = 4; rate = 3; damage = 3
RY: speed = 3; rate = 4; damage = 2
RA: speed = 6; rate = 6; damage = 1
RB: speed = 3; rate = 2; damage = 4
Squadrons are 12 boids: Red RX, Blue RX, Gold RY, Green RA, Gray RB, Black RY
'''
