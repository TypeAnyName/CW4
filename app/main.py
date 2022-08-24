from flask import Flask, render_template, request, redirect, url_for

from app.assets.base import Arena
from app.assets.classes import unit_classes, UnitClass
from app.assets.equipment import Equipment
from app.assets.unit import BaseUnit, PlayerUnit, EnemyUnit

app = Flask(__name__)

heroes = {
    "player": PlayerUnit,
    "enemy": EnemyUnit
}

arena = Arena()  # TODO инициализируем класс арены


@app.route("/")
def menu_page():
    return render_template("index.html")  # TODO рендерим главное меню (шаблон index.html)


@app.route("/fight/")
def start_fight():
    result = arena.start_game(player=heroes["player"], enemy=heroes['enemy'])
    return render_template("fight.html", heroes=heroes, result=result)

@app.route("/fight/hit")
def hit():
    if arena.game_is_running:
        result = arena.player_hit()
        return render_template("fight.html", heroes=heroes, result=result)
    else:
        result = arena._end_game()
        return render_template("fight.html", heroes=heroes, result=result)


@app.route("/fight/use-skill")
def use_skill():
    if arena.game_is_running:
        result = arena.player_use_skill()
        return render_template("fight.html", heroes=heroes, result=result)
    else:
        result = arena._end_game()
        return render_template("fight.html", heroes=heroes, result=result)


@app.route("/fight/pass-turn")
def pass_turn():
    if arena.game_is_running:
        result = arena.next_turn()
        return render_template("fight.html", heroes=heroes, result=result)
    else:
        result = arena._end_game()
        return render_template("fight.html", heroes=heroes, result=result)


@app.route("/fight/end-fight")
def end_fight():
    # TODO кнопка завершить игру - переход в главное меню
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    if request.method == "GET":
        equipment = Equipment()
        result = {
            "header": "Выбор героя для игрока",  # для названия страниц
            "classes": unit_classes,  # для названия классов
            "weapons": equipment.get_weapons_names(),  # для названия оружия
            "armors": equipment.get_armors_names()  # для названия брони
        }
        return render_template("hero_choosing.html", result=result)
    if request.method == "POST":
        equipment = Equipment()
        user_name = request.form.get("name")
        unit_class = unit_classes[request.form.get('unit_class')]
        weapon_name = request.form.get("weapon")
        armor_name = request.form.get("armor")
        player_unit = PlayerUnit(name=user_name, unit_class=unit_class, weapon=equipment.get_weapon(weapon_name),
                                 armor=equipment.get_armor(armor_name))
        heroes["player"] = player_unit
        return redirect(url_for("choose_enemy"), 301)


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    if request.method == "GET":
        equipment = Equipment()
        result = {
            "header": "Выбор героя для соперника",  # для названия страниц
            "classes": unit_classes,  # для названия классов
            "weapons": equipment.get_weapons_names(),  # для названия оружия
            "armors": equipment.get_armors_names()  # для названия брони
        }
        return render_template("hero_choosing.html", result=result)
    if request.method == "POST":
        equipment = Equipment()
        user_name = request.form.get("name")
        unit_class = unit_classes[request.form.get('unit_class')]
        weapon_name = request.form.get("weapon")
        armor_name = request.form.get("armor")
        enemy_unit = EnemyUnit(name=user_name, unit_class=unit_class, weapon=equipment.get_weapon(weapon_name),
                                 armor=equipment.get_armor(armor_name))
        heroes["enemy"] = enemy_unit
        return redirect(url_for("start_fight"), 301)


if __name__ == "__main__":
    app.run(debug=True)
