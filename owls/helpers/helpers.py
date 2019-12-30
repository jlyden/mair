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

def buildOwlDict(id, nom, life, mice):
    this_owl = {
        "id": id,
        "nom": nom,
        "life": life,
        "mice": mice
    }
    return this_owl

def getOwl(game_id):
    db_owl = sql.getOwlByGameId(game_id)
    owl_dict = {}
    if db_owl:
        owl_dict = buildOwlDict(db_owl[0], db_owl[1], db_owl[2], db_owl[3])
    return owl_dict

def getAllOwls():
    db_owls = sql.getOwls()
    all_owls_dict = {}
    if db_owls:
        for owl in db_owls:
            owl_dict = buildOwlDict(owl[0], owl[1], owl[2], owl[3])
            owl_id = owl_dict['id']
            all_owls_dict[owl_id] = owl_dict
            print(str(all_owls_dict))
    return all_owls_dict
