from flask import Flask, render_template, request

from app.assets.base import Arena
from app.assets.classes import unit_classes, UnitClass
from app.assets.equipment import Equipment
from app.assets.unit import BaseUnit, PlayerUnit

app = Flask(__name__)

heroes = {
    "player": BaseUnit,
    "enemy": BaseUnit
}

arena = Arena()  # TODO инициализируем класс арены


@app.route("/")
def menu_page():
    return render_template("index.html")# TODO рендерим главное меню (шаблон index.html)


@app.route("/fight/")
def start_fight():
    # TODO выполняем функцию start_game экземпляра класса арена и передаем ему необходимые аргументы
    # TODO рендерим экран боя (шаблон fight.html)
    pass


@app.route("/fight/hit")
def hit():
    # TODO кнопка нанесения удара
    # TODO обновляем экран боя (нанесение удара) (шаблон fight.html)
    # TODO если игра идет - вызываем метод player.hit() экземпляра класса арены
    # TODO если игра не идет - пропускаем срабатывание метода (простот рендерим шаблон с текущими данными)
    pass


@app.route("/fight/use-skill")
def use_skill():
    # TODO кнопка использования скилла
    # TODO логика пркатикчески идентична предыдущему эндпоинту
    pass


@app.route("/fight/pass-turn")
def pass_turn():
    # TODO кнопка пропус хода
    # TODO логика пркатикчески идентична предыдущему эндпоинту
    # TODO однако вызываем здесь функцию следующий ход (arena.next_turn())
    pass


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
        user_name = request.form.get("name")
        unit_class_name = request.form.get("class")
        weapon_name = request.form.get("weapon_name")
        armor_name = request.form.get("armor_name")
        player = PlayerUnit(user_name, unit_class, weapon_name, armor_name)
        heroes["player"] = player




@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    # TODO кнопка выбор соперников. 2 метода GET и POST
    # TODO также на GET отрисовываем форму.
    # TODO а на POST отправляем форму и делаем редирект на начало битвы
    pass


if __name__ == "__main__":
    app.run(debug=True)
