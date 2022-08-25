from app.assets.unit import BaseUnit, PlayerUnit, EnemyUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False

    def start_game(self, player: PlayerUnit, enemy: EnemyUnit) -> None:
        self.player = player
        self.enemy = enemy
        self.game_is_running = True
        return "Бой начался"

    def _check_players_hp(self):
        self.battle_result = ""
        if self.player.health_points <= 0:
            self.battle_result == "Игрок проиграл"
            return self.battle_result
        elif self.enemy.health_points <= 0:
            self.battle_result == "Игрок выиграл"
            return self.battle_result
        else:
            pass

    def _stamina_regeneration(self):
        if self.player.stamina_points < self.player.unit_class.max_stamina:
            self.player.stamina += self.STAMINA_PER_ROUND
        else:
            pass
        if self.enemy.stamina_points < self.enemy.unit_class.max_stamina:
            self.enemy.stamina += self.STAMINA_PER_ROUND
        else:
            pass

    def next_turn(self):
        result = self._check_players_hp()
        if result:
            return result
        else:
            self._stamina_regeneration()
            result = self.enemy.hit(self.player)
            return result

    def _end_game(self):
        self._instances = {}
        self.game_is_running = False

    def player_hit(self):
        result = self.player.hit(self.enemy)
        enemy_result = self.next_turn()
        return f"{result} \n {enemy_result}"

    def player_use_skill(self):
        result = self.player.use_skill(self.enemy)
        enemy_result = self.next_turn()
        return f"{result} \n {enemy_result}"
