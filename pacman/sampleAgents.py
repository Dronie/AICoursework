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
import numpy as np
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

    def getAction(self, state):
        # Agent that always moves to the nearest peice of food

        # Initialize direction
        direction = Directions.STOP

        # Get legal actions
        legal = api.legalActions(state)
        print legal

        # Get location of Pacman
        pacman = api.whereAmI(state)
        print "pacman", pacman

        # Get locations of all peices of food
        all_food = api.food(state)
        #print "all_food", all_food

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
        print "closest_food", closest_food

        if closest_food[0] > pacman[0] and 'East' in legal:
            direction = Directions.EAST
        elif closest_food[0] < pacman[0] and 'West' in legal:
            direction = Directions.WEST
        elif closest_food[1] > pacman[1] and 'North' in legal:
            direction = Directions.NORTH
        elif closest_food[1] < pacman[1] and 'South' in legal:
            direction = Directions.SOUTH
        
        if direction not in legal:
            direction = Directions.EAST

        

        return api.makeMove(direction, legal)
