#
# Body.py
# Class file for the celestial bodies.
#

import math
import pygame
from random import *
import numpy as np
from database_creation.database_antikythera import *

# set up colors:


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

############################## celestial body object
class Body(object):
    def __init__(self, n, m, x, y, r, c, s, root, tr):
        # mass, postion (x, y), color
        self.name = n
        self.mass = m
        self.position = np.array([x, y])
        self.last_position = np.array([x-1, y-1])
        self.velocity = np.array([randint(10,15), randint(10,15)])
        self.accel = np.array([0,0])
        self.color = c
        self.radius = r
        self.sun = s
        self.surface = root
        self.trails = tr
        self.sunDistance = math.sqrt((self.position[0] - 800)**2 + (self.position[1] - 400)**2)


    def applyForce(self, force):
        # apply forces to a body
        f = force / self.mass
        self.accel = np.add(self.accel, f)

    def update(self):
        if self.sun == False:
            # update position based on velocity and reset accel if not sun
            self.velocity = np.add(self.velocity, self.accel)
            self.last_position = self.position
            self.position = np.add(self.position, self.velocity)
            self.sunDistance = math.sqrt((self.position[0] - 800) ** 2 + (self.position[1] - 400) ** 2)
            self.accel = 0

    def display(self):
        # draw over old object location
        pygame.draw.circle(self.surface, BLACK, (int(self.last_position[0]), int(self.last_position[1])), self.radius)  	# (drawLayer, color, (coordinates), radius)

        # draw trail (Comment this line out to remove trails)
        if self.trails:
            pygame.draw.line(self.surface, self.color, (int(self.last_position[0]), int(self.last_position[1])), (int(self.position[0]), int(self.position[1])), 5)

        # draw new object location
        pygame.draw.circle(self.surface, self.color, (int(self.position[0]), int(self.position[1])), self.radius)


    def attract(self, m, g):
        # gravitational code rewritten from Daniel Shiffman's "Nature of Code"
        force = self.position - m.position
        distance = np.linalg.norm(force)
        distance = constrain(distance, 5.0, 25.0)
        force = normalize(force)
        strength = (g * self.mass * m.mass) / float(distance * distance)
        force = force * strength
        return force


    def printData(self):
        if(self.name == 'Sun'):
             print("\n\n\n\n\n\n\n===============================")
             print("Name: " + self.name)
             print("Mass: " + str(self.mass))
             print("Position: " + str(self.position))
             print("===============================")
        else:
             print("\n\n\n\n\n===============================")
             print("Name: " + self.name)
             print("Mass: " + str(self.mass))
             print("Position: " + str(self.position))
             print("Velocity: " + str(self.velocity))
             print("Distance from Sun: " + str(self.sunDistance))
             print("===============================")

        return

    def eclipseCheck(self, body2, sun):
        col = math.isclose(np.cross(self.position - sun.position, body2.position - sun.position), 0, abs_tol=25)
        if self.sunDistance > body2.sunDistance:
            betweenx = self.position[0] <= body2.position[0] <= sun.position[0] or sun.position[0] <= body2.position[0] <= self.position[0]
            betweeny = self.position[1] <= body2.position[1] <= sun.position[1] or sun.position[1] <= body2.position[1] <= self.position[1]
        else:
            betweenx = body2.position[0] <= self.position[0] <= sun.position[0] or sun.position[0] <= self.position[0] <= body2.position[0]
            betweeny = body2.position[1] <= self.position[1] <= sun.position[1] or sun.position[1] <= self.position[1] <= body2.position[1]
        return (col and (betweenx if self.position[0] != sun.position[0] else betweeny))


############################## mathematical functions

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))


def normalize(force):
    normal = np.linalg.norm(force, ord=1)
    if normal == 0:
        normal = np.finfo(force.dtype).eps
    return force / normal

