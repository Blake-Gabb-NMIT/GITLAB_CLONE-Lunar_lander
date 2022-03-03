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
fuel = 10 # seconds of burn time
mono = 10 # seconds of spinny-ness? idk 
score = 0



#this makes new astoroids
dangers = [[],[]]
#dangers = Physics.astoroidsSpawn(dangers,2)

#these vaules are the max ammounts that the ships tank can take, as will be adding refueling into the game
fuel_cap = fuel
mono_cap = fuel 

#setting up infor for target system
worldData = worldMaker(seed,start)
targetX = 0
targetY = 0
targethit = False
ObjectiveX, objectiveY = Physics.objectiveGen(800,worldData)
ObjectiveActive = True


###


#setting up the ship in pygame to be drawn in
ship_og = pygame.image.load("ship.jpg") #ship_og is the image file of the ship
ship_og = pygame.transform.rotate(ship_og, 0)
ship_og = pygame.transform.scale(ship_og, (40,40))
ship_rect = ship_og.get_rect(center= (landerX,landerY)) # ship rect is the physics body of the ship(?) 
###

#this just makes a random-ass world, if you can call i that

finishDataX, finishDataY = finishMaker(worldData) #pretty sure that this just checks the highest and lowest points of the data(unused)

### this makes the game run at 60 fps (timeConstant)

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



#################################################################################################################
            #start of game


            thrust, right, left = inputs.input(thrust, left, right) # gets the users inputs
            if thrust == True:
                fuel -= 1/timeConstant # this takes away the mono used per frame
                if fuel < 0:
                    Running = False
                    print("Out of fuel")
            mono -= abs(left - right)/timeConstant # this clauclates the ammont of mono used per frame per key press
            if mono < 0:
                Running = False
                print("out of mono")
            

            #converts all the angles so that 0 is up, only works if ship is upwards facing
            angle += left - right
            if angle > 180:
                angle -= 360
            if angle < -180:
                angle += 360
            #print(angle)




            landerVY, landerVX = Physics.Vectors(timeConstant,landerVY,thrust,landerVX,angle) #gets the ships x and y velocity


            #shows the ships angle on screen, and edits the ships render(?)
            ship = pygame.transform.rotate(ship_og, (angle))
            ship_rect = ship.get_rect(center= (landerX,landerY))

            #adds the new veloctiys of the ships, if any changes 
            landerY -= landerVY 
            landerX += landerVX

            Zone = 400 #?
            

            if landerY >= 800: # if lander is touching the ground # no longer used as touching ground kills player
                landerY = 800
                landerVY = 0

            if Physics.alive(int(landerX),int(landerY),worldData) == False: #this checks to see if the player is alive
                print("dead")
                font_color = pygame.Color('black')
                font = pygame.font.Font(None,58)
                text3 = font.render(str(score), True, font_color)
                screen.blit(text3,(400,400))
                display.flip()

                import time
                time.sleep(10)
                Running = False

            distFromObejctive = distFromTarget(landerX,landerY,ObjectiveX,objectiveY)
            if distFromObejctive < 40:
                print(distFromObejctive)
                ObjectiveX, objectiveY = Physics.objectiveGen(800,worldData)
                fuel += 2
                mono += 1
                print("wow")
                score += 1
            

             ##### Danger zone #####

             
           
           
           
           
           
           
            #renders the whole screen leave this till after all the game play elements have been done
           
            screen.fill((255, 255, 255)) # makes the screen white
            
            #shows the fuel left
            fuel_render = round(fuel,1)
            font_color = pygame.Color('black')
            font = pygame.font.Font(None,20)
            text = font.render(str(fuel_render), True, font_color)
            screen.blit(text,(50,50))

            mono_render = round(mono,1)
            font_color = pygame.Color('black')
            font = pygame.font.Font(None,20)
            text2 = font.render(str(mono_render), True, font_color)
            screen.blit(text2,(100,50))


            screen.blit(ship, ship_rect)
            
            Physics.drawObject(ObjectiveX,objectiveY,20,(0,255,0),screen)

            #pygame.draw.circle(screen, (0, 0, 0), (landerX, landerY), 20) #then draws the "ship" over top
            render(worldData,screen)
            #renderFinish(finishDataY,finishDataX,screen)
            display.flip() #this shouldbe the final line, this renders the screen an updates the frames
            if Running == False:
                break

