import game.constant as const
import game.classes.owl as owl
import game.helpers.sqlhelpers as sql

@dataclass
class World:
    owl: str                    # (owl's name)
    day: int = 1
    nightfall: bool = False
    mouse_pop: int = const.INITIAL_MOUSE_POP

    def create(self, owl_id):
        game_id = sql.insertWorld(owl_id, day, nightfall, mouse_pop)
        return owl_id

    def checkAndHandleEndOfDay(self):
        if self.endOfDay():
            endDay(self)
        else:
            self.nightfall = True

    def endOfDay(self):
        return self.nightfall

    def endDay(self, owl):
        owl.age()
        # Every four days, mice reproduce
        if self.day % 4 == 0:
            miceReproduce(self)
        self.day = self.day + 1
        self.nightfall = False
        return

    def miceReproduce(self):
        mouse_pop = mouse_pop + mouse_pop // 2
        return 
