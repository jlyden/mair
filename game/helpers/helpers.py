import random

import game.helpers.sqlhelpers as sql
import game.classes.owl as owl 
import game.classes.world as world
import game.constant as const

def validateStart(nom):
    error = None
    if not nom:
        error = 'You must name your owl.'
    elif sql.getOwlIdByName(nom) is not None:
        error = 'Owl {} has already started playing.'.format(nom)
    return error

def initiateGame(nom):
    new_owl = owl.Owl(nom)
    new_owl_id = new_owl.create()
    new_world = world.World(new_owl.nom)
    new_world_id = new_world.create(new_owl_id)
    return new_world_id
