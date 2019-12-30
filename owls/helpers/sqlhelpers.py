from owls.db import get_db

def insertOwl(nom):
    db = get_db()
    db.execute('INSERT INTO owl (nom) VALUES (?)', (nom,))
    db.commit()
    owl_id = db.execute('SELECT last_insert_rowid()').fetchone()
    return owl_id[0]

def getOwlIdByName(nom):
    db = get_db()
    owl_id = db.execute('SELECT id FROM owl WHERE nom = ?', (nom,)).fetchone()
    print('owl_id in getOwlId is ' + str(owl_id))
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

def insertGame(owl_id):
    # Initiate game & counters
    db = get_db()
    db.execute('INSERT INTO game (owl_id) VALUES (?)', (owl_id,))
    game_id = db.execute('SELECT last_insert_rowid()').fetchone()
    db.execute('INSERT INTO counters (game_id) VALUES (?)', (game_id[0],))
    db.commit()
    return game_id[0]

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
