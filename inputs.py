import pygame

#not even sure why this is in a external file, night add it to a list of functions i have

turn = 1 #this is the rate of turn per frame? 

def input(thrust, left, right): # gets users input and directly converts into thrust vaules
    events = pygame.event.get()
    x = 0
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                thrust = 1
                #print("down")
            if event.key == pygame.K_RIGHT:
                right = turn
            if event.key == pygame.K_LEFT:
                left = turn
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                thrust = 0
                #print("up")
            if event.key == pygame.K_RIGHT:
                right = 0
            if event.key == pygame.K_LEFT:
                left = 0
    return(thrust, right, left)