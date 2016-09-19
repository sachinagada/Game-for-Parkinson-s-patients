# Sachi Nagada
# Term Project Deliverable 2

from pykinect2 import PyKinectV2, PyKinectRuntime
from pykinect2.PyKinectV2 import *
import ctypes
import _ctypes
import pygame
import sys
import math
import random
import os

red = (255, 102, 102)
blue = (178, 102 , 255)
orange = (255, 165, 0)
green = (76, 153, 0)
peach = (255, 204, 152)

class Start(pygame.sprite.Sprite):
    def __init__(self,location):
        super(Start,self).__init__()
        # play button image from http://www.freevideogamesonline.org/core-images/play-game-dark-blue.png
        self.image = pygame.image.load("playbutton.png").convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = location

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
        self.rect = pygame.Rect(self.cx - self.r, self.cy - self.r,
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

class CutFruit(pygame.sprite.Sprite):
    def __init__(self,r, x, y, color):
        super(CutFruit, self).__init__()
        self.r = r
        self.x = x
        self.y = y
        self.color = color
        self.drop = 2
        self.rect = pygame.Rect(self.x-self.r, self.y - self.r,
                                2*self.r, 2*self.r)
        self.image = pygame.Surface((2 * self.r, 2 * self.r),
                                    pygame.SRCALPHA)  # make it transparent
        self.image = self.image.convert_alpha()

    def update(self):
        self.y += self.drop
        self.rect = pygame.Rect(self.x-self.r, self.y - self.r,
                                2*self.r, 2*self.r)
        pygame.draw.polygon(self.image, self.color, [(0,self.r),(self.r/4, self.r/2),( self.r-3, 0),(self.r-3, 2*self.r),(self.r/4, 3*self.r/2)])
        pygame.draw.polygon(self.image, self.color, [(self.r+3,0),(3*self.r/2, self.r/4),(2*self.r, self.r),(7*self.r/4, 3*self.r/2),(self.r+3, 2*self.r)]) 

# need to change where the ball is going to be located
# need new values to see if the ball is kicked
# update the update function to make the ball move according to kick direction
# see if there is a way to reduce the size of the ball while it goes back
class Ball(pygame.sprite.Sprite):
    # image from https://commons.wikimedia.org/wiki/File:Soccerball.svg
    def __init__(self):
        super(Ball, self).__init__()
        self.r = 30
        self.color = (0,0,0)#(255, 255, 255)
        self.cx = random.randint(100, 700)
        self.cy = 400
        self.rect = pygame.Rect(self.cx-self.r, self.cy - self.r,
                                2*self.r, 2*self.r)
        self.image = pygame.Surface((2 * self.r, 2 * self.r),
                                    pygame.SRCALPHA)  # make it transparent
        self.image = self.image.convert_alpha()
        self.dropX = 0
        self.dropY = 0
        self.a = self.r
    def update(self):
         self.cx += self.dropX
         self.cy -= self.dropY # negative because the ball has to go up

         #if ((self.dropX or self.dropY != 0) and self.r>10):
         #    self.r -= 50 # to make it look like the ball is going in the distance
         self.rect = pygame.Rect(self.cx-self.r, self.cy - self.r,
                                2*self.r, 2*self.r)
         pygame.draw.circle(self.image, self.color, (self.r, self.r), self.r)

class Goal(pygame.sprite.Sprite):
    # image from http://cdn4.kozzi.com/b1/11/248/photo-24727257-illustration-of-soccer-goal..jpg
    def __init__(self, ball):
        super(Goal, self).__init__()
        self.ball = ball
        self.image = pygame.image.load("goal.png").convert()
        self.rect = self.image.get_rect()
        self.cx = random.randint(20,700)
        self.cy = 20
        self.rect.topleft = [self.cx, self.cy]


class LeftHand(pygame.sprite.Sprite):
    def __init__(self, fruit, leftX, leftY, elbowX=0):
        super(LeftHand,self).__init__()
        self.fruit = fruit
        self.leftX = leftX
        self.leftY = leftY
        self.elbowX = elbowX
        self.color = peach
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
    def __init__(self, fruit, rightX, rightY, elbowX= 0):
        super(RightHand,self).__init__()
        self.fruit = fruit
        self.rightX = rightX
        self.rightY = rightY
        self.elbowX = elbowX
        self.color = peach 
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

class LeftFoot(pygame.sprite.Sprite):
    def __init__(self, ball, leftX, leftY):
        super(LeftFoot, self).__init__()
        self.currX = leftX
        self.currY = leftY
        self.prevX = 0
        self.prevY = 0
        self.color = peach 
        self.r = 20
        self.rect = pygame.Rect(self.currX-self.r, self.currY - self.r,
                              2*self.r, 2*self.r)
        self.image = pygame.Surface((2 * self.r, 2 * self.r),
                                    pygame.SRCALPHA) 
        self.image = self.image.convert_alpha()

    def update(self):
        self.prevX = self.currX
        self.prevY = self.currY
        self.rect = pygame.Rect(self.currX-self.r, self.currY - self.r,
                              2*self.r, 2*self.r)
        pygame.draw.circle(self.image, self.color, (self.r, self.r), self.r)


class RightFoot(pygame.sprite.Sprite):
    def __init__(self, ball, rightX, rightY):
        super(RightFoot,self).__init__()
        self.ball = ball
        self.currX = rightX
        self.currY = rightY
        self.prevX = 0
        self.prevY = 0
        self.color = peach 
        self.r = 20
        self.rect = pygame.Rect(self.currX-self.r, self.currY - self.r,
                              2*self.r, 2*self.r)
        self.image = pygame.Surface((2 * self.r, 2 * self.r),
                                    pygame.SRCALPHA) 
        self.image = self.image.convert_alpha()

    def update(self):
        self.prevX = self.currX
        self.prevY = self.currY
        self.rect = pygame.Rect(self.currX-self.r, self.currY - self.r,
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
        self.counter = 0
        self.leftCurrX = 0
        self.leftCurrY = 0
        self.rightCurrX = 0
        self.rightCurrY = 0
        self.rightElbowX = 0
        self.leftElbowX = 0
        self.differenceX = 0
        self.differenceY = 0
        self.startScreen = True
        self.FruitNinjaOver = True
        self.FruitNinjaExercise = False
        self.FruitExerciseMessage = False
        self.soccerOver = True
        self.soccerMessage = True
        self.soccerExercise = False 
        self.boxingOver = True
        self.GameOver=False
        self.score=0
        self.misses = 0 

        self.start = Start([350,250])
        self.starts = pygame.sprite.Group(self.start)

        # initialize the cutFruit and fruit Sprite group
        self.fruit = pygame.sprite.Group()
        self.cutFruit = pygame.sprite.Group() 

        self.lefthand = LeftHand(self.fruit, self.leftCurrX, self.leftCurrY)
        self.lefts = pygame.sprite.Group(self.lefthand)

        self.righthand = RightHand(self.fruit, self.rightCurrX, self.rightCurrY)
        self.rights = pygame.sprite.Group(self.righthand)

        self.ball = Ball()
        self.balls = pygame.sprite.Group()

        self.goal = Goal(self.ball)
        self.goals = pygame.sprite.Group(self.goal)

        self.rightFoot = RightFoot(self.ball, self.rightCurrX, self.rightCurrY)
        self.rightFeet = pygame.sprite.Group(self.rightFoot)

        self.leftFoot = LeftFoot(self.ball, self.leftCurrX, self.leftCurrY)
        self.leftFeet = pygame.sprite.Group(self.leftFoot)

    def timerFired(self, dt):
        if self.GameOver == False:

            if self.FruitNinjaOver == False or self.startScreen == True or self.FruitNinjaExercise == True:
                # determines if new frame and gets the joints for the body
                # first few lines below from the kinect workshop
                if self.kinect.has_new_body_frame():
                    self.bodies = self.kinect.get_last_body_frame()
                    if self.bodies is not None:
                        for i in range (0, self.kinect.max_body_count):
                            body = self.bodies.bodies[i]
                            if not body.is_tracked:
                                continue 
                            joints = body.joints   #tracking states: tracked, inferred, and not tracked
                            if (joints[PyKinectV2.JointType_HandRight].TrackingState != PyKinectV2.TrackingState_NotTracked):
                                # updates the hand position in the Right/Left hand Class
                                self.rightCurrX = joints[PyKinectV2.JointType_HandRight].Position.x
                                self.rightCurrY = joints[PyKinectV2.JointType_HandRight].Position.y
                            if joints[PyKinectRuntime.JointType_ElbowRight].TrackingState != PyKinectV2.TrackingState_NotTracked:
                                self.rightElbowX = joints[PyKinectV2.JointType_ElbowRight].Position.x
                            if joints[PyKinectRuntime.JointType_ElbowLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                                self.leftElbowX = joints[PyKinectV2.JointType_ElbowLeft].Position.x
                            if joints[PyKinectV2.JointType_HandLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                                self.leftCurrX = joints[PyKinectV2.JointType_HandLeft].Position.x
                                self.leftCurrY = joints[PyKinectV2.JointType_HandLeft].Position.y
                            for right in self.rights:
                                # the following equation was determined by corresponding different
                                # values of kinect to different values on the canvas and coming up with a line
                                # these equations make for a smooth transition of the hand visible on the screen
                                right.rightX = (900)*self.rightCurrX + 450
                                right.rightY = (-600/0.45)*self.rightCurrY + 300
                                right.elbowX = self.rightElbowX
                            for left in self.lefts:
                                left.leftX = (450/0.5)*self.leftCurrX + 225
                                left.leftY = (-600/0.45)*self.leftCurrY + 300
                                left.elbowX = self.leftElbowX
                if self.startScreen == True:
                    if pygame.sprite.groupcollide(self.rights, self.starts, False, True, 
                        pygame.sprite.collide_rect) or pygame.sprite.groupcollide(self.lefts, self.starts,
                                False, True, pygame.sprite.collide_rect):
                        self.FruitNinjaOver = False
                        self.startScreen = False
                    self.rights.update()
                    self.lefts.update()
                        
                if self.FruitNinjaOver == False:
                #increases the speed of fruit moving over time
                    if self.score > 10:
                        for fruit in self.fruit:
                            fruit.drop = (self.score//10)*2
            
                    # checks for collision between the hand and the fruit and gets rid of the fruit
                    if pygame.sprite.groupcollide(self.rights, self.fruit, False, False, 
                        pygame.sprite.collide_rect) or pygame.sprite.groupcollide(self.lefts, self.fruit,
                          False, False, pygame.sprite.collide_rect):
                        self.score +=1
                        for fruit in self.fruit:
                            self.cutFruit.add(CutFruit(fruit.r,fruit.cx,fruit.cy,fruit.color))
                            self.fruit.remove(fruit)

                    #gets rid of the fruit if at the bottom of the screen and increases the number of misses
                    for fruit in self.fruit:
                        if fruit.cy > 500 and (fruit.touchXWalls==True or fruit.touchYWalls == True):
                            self.fruit.remove(fruit)
                            self.misses +=1
                    # if the number of misses is more than 10, exercise is needed
                            if self.misses > 1:
                                # so stretching image will pop
                                self.FruitNinjaExercise = True #
                                self.counter = 0 # counter reset to 0
                                self.FruitNinjaOver = True # fruit ninja game is over
                        
                    # adds fruit when less than one on the screen
                    if len(self.fruit) < 1:
                        self.f = Fruit()
                        self.fruit.add(self.f)
                
                    # if score of 25 is achieved, move to soccer
                    if self.score > 5: 
                        self.soccerOver = False
                        self.counter = 0 # resets the counter
                        self.misses = 0 # resets the misses
                        self.FruitNinjaOver = True

                self.fruit.update()
                self.rights.update()
                self.lefts.update()
                self.cutFruit.update()

            if self.FruitNinjaExercise == True:
                self.counter += 0.01 # this number because it's the closest to counting down seconds
                # elbow and hand of opposite hands should be on top of each other so leaving a 10 cm margin for kinect buffer
                if ((abs(self.rightCurrX - self.leftElbowX) > 0.1 and abs(self.leftCurrX - self.leftElbowX) < 0.1)
                    or abs(self.rightCurrX - self.leftElbowX) < 0.1 and abs(self.leftCurrX - self.leftElbowX) > 0.1):
                    self.FruitExerciseMessage = False
                else:
                    self.FruitExerciseMessage = True
                # enough stretching, time to move to next game
                if self.counter > 30: 
                    self.soccerOver == False
                    self.misses = 0
                    self.FruitExerciseMessage = False
                    self.counter = 0
                    self.FruitNinjaExercise = False
                self.rights.update()
                self.lefts.update()

            #soccer game is ons
            if self.soccerOver == False:
                self.counter +=0.1
                # explains the rules in the first ten seconds
                if self.counter > 5:
                    self.soccerMessage = False
                # always have at least one ball on screen
                if len(self.balls) < 1:
                    newBall = Ball()
                    self.balls.add(newBall)

                    # always have at least one goal on screen
                if len(self.goals)<1:
                    for ball in self.balls:
                        newGoal = Goal(ball)
                        self.goals.add(newGoal)

                # if ball is at the 100 pixel mark, it hasn't hit the goal
                # and will be removed from the sprite
                for ball in self.balls:
                    if ball.cy < 100 or ball.cy> 600 or ball.cx < 0 or ball.cx > 800:
                        self.balls.remove(ball)
                        self.misses +=1

                # if the ball goes in the goal, score increases and new challenge
                if (pygame.sprite.groupcollide(self.balls, self.goals, 
                    True, True, pygame.sprite.collide_rect)):
                    self.score+=1

                # first few lines below from the kinect workshop
                if self.kinect.has_new_body_frame():
                    self.bodies = self.kinect.get_last_body_frame()
                    if self.bodies is not None:
                        for i in range (0, self.kinect.max_body_count):
                            body = self.bodies.bodies[i]
                            if not body.is_tracked:
                                continue 
                            joints = body.joints   #tracking states: tracked, inferred, and not tracked
                            if (joints[PyKinectV2.JointType_AnkleRight].TrackingState != PyKinectV2.TrackingState_NotTracked):
                                # updates the hand position in the Right/Left hand Class
                                self.rightCurrX = joints[PyKinectV2.JointType_AnkleRight].Position.x
                                self.rightCurrY = joints[PyKinectV2.JointType_AnkleRight].Position.y
                            if joints[PyKinectV2.JointType_AnkleLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                                self.leftCurrX = joints[PyKinectV2.JointType_AnkleLeft].Position.x
                                self.leftCurrY = joints[PyKinectV2.JointType_AnkleLeft].Position.y
                               
                            # need line to correlate the meters to pixels
                            for left in self.leftFeet:
                                left.currX = (450/0.5)*self.leftCurrX + 225
                                left.currY = (-200/0.3)*self.leftCurrY + 50
                            for right in self.rightFeet:
                                right.currX = (900)*self.rightCurrX + 450
                                right.currY = (-200/0.3)*self.rightCurrY + 50

                # if the foot kicks the ball, both should be on the screen
                # difference between the prev and current leg coordinates
                # will determine the trajectory of the ball
                if pygame.sprite.groupcollide(self.rightFeet, self.balls, 
                    False, False, pygame.sprite.collide_rect):
                    for right in self.rightFeet:
                        self.differenceX = right.prevX - right.currX
                        self.differenceY = right.currY - right.prevY
                    for ball in self.balls:
                        ball.dropX = self.differenceX
                        ball.dropY = self.differenceY

                # need to look at both feet because player can kick the ball
                # with both feet
                if pygame.sprite.groupcollide(self.leftFeet, self.balls, 
                    False, False, pygame.sprite.collide_rect):
                    for left in self.leftFeet:
                        self.differenceX = left.prevX - left.currX
                        self.differenceY = left.prevY - left.currY

                    for ball in self.balls:
                        ball.dropX = self.differenceX
                        ball.dropY = self.differenceY

                if self.score> 40:
                    self.boxingOver = False
                    self.misses = 0
                    self.counter = 0
                    self.soccerOver = True

                self.goals.update()
                self.balls.update()
                self.rightFeet.update()
                self.leftFeet.update()

                # have done well in this game and time to move on to a 
                # different game
    
                
    def redrawAll(self, screen):

        if self.GameOver == False:
            if self.startScreen == True:
                # rectangle to give a background color
                rectangle = pygame.draw.rect(screen, (204, 255, 153),(0,0,1000,1000))
                # idea for displaying this sprite from http://floppsie.comp.glam.ac.uk/Glamorgan/gaius/games/8.html
                for start in self.starts:
                    screen.blit(start.image, start.rect)
                
                #text on the screen
                myfont = pygame.font.SysFont("comicsansms",20)
                label1 = myfont.render("Please stand 1-2 meters away from the kinect", 1,blue)
                label3 = myfont.render("Please move your hand over 'Play'", 1, blue)
                label4 = myfont.render("to begin Fruit Ninja", 1, blue)                
                screen.blit(label1,(280,20))
                screen.blit(label3,(340, 140))
                screen.blit(label4,(400, 180))
                self.lefts.draw(screen)
                self.rights.draw(screen)

            if self.FruitNinjaOver == False:
                #background image from http://img3.wikia.nocookie.net/__cb39/fruitninja/images/5/50/Wiki-background
                background = pygame.image.load("FruitNinjaBackground.png")
                screen.blit(background, (0,0))
                self.fruit.draw(screen)
                self.cutFruit.draw(screen)
                self.lefts.draw(screen)
                self.rights.draw(screen)
                
                #all the text on the screen:
                myfont = pygame.font.SysFont("comicsansms",20)
                label = myfont.render("Score: " + str(self.score), 1,(245, 221, 186))
                screen.blit(label,(450,20))

            if self.FruitNinjaExercise == True:
                #background image from http://blog.hottubthings.com/wp-content/uploads/2014/06/6277148.jpg
                background = pygame.image.load("FruitNinjaExercise.png")
                screen.blit(background,(400,40))
                # text
                myfont = pygame.font.SysFont("arial", 30)
                label1 = myfont.render("Please do this stretch", 1, blue)
                label2 = myfont.render("for 30 seconds with each arm", 1, blue)
                screen.blit(label1, (350,325))
                screen.blit(label2, (275,375))
                if self.FruitExerciseMessage == True:
                    myfont = pygame.font.SysFont("arial", 40)
                    label3 = myfont.render("Please continue stretching", 1, red)
                    screen.blit(label3, (250, 450))
            
            if self.soccerOver == False:
                # background image from http://www.imgmob.net/soccer-field.html
                background = pygame.image.load("soccerfield.png")
                screen.blit(background,(0,0))
                if self.soccerMessage == True:
                    myfont = pygame.font.SysFont("comicsansms",30)
                    label = myfont.render("Kick the soccer ball and aim for the goal", 1,(0,0,153)) 
                    screen.blit(label,(300,200))
                else:
                    for goal in self.goals:
                        screen.blit(goal.image, goal.rect)
                    self.balls.draw(screen)
                    self.rightFeet.draw(screen)
                    self.leftFeet.draw(screen)
                myfont = pygame.font.SysFont("comicsansms",20)
                label = myfont.render("Score: " + str(self.score), 1,(0,0,153))
                screen.blit(label,(5,5))
        else:
            #shows a black background with "Game Over" and the score
            pygame.draw.rect(screen, (0,0,0),(0, 0, 1000, 800))
            myfont = pygame.font.SysFont("comicsansms",20)
            label = myfont.render("Score: " + str(self.score), 1,red)
            screen.blit(label,(20,20))
            myfont1 = pygame.font.SysFont("comicsansms", 40)
            label1 = myfont1.render("Game Over!", 1, red)
            screen.blit(label1, (400, 200))


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
        while True:
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