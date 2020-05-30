import numpy as np
import cv2

class Star(object):
    def __init__(self,width,height):
        self.width = width - 50
        self.height = height - 50
        self.x = np.random.randint(-self.width/2,self.width/2)
        self.y = np.random.randint(-self.height/2,self.height/2)
        self.z = np.random.randint(1,100)

    def update(self):
        self.z = self.z - 1
        if self.z < 1:
            self.z = 100
            self.x = np.random.randint(-self.width/2,self.width/2)
            self.y = np.random.randint(-self.height/2,self.height/2)
    def show(self,board):
        zx = self.z / 100 * self.width
        zy = self.z / 100 * self.height
        sx = (self.x / zx * self.width) + self.width/2
        sy = (self.y / zy * self.height) + self.height/2
        # board = cv2.circle(board,(int(sx),int(sy)),3,255,-1)
        board = cv2.line(board,(int(self.x+self.width/2),int(self.y+self.height/2)),(int(sx),int(sy)),100,1)

def draw(width,height):
    stars = []
    count = 500
    for a in range(count):
        stars.append(Star(width,height))
    while True:
        canvas = np.zeros((height,width),np.uint8)
        for star in stars:
            star.show(canvas)
            star.update()

        cv2.imshow('Howdy',canvas)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    draw(1200,700)
