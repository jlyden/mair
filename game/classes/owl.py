import random
import game.constant as const
import game.helpers.sqlhelpers as sql

@dataclass
class Owl:
    nom: str
    life: int = const.INITIAL_LIFE
    mice: int = 0

    def create(self) -> Owl:
        owl_id = sql.insertOwl(nom, life, mice)
        return owl_id

    def age(self) -> Owl:
        self.life = self.life - const.LIFE_PENALTY_FOR_AGING
        return self

    def sleep(self) -> Owl:
        self.life = self.life + const.LIFE_BONUS_FOR_SLEEPING
        return self

    def eat(self) -> Owl:
        self.life = self.life + const.LIFE_BONUS_FOR_EATING
        self.mice = self.mice - 1
        return self

    def hunt(self, game) -> Owl:
        self.life = self.life - const.LIFE_PENALTY_FOR_HUNTING
        message = None
        if random.randrange(10) % 2 == 0:
            message = 'You caught a mouse!'
            game.mouse_pop = game.mouse_pop - 1
            self.mice - self.mice + 1
        else:
            message = 'Hunt failed - no mouse today.'
        return self, game, message