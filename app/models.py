import random

from app import db
from . constant import *


class Owl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(64), index=True, unique=True)
    life = db.Column(db.Integer, default=INITIAL_LIFE)
    mice = db.Column(db.Integer, default=0)
    world = db.relationship('World', backref='owl', uselist=False)

    def __rep__(self):
        return '<Owl {}, life {}>'.format(self.username, self.life)

    def age(self):
        self.life = self.life - LIFE_PENALTY_FOR_AGING
        db.session.commit()
        return self

    def sleep(self):
        self.life = self.life + LIFE_BONUS_FOR_SLEEPING
        db.session.commit()
        return self

    def eat(self):
        message = None
        if self.mice > 0:
            self.life = self.life + LIFE_BONUS_FOR_EATING
            self.mice = self.mice - 1
            db.session.commit()
            message = "You ate a mouse."
        else:
            message = "No mice to eat -- hunt first."
        return self, message

    def hunt(self, world):
        self.life = self.life - LIFE_PENALTY_FOR_HUNTING
        message = None
        if random.randrange(10) % 2 == 0:
            message = 'You caught a mouse!'
            world.mouse_pop = world.mouse_pop - 1
            self.mice = self.mice + 1
            db.session.commit()
        else:
            message = 'Hunt failed - no mouse today.'
        return self, world, message


class World(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owl_id = db.Column(db.Integer, db.ForeignKey('owl.id'), nullable=False)
    day = db.Column(db.Integer, default=1)
    nightfall = db.Column(db.Boolean, default=False)
    mouse_pop = db.Column(db.Integer, default=INITIAL_MOUSE_POP)

    def __rep__(self):
        return '<Day {}, mouse_pop {}>'.format(self.day, self.mouse_pop)

    def checkAndHandleEndOfDay(self, owl):
        if self.nightfall:
            self.endDay(owl)
        else:
            self.nightfall = True
            db.session.commit()

    def endDay(self, owl):
        owl.age()
        # Every four days, mice reproduce
        if self.day % 4 == 0:
            miceReproduce(self)
        self.day = self.day + 1
        self.nightfall = False
        db.session.commit()
        flash('Day ended')
        return

    def miceReproduce(self):
        mouse_pop = mouse_pop + mouse_pop // 2
        db.session.commit()
        return 
