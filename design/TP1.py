# Sachi Nagada
# Term Project Deliverable 1

from pykinect2 import PyKinectV2, PyKinectRuntime
from pykinect2.PyKinectV2 import *
import ctypes
import _ctypes
import pygame
import sys
import math
import random

red = (255, 102, 102)
blue = (178, 102 , 255)
orange = (255, 165, 0)
green = (76, 153, 0)

#class Background(pygame.sprite.Sprite):
#    def __init__(self, location):
#        super(Background, self).__init__()
#        self.image = pygame.image.load("image.png")
#        self.rect = self.image.get_rect()
#        self.rect.left, self.rect.top = location
#        #self.image = pygame.Surface((1920, 1080),
        #                            pygame.SRCALPHA)  # make it transparent
        #self.image = self.image.convert_alpha()
        #pygame.image.save(self.image, filename)
        #self.imageSurf = pygame.image.load("FruitNinjaBackground.png").convert_alpha()

    


class Fruit(pygame.sprite.Sprite):
    def __init__(self):
        super(Fruit, self).__init__()
        self.r = random.randint(20,40)
        self.color = random.choice([red, blue, orange, green])
        self.cx = random.randint(40, 900)
        self.cy = random.randint(400, 600)
        self.drop = 2
        self.xdrop = random.choice([-2,2])
        self.touchXWalls = False
        self.touchYWalls = False

        self.rect = pygame.Rect(self.cx-self.r, self.cy - self.r,
                                2*self.r, 2*self.r)
        self.image = pygame.Surface((2 * self.r, 2 * self.r),
                                    pygame.SRCALPHA)  # make it transparent
        self.image = self.image.convert_alpha()

    def update(self):
        if self.cx < 10 or self.cx > 980:
            self.touchXWalls = True
        elif self.cy < 10:
            self.touchYWalls = True
         # make fruit change direction once it hits a wall
        if self.touchXWalls == False:
            self.cx += self.xdrop
        else:
            self.cx -= self.xdrop
      
        if self.touchYWalls == False:
            self.cy -= self.drop
        else:
            self.cy += self.drop
      
        self.rect = pygame.Rect(self.cx-self.r, self.cy - self.r,
                                2*self.r, 2*self.r)
        pygame.draw.circle(self.image, self.color, (self.r, self.r), self.r)
        

class LeftHand(pygame.sprite.Sprite):
    def __init__(self, fruit, leftX, leftY):
        super(LeftHand,self).__init__()
        self.fruit = fruit
        self.leftX = leftX
        self.leftY = leftY
        self.color = [255, 204, 152] #rgb values for peach
        self.r = 20
        self.rect = pygame.Rect(self.leftX-self.r, self.leftY - self.r,
                              2*self.r, 2*self.r)
        self.image = pygame.Surface((2 * self.r, 2 * self.r),
                                    pygame.SRCALPHA) 
        self.image = self.image.convert_alpha()

    def update(self):
        self.rect = pygame.Rect(self.leftX-self.r, self.leftY - self.r,
                                2*self.r, 2*self.r)
        pygame.draw.circle(self.image, self.color, (self.r, self.r), self.r)

class RightHand(pygame.sprite.Sprite):
    def __init__(self, fruit, rightX, rightY):
        super(RightHand,self).__init__()
        self.fruit = fruit
        self.rightX = rightX
        self.rightY = rightY
        self.color = [255, 204, 152] #rgb values for peach
        self.r = 20
        self.rect = pygame.Rect(self.rightX-self.r, self.rightY - self.r,
                              2*self.r, 2*self.r)
        self.image = pygame.Surface((2 * self.r, 2 * self.r),
                                    pygame.SRCALPHA) 
        self.image = self.image.convert_alpha()

    def update(self):
        self.rect = pygame.Rect(self.rightX-self.r, self.rightY - self.r,
                              2*self.r, 2*self.r)
        pygame.draw.circle(self.image, self.color, (self.r, self.r), self.r)


       
