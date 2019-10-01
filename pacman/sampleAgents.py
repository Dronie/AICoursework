# sampleAgents.py
# parsons/07-oct-2017
#
# Version 1.1
#
# Some simple agents to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agents here are extensions written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util

# RandomAgent
#
# A very simple agent. Just makes a random pick every time that it is
# asked for an action.
class RandomAgent(Agent):

    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Random choice between the legal options.
        return api.makeMove(random.choice(legal), legal)

# RandomishAgent
#
# A tiny bit more sophisticated. Having picked a direction, keep going
# until that direction is no longer possible. Then make a random
# choice.
class RandomishAgent(Agent):

    # Constructor
    #
    # Create a variable to hold the last action
    def __init__(self):
         self.last = Directions.STOP
    
    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # If we can repeat the last action, do it. Otherwise make a
        # random choice.
        if self.last in legal:
            return api.makeMove(self.last, legal)
        else:
            pick = random.choice(legal)
            # Since we changed action, record what we did
            self.last = pick
            return api.makeMove(pick, legal)

# SensingAgent
#
# Doesn't move, but reports sensory data available to Pacman
class SensingAgent(Agent):

    def getAction(self, state):

        # Demonstrates the information that Pacman can access about the state
        # of the game.

        # What are the current moves available
        legal = api.legalActions(state)
        print "Legal moves: ", legal

        # Where is Pacman?
        pacman = api.whereAmI(state)
        print "Pacman position: ", pacman

        # Where are the ghosts?
        print "Ghost positions:"
        theGhosts = api.ghosts(state)
        for i in range(len(theGhosts)):
            print theGhosts[i]

        # How far away are the ghosts?
        print "Distance to ghosts:"
        for i in range(len(theGhosts)):
            print util.manhattanDistance(pacman,theGhosts[i])

        # Where are the capsules?
        print "Capsule locations:"
        print api.capsules(state)
        
        # Where is the food?
        print "Food locations: "
        print api.food(state)

        # Where are the walls?
        print "Wall locations: "
        print api.walls(state)
        
        # getAction has to return a move. Here we pass "STOP" to the
        # API to ask Pacman to stay where they are.
        return api.makeMove(Directions.STOP, legal)

class GoWestAgent(Agent):
    
    def getAction(self, state):
        # Agent that tries to get as far left on the screen as possible

        # Initialize direction
        direction = Directions.WEST

        # Get Legal Actions
        legal = api.legalActions(state)

        # Check if going west is possible if not go either north or south (prioritizing north)
        if "West" not in legal:
            if "North" in legal:
                direction = Directions.NORTH
            elif "South" in legal:
                direction = Directions.SOUTH
        
        return api.makeMove(direction, legal)

class SurvivalAgent(Agent):
        # agent that tries to stay as far away form the ghosts as possible
        
        def getAction(self, state):

            # Get legal actions
            legal = api.legalActions(state)

            # Get location of Pacman
            pacman = api.whereAmI(state)

            # Get location of Ghosts
            locGhosts = api.ghosts(state)
            #print "locGhosts: ", locGhosts

            # Get distance between pacman and the ghosts
            for i in locGhosts:
                p_g_dist = util.manhattanDistance(pacman, i)

            # Get distance between ghosts
            g_g_dist = util.manhattanDistance(locGhosts[0], locGhosts[1])
            #print "g_g_dist:", g_g_dist

            # Get distance between pacman and first Ghost
            dist = []
            dist.append(locGhosts[0][0] - pacman[0])
            dist.append(locGhosts[0][1] - pacman[1])

            return api.makeMove(Directions.STOP, legal)
        
class HungryAgent(Agent):

    def __init__(self):
        self.wall_locs = []
        self.open_space = []
        self.adjacencies = []
        self.direction = Directions.STOP

    def getAction(self, state):
        # Agent that always moves to the nearest peice of food

        # Get legal actions
        legal = api.legalActions(state)
        #legal.remove(Directions.STOP)

        # Get location of Pacman
        pacman = api.whereAmI(state)
        

        # Get locations of all peices of food
        all_food = api.food(state)
        #print "all_food", all_food

        # Get locations of walls
        if self.wall_locs == []:
            self.wall_locs = api.walls(state)

        if self.open_space == []:
            for i in range(0, self.wall_locs[len(self.wall_locs) - 1][0]):
                for j in range(0, self.wall_locs[len(self.wall_locs) - 1][1]):
                    if (i, j) not in self.wall_locs:
                        self.open_space.append((i, j))

        # Find closest peice of food
        dists = []
        for i in all_food:
            dists.append(util.manhattanDistance(pacman, i))
        closest_food = min(dists)
        
        closest_index = 0
        for i in dists:
            if i == closest_food:
                closest_index = dists.index(closest_food)
        
        closest_food = all_food[closest_index]

        print "Pacman:", pacman, "Closest Pellet:", closest_food

        if closest_food[0] > pacman[0] and 'East' in legal:
            self.direction = Directions.EAST
            print "Going East"
        elif closest_food[0] < pacman[0] and 'West' in legal:
            self.direction = Directions.WEST
            print "Going West"
        elif closest_food[1] > pacman[1] and 'North' in legal:
            self.direction = Directions.NORTH
            print "Going North"
        elif closest_food[1] < pacman[1] and 'South' in legal:
            self.direction = Directions.SOUTH
            print "Going South"
        elif self.direction in legal:
            return api.makeMove(self.direction, legal)
        elif len(legal) >= 4:
            legal.remove(Directions.STOP)
            pick = random.choice(legal)
            # Since we changed action, record what we did
            self.direction = pick
            return api.makeMove(pick, legal)
        else:
            legal.remove(Directions.STOP)
            pick = random.choice(legal)
            # Since we changed action, record what we did
            self.direction = pick
            return api.makeMove(pick, legal)

        print(len(legal))


        '''else:
            if 'North' in legal and 'South' in legal and 'East' not in legal and 'West' not in legal:
                direction = Directions.SOUTH
            elif 'East' in legal and random.random() > 0.5:
                direction = Directions.EAST
            elif 'West' in legal and random.random() > 0.5:
                direction = Directions.WEST
            elif 'North' in legal and random.random() > 0.5:
                direction = Directions.NORTH
            elif 'South' in legal and random.random() > 0.5:
                direction = Directions.SOUTH
            elif 'South' not in legal and 'North' in legal and 'East' in legal and 'West' in legal:
                direction = Directions.NORTH'''
        
        # TO DO: Implement some kind of pathfinding algorithm: this will make it alot easier

        return api.makeMove(self.direction, legal)

class CornerSeekingAgent(Agent):
    def __init__(self):
        self.explored = []
        self.waypoints = []
    
    def getAction(self, state):
        legal = api.legalActions(state)

        corners = api.corners(state)
        print(corners)

        return api.makeMove(Directions.STOP, legal)
