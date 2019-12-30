from owls.db import get_db

# Inserts
def insertOwl(nom):
    db = get_db()
    db.execute('INSERT INTO owl (nom) VALUES (?)', (nom,))
    db.commit()
    owl_id = db.execute('SELECT last_insert_rowid()').fetchone()
    return owl_id[0]

def insertGame(owl_id):
    # Initiate game & counters
    db = get_db()
    db.execute('INSERT INTO game (owl_id) VALUES (?)', (owl_id,))
    game_id = db.execute('SELECT last_insert_rowid()').fetchone()
    db.execute('INSERT INTO counters (game_id) VALUES (?)', (game_id[0],))
    db.commit()
    return game_id[0]


# Updates
def updateLife(owl_id, new_value):
    db = get_db()
    db.execute('UPDATE owl SET life = ? WHERE id = ?', (new_value, owl_id,))
    db.commit()
    return

def updateOwlMiceCount(owl_id, new_value):
    db = get_db()
    db.execute('UPDATE owl SET mice = ? WHERE id = ?', (new_value, owl_id,))
    db.commit()
    return

def updateEndOfDay(game_id, new_value):
    db = get_db()
    db.execute('UPDATE counters SET endOfDay = ? WHERE game_id = ?', (new_value, game_id,))
    db.commit()
    return

def updateDay(game_id, new_value):
    db = get_db()
    db.execute('UPDATE counters SET day = ? WHERE game_id = ?', (new_value, game_id,))
    db.commit()
    return

def updateMousePopulation(game_id, new_value):
    db = get_db()
    db.execute('UPDATE counters SET mousePopulation = ? WHERE game_id = ?', (new_value, game_id,))
    db.commit()
    return


# Get Owls
def getOwlIdByName(nom):
    db = get_db()
    owl_id = db.execute('SELECT id FROM owl WHERE nom = ?', (nom,)).fetchone()
    return owl_id

def getOwlById(owl_id):
    db = get_db()
    return db.execute('SELECT * FROM owl WHERE id = ?', (owl_id,)).fetchone()

def getOwlByGameId(game_id):
    db = get_db()
    owl = db.execute('SELECT o.* FROM game g            \
        JOIN owl o ON o.id = g.owl_id                   \
            WHERE g.id = ?', (game_id,)).fetchone()
    return owl

def getOwls():
    db = get_db()
    return db.execute('SELECT * FROM owl',).fetchall()


# Get Others
def getGameIdByOwlId(owl_id):
    db = get_db()
    game_id = None
    result = db.execute('SELECT id FROM game WHERE owl_id = ?', (owl_id,)).fetchone()
    if result:
        game_id = result[0]
    return game_id

def getDay(game_id):
    db = get_db()
    counters_day = db.execute('SELECT day FROM counters WHERE game_id = ?', (game_id,)).fetchone()
    return counters_day[0]

def getEndOfDay(game_id):
    db = get_db()
    counters_end_day = db.execute('SELECT endOfDay FROM counters WHERE game_id = ?', (game_id,)).fetchone()
    return counters_end_day[0]

def getMousePopulation(game_id):
    db = get_db()
    counters_mice_pop = db.execute('SELECT mousePopulation FROM counters WHERE game_id = ?', (game_id,)).fetchone()
    return counters_mice_pop[0]
