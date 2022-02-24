import pygame
import time as t 
from pygame import display
from pygame import key
from Physics import worldMaker
from Physics import finishMaker
import Physics
import inputs 
from Physics import render, renderFinish, distFromTarget
import random



#setting up the window
pygame.init()
Running = True #detirmies if the program keeps running to stops
screen = pygame.display.set_mode((800, 800))
screen.fill((255, 255, 255))

#setting key varibles
landerX = 400
landerY = 400
landerVY = 0
landerVX = 0
timeConstant = 60
thrust = 0
right = 0
left = 0
angle = 0
seed = 200
start = random.randint(1,20)
fuel = 1000 # seconds of burn time
mono = 20 # seconds of spinny-ness? idk how e
#these vaules are the max ammounts that the ships tank can take, as will be adding refueling into the game
fuel_cap = fuel
mono_cap = fuel 

targetX = 0
targetY = 0
targethit = False


###


#setting up the ship in pygame to be drawn in
ship_og = pygame.image.load("ship.jpg") #ship_og is the image file of the ship
ship_og = pygame.transform.rotate(ship_og, 0)
ship_og = pygame.transform.scale(ship_og, (40,40))
ship_rect = ship_og.get_rect(center= (landerX,landerY)) # ship rect is the physics body of the ship(?) 
###

#this just makes a random-ass world, if you can call i that
worldData = worldMaker(seed,start)
finishDataX, finishDataY = finishMaker(worldData) #pretty sure that this just checks the highest and lowest points of the data
###

#print statements, not sure what they do but theyll stay for now
print (finishDataX)
print(finishDataY)
###


ObjectiveX, objectiveY = Physics.objectiveGen(800)
ObjectiveActive = True



x = 0
while Running:
#### this whole section controlls frame rates ####
    frame_cap = 1.0/timeConstant
    time = t.time()
    unprocessed = 0

    while True and Running:
        can_render = False
        time_2 = t.time()
        passed = time_2 - time
        unprocessed += passed
        time = time_2

        while(unprocessed >= frame_cap) and Running:
            unprocessed -= frame_cap
            can_render = True

        if can_render: #if the frame rate is not over 60 it will start the render process
#### end of frame counter #### 



#################################################################################################################
            #start of game


            thrust, right, left = inputs.input(thrust, left, right) # gets the users inputs
            if thrust == True:
                fuel -= 1/timeConstant
                if fuel < 0:
                    Running = False
                    print("Out of fuel")
                #print(fuel,mono)
            mono -= abs(left - right)/timeConstant
            if mono < 0:
                Running = False
                print("out of mono")
            

            #converts all the angles so that 0 is up
            angle += left - right
            if angle > 180:
                angle -= 360
            if angle < -180:
                angle += 360
            #print(angle)




            landerVY, landerVX = Physics.Vectors(timeConstant,landerVY,thrust,landerVX,angle)


            #shows the ships angle
            ship = pygame.transform.rotate(ship_og, (angle))
            ship_rect = ship.get_rect(center= (landerX,landerY))

            #adds the new veloctiys of the ships, if any changes
            landerY -= landerVY
            landerX += landerVX

            Zone = 400 #?
            
            #print(distFromTarget(landerX,landerY, Zone))

            if landerY >= 800: # if lander is touching the ground
                landerY = 800
                landerVY = 0

            if Physics.alive(int(landerX),int(landerY),worldData) == False:
                print("dead")
                Running = False


            if distFromTarget(landerX,landerY,ObjectiveX,objectiveY) < 5:
                print(distFromTarget(landerX,landerY,ObjectiveX,objectiveY))
                print("me")


            

            #renders the whole screen
           
            screen.fill((255, 255, 255)) # makes the screen white
            
            screen.blit(ship, ship_rect)
            Physics.drawObject(ObjectiveX,objectiveY,20,(0,255,0),screen)

            #pygame.draw.circle(screen, (0, 0, 0), (landerX, landerY), 20) #then draws the "ship" over top
            render(worldData,screen)
            #renderFinish(finishDataY,finishDataX,screen)
            display.flip() #this shouldbe the final line, this renders the screen an updates the frames
            if Running == False:
                break

