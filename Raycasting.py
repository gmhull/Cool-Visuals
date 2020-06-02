import numpy as np
import pygame, sys, math

class Ray(object):
    def __init__(self,pos,angle):
        self.pos = np.array([pos[0],pos[1]])
        self.angle = angle
        self.newAngle = 0
        self.dir = np.array([math.sin(self.angle),math.cos(self.angle)])
    def show(self,surface,end):
        # Perhaps self.pos should be turned into an int
        pygame.draw.line(surface,(0,255,255),(int(self.pos[0]),int(self.pos[1])),end,1)
    def updateAngle(self,angle):
        self.newAngle = self.angle + angle
        self.dir = np.array([math.sin(self.newAngle),math.cos(self.newAngle)])
    def cast(self,wall):
        x1 = wall.a[0]
        y1 = wall.a[1]
        x2 = wall.b[0]
        y2 = wall.b[1]
        x3 = self.pos[0]
        y3 = self.pos[1]
        x4 = self.pos[0] + self.dir[0]
        y4 = self.pos[1] + self.dir[1]

        den = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)

        if den == 0:
            return

        t =  ((x1 - x3)*(y3 - y4) - (y1 - y3)*(x3 - x4)) / den
        u = -((x1 - x2)*(y1 - y3) - (y1 - y2)*(x1 - x3)) / den

        if t > 0 and t < 1 and u > 0:
            pt = [0,0]
            pt[0] = int(x1 + t * (x2 - x1))
            pt[1] = int(y1 + t * (y2 - y1))
            return pt
        else:
            return

class Boundary(object):
    def __init__(self,x1,y1,x2,y2):
        self.a = (x1,y1)
        self.b = (x2,y2)
    def show(self,surface):
        pygame.draw.line(surface,255,self.a,self.b,1)

class Particle(object):
    def __init__(self,width,height):
        self.fov = 50
        self.pos = [width/2,height/2]
        self.rays = []
        self.angle = 0
        for i in range(int(-self.fov/2),int(self.fov/2),1):
            self.rays.append(Ray(self.pos,math.radians(i)))
    def update(self):
        for ray in self.rays:
            ray.pos = self.pos
    def look(self,surface,walls):
        scene = []
        for ray in self.rays:
            closest = None
            max = math.inf
            for wall in walls:
                pt = ray.cast(wall)
                if pt:
                    dist = math.dist((self.pos),(pt))
                    # Should be able to fix the fishbowl with something here
                    # a = ray.newAngle - self.angle
                    # dist *= math.cos(a)
                    if dist < max:
                        max = dist
                        closest = pt
            if closest:
                ray.show(surface,closest)
                pygame.draw.circle(surface,(255,0,255),closest,2)
            scene.append(max)
        return scene
    def rotate(self,changeAmt):
        self.angle += changeAmt
        for ray in self.rays:
            ray.updateAngle(math.radians(self.angle))
    def move(self, moveSpeed):
        self.dir = moveSpeed * np.array([math.sin(math.radians(self.angle)),math.cos(math.radians(self.angle))])
        self.pos += self.dir

def run():
    pygame.init()
    size = width, height = 500, 700
    screen = pygame.display.set_mode((2*width,height))
    walls = []
    # The edges of the screen
    walls.append(Boundary(0,0,width,0))
    walls.append(Boundary(0,0,0,height))
    walls.append(Boundary(0,height,width,height))
    walls.append(Boundary(width,0,width,height))
    for i in range(5):
        walls.append(Boundary(np.random.randint(0,width),np.random.randint(0,height),
                    np.random.randint(0,width),np.random.randint(0,height)))
    particle = Particle(width,height)
    rotator = 0
    moveSpeed = 0
    while True:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_a:
                    rotator = 1
                elif event.key == pygame.K_d:
                    rotator = -1
                elif event.key == pygame.K_w:
                    moveSpeed = 1
                elif event.key == pygame.K_s:
                    moveSpeed = -1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    rotator = 0
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    moveSpeed = 0
        particle.rotate(rotator)
        particle.move(moveSpeed)

        mouseX, mouseY = pygame.mouse.get_pos()
        screen.fill(0)
        for wall in walls:
            wall.show(screen)
        particle.update()

        scene = particle.look(screen,walls)
        w = int(width / len(scene))
        for i in range(len(scene)):
            color = 255 - scene[i]**2 / width**2 * 255
            if color < 0:
                color = 0
            h = int(height - (scene[i] / width * height))
            rect = pygame.Rect(width*2-i*w,0,w+1,h)
            rect.centery = int(height/2)
            pygame.draw.rect(screen,(color,color,color),rect)

        pygame.display.flip()

if __name__ == "__main__":
    run()
