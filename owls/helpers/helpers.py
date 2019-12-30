import owls.helpers.sqlhelpers as sql

def validateStart(nom):
    error = None
    if not nom:
        error = 'You must name your owl.'
    elif sql.getOwlId(nom) is not None:
        error = 'Owl {} has already started playing.'.format(nom)
    return error

def initiateGame(nom):
    owl_id = sql.insertOwl(nom)
    game_id = sql.insertGame(owl_id)
    return game_id