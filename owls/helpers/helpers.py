import random

import owls.helpers.sqlhelpers as sql
import owls.constant as const

def validateStart(nom):
    error = None
    if not nom:
        error = 'You must name your owl.'
    elif sql.getOwlIdByName(nom) is not None:
        error = 'Owl {} has already started playing.'.format(nom)
    return error

def initiateGame(nom):
    owl_id = sql.insertOwl(nom)
    game_id = sql.insertGame(owl_id)
    return game_id

def buildOwlDict(id, nom, life, mice):
    this_owl = {
        "id": id,
        "nom": nom,
        "life": life,
        "mice": mice
    }
    return this_owl

# Return dictionary of owl's attributes
def getOwl(game_id):
    db_owl = sql.getOwlByGameId(game_id)
    owl_dict = {}
    if db_owl:
        owl_dict = buildOwlDict(db_owl[0], db_owl[1], db_owl[2], db_owl[3])
    return owl_dict

# Return nested dictionary of all owls' attributes
def getAllOwls():
    db_owls = sql.getOwls()
    all_owls_dict = {}
    if db_owls:
        for owl in db_owls:
            owl_dict = buildOwlDict(owl[0], owl[1], owl[2], owl[3])
            owl_id = owl_dict['id']
            all_owls_dict[owl_id] = owl_dict
    return all_owls_dict

def checkAndHandleEndOfDay(game_id, this_owl):
    if checkEndOfDay(game_id):
        endDay(game_id, this_owl)
    else:
        sql.updateEndOfDay(game_id, True)

def checkEndOfDay(game_id):
    return sql.getEndOfDay(game_id)

def endDay(game_id, owl_dict):
    owlAge(owl_dict)
    current_day = sql.getDay(game_id)
    # Every four days, mice reproduce
    if current_day % 4 == 0:
        miceReproduce(game_id)
    sql.updateDay(game_id, current_day + 1)
    sql.updateEndOfDay(game_id, False)
    return

def miceReproduce(game_id):
    current_mouse_pop = sql.getMousePopulation(game_id)
    new_mouse_pop = current_mouse_pop + current_mouse_pop // 2 
    sql.updateMousePopulation(game_id, new_mouse_pop)
    return 

def owlAge(owl_dict):
    sql.updateLife(owl_dict['id'], owl_dict['life'] - const.LIFE_PENALTY_FOR_AGING)
    return

def owlSleep(owl_dict):
    sql.updateLife(owl_dict['id'], owl_dict['life'] + const.LIFE_BONUS_FOR_SLEEPING)
    return

def owlEat(owl_dict):
    message = None
    if owl_dict['mice'] > 0:
        new_value = owl_dict['life'] + const.LIFE_BONUS_FOR_EATING
        print('new_value in owlEat() is ' + str(new_value))
        sql.updateLife(owl_dict['id'], new_value)
        sql.updateOwlMiceCount(owl_dict['id'], owl_dict['mice'] - 1)
        message = "You ate a mouse."
    else:
        message = "No mice to eat - hunt first!"
    return message

def owlHunt(game_id, owl_dict):
    message = None
    sql.updateLife(owl_dict['id'], owl_dict['life'] - const.LIFE_PENALTY_FOR_HUNTING)
    current_mouse_population = sql.getMousePopulation(game_id)
    if current_mouse_population > 0:
        # Owl can try hunt - roll proverbial dice
        if random.randrange(10) % 2 == 0:
            message = 'You caught a mouse!'
            sql.updateMousePopulation(game_id, current_mouse_population - 1)
            sql.updateOwlMiceCount(owl_dict['id'], owl_dict['mice'] + 1)
        else:
            message = 'You failed to catch a mouse.'
    else:
        message = 'There are no mice to hunt.'
    return message