# the general outline from Lukas' blog:
# https://github.com/LBPeraza/Pygame-Asteroids/blob/master/pygamegame.py
class PygameGame(object):

    def init(self):
        pygame.init()
        self.screenWidth = 1920  #resolution of kinect
        self.screenHeight = 1080      
        self.screen = pygame.display.set_mode((960, 540), pygame.HWSURFACE|pygame.DOUBLEBUF, 32)
        # import the kinect hardware for the color source and body type
        self.kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color|PyKinectV2.FrameSourceTypes_Body)       
        self.bodies = None  
        self.frameSurface = pygame.Surface((self.kinect.color_frame_desc.Width, self.kinect.color_frame_desc.Height), 0, 32)  
        
        self.leftCurrX = 0
        self.leftCurrY = 0
        self.rightCurrX = 0
        self.rightCurrY = 0
        self.FruitNinjaOver = False
        self.GameOver=False
        self.score=0
        self.misses = 0 

       # background = Background([0,0])

        self.f = Fruit()
        self.fruit = pygame.sprite.Group(self.f)

        self.lefthand = LeftHand(self.fruit, self.leftCurrX, self.leftCurrY)
        self.lefts = pygame.sprite.Group(self.lefthand)

        self.righthand = RightHand(self.fruit, self.rightCurrX, self.rightCurrY)
        self.rights = pygame.sprite.Group(self.righthand)


    def timerFired(self, dt):
        if self.FruitNinjaOver == False:
            # determines if new frame and gets the joints for the body
            if self.kinect.has_new_body_frame():
                self.bodies = self.kinect.get_last_body_frame()
                if self.bodies is not None:
                    for i in range (0, self.kinect.max_body_count):
                        body = self.bodies.bodies[i]
                        if not body.is_tracked:
                            continue 
                        joints = body.joints   #tracking states: tracked, inferred, and not tracked
                        if joints[PyKinectV2.JointType_HandRight].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.rightCurrX = joints[PyKinectV2.JointType_HandRight].Position.x
                            self.rightCurrY = joints[PyKinectV2.JointType_HandRight].Position.y
                        if joints[PyKinectV2.JointType_HandLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.leftCurrX = joints[PyKinectV2.JointType_HandLeft].Position.x
                            self.leftCurrY = joints[PyKinectV2.JointType_HandLeft].Position.y
                        for right in self.rights:
                            # the following equation was determined by corresponding different
                            # values of kinect to different values on the canvas and coming up with a line
                            right.rightX = (900)*self.rightCurrX + 450
                            right.rightY = (-600/0.45)*self.rightCurrY + 300
                        for left in self.lefts:
                            left.leftX = (450/0.5)*self.leftCurrX + 225
                            left.leftY = (-600/0.45)*self.leftCurrY + 300

            #increases the speed of fruit moving over time
            if self.score > 10:
                for fruit in self.fruit:
                    fruit.drop = (self.score//10)*2
            
            # checks for collision between the hand and the fruit and gets rid of the fruit
            if pygame.sprite.groupcollide(self.rights, self.fruit, False, True, 
                pygame.sprite.collide_rect) or pygame.sprite.groupcollide(self.lefts, self.fruit,
                  False, True, pygame.sprite.collide_rect):
                self.score +=1

            self.fruit.update()
            self.rights.update()
            self.lefts.update()

            for fruit in self.fruit:
                if fruit.cy > 500:
                    self.fruit.remove(fruit)
                    self.misses +=1
               
            if len(self.fruit) < 1:
                self.f = Fruit()
                self.fruit.add(self.f)
                
    def redrawAll(self, screen):
        if self.GameOver == False:
            #all the text on the screen:
            myfont = pygame.font.SysFont("comicsansms",20)
            label = myfont.render("Score: " + str(self.score), 1,red)
            screen.blit(label,(20,20))
            if self.FruitNinjaOver == False:
                #screen.blit(background.image, background.rect)
                self.fruit.draw(screen)
                self.lefts.draw(screen)
                self.rights.draw(screen)

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=800, height=800, fps=50, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        pygame.init()

    def run(self):

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        while self.GameOver == False:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.GameOver = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()
       
        self.kinect.close()
        pygame.quit()


def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()