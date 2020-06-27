import numpy as np
import random as r
import cv2
import math

class Circle(object):
    def __init__(self,x,y,radius,color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.growing = True
    def grow(self):
        # Increase the radius of the circle by one
        if self.growing:
            self.radius += 1
    def edges(self,height,width):
        # Return whether or not the edge of the circle hits the edge of the frame
        return (self.y + self.radius > height or self.y - self.radius < 0 or self.x + self.radius > width or self.x - self.radius < 0)

def newCircle(x,y,circles,image):
    valid = True

    for circle in circles:
        d = math.dist((x,y),(circle.x,circle.y))
        if d < circle.radius:
            valid = False
            break
    if valid:
        color = tuple(image[y][x])
        return Circle(x,y,1,(int(color[0]),int(color[1]),int(color[2])))

def draw(image):
    img = cv2.imread(image)
    height = img.shape[0]
    width = img.shape[1]
    print(img.shape)
    canvas = np.zeros((height,width,3),np.uint8)
    circles = []
    attempts = 0
    total = 10
    while True:
        canvas = np.zeros((height,width,3),np.uint8)
        count = 0
        while count < total:
            c = newCircle(r.randint(0,width-1),r.randint(0,height-1),circles,img)
            if c != None:
                circles.append(c)
                count += 1
            attempts += 1
            print(attempts)
            if attempts > 1000:
                total = 0
        for circle in circles:
            canvas = cv2.circle(canvas,(circle.x,circle.y),circle.radius,circle.color,-1)
            if circle.edges(height,width):
                circle.growing = False
            else:
                overlapping = False
                for otherC in circles:
                    d = math.dist((circle.x,circle.y),(otherC.x,otherC.y))
                    if circle != otherC:
                        if d < circle.radius + otherC.radius:
                            circle.growing = False
                            break
            circle.grow()
        cv2.imshow('Howdy',img)
        cv2.imshow(image,canvas)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Put your image in here
    draw()
