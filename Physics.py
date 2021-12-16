import numpy
import math
import time as t

import pygame
from noise import pnoise1 as pynoise1
#this is more the engine file then anything


#sets varibles
scale = 10 #1 = 1 pixel for every Metre
Gravity = 5 / scale #10 because its an easy number to work with
accel = 20 /scale / 60


#accel is the H of the triangle

def Vectors(timeConstant,velocityY,thrust,velocityX,angle): #gets all inputs and converts to x and Y pos changes to be made
    velocityY -= Gravity/timeConstant # this changes G before any thrust is added
    #Velo Y
    #H trynig to find A with angle 
    # Velo y = cos (angle) * accel
    #-angle is right

    

    if thrust == True:
        if angle == 0:
            velocityY += accel
        elif -90< angle < 0:# top right
            angle = abs(angle)
            angle = angle * (math.pi/180) #converts into rads
            velocityY += math.cos(angle) * accel

            velocityX += math.sin(angle) * accel
        
        elif 0 < angle < 90: # top left
            angle = abs(angle)
            angle = angle * (math.pi/180) #converts into rads
            velocityY += math.cos(angle) * accel
           
            velocityX += -(math.sin(angle) * accel)
            

    #print(velocityY,velocityX, angle)
    return(velocityY,velocityX) # this will return the velocity changes to x and y where it will be changed by the app.py, this just does the math


def worldMaker(seed,start):
    x = 0
    world = []
    px = 1 / seed
    px += start
    while x != 800:
        world.append(800-((pynoise1(px,1)+1)*200))
        x += 1
        px += 1/seed
    #print(world)
    return(world)


def finishMaker(worldData):
    memory = 0
    x = 0
    for item in worldData:
        if item < memory:
            return(item,x)
        else:
            x += 1
            memory = item

def renderFinish(x,finishData,screen):
    pix = 0
    while pix !=100:
        pygame.draw.circle(screen,(0,100,0),(x-50,((finishData+10))),10)
        pix+=1
    return


def alive(shipx,shipy,world):
    if world[shipx] > shipy+25:
        return(True)
    else:
        return (False)


def render(world,display):
    x = 0
    for item in world:
        pygame.draw.circle(display,(0,0,0),(x, (item)),1)
        x+=1
    return 



#isnt used but is kept here in case
def CanRender():
    frame_cap = 1.0/60
    time = t.time()
    unprocessed = 0

    while True:
        can_render = False
        time_2 = t.time()
        passed = time_2 - time
        unprocessed += passed
        time = time_2

        while(unprocessed >= frame_cap):
            unprocessed -= frame_cap
            can_render = True

        if can_render:
            return()

    