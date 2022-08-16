import random
from dataclasses import dataclass
from typing import List
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    name: str
    defence: float
    stamina_per_turn: float

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class Weapon:
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    class Meta:
        unknown = marshmallow.EXCLUDE

    @property
    def damage(self) -> float:
        weapon_damage = random.uniform(self.min_damage, self.max_damage)
        return weapon_damage


@dataclass
class EquipmentData:
    armors: List[Armor]
    weapons: List[Weapon]


class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name) -> Weapon:
        # TODO возвращает объект оружия по имени
        for weapon in EquipmentData.weapons:
            if weapon_name == weapon.name:
                return weapon

    def get_armor(self, armor_name) -> Armor:
        # TODO возвращает объект брони по имени
        for armor in EquipmentData.armors:
            if armor_name == armor.name:
                return armor

    def get_weapons_names(self) -> list:
        weapons_names_list = []
        for weapons in EquipmentData.weapons:
            weapons_names_list.append(weapons.name)
        return weapons_names_list

    def get_armors_names(self) -> list:
        armors_names_list = []
        for armors in EquipmentData.armors:
            armors_names_list.append(armors.name)
        return armors_names_list

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        # TODO этот метод загружает json в переменную EquipmentData
        equipment_file = open("C:/Users/alexg/PycharmProjects/CW4/data/equipment.json")
        data = json.load(equipment_file)
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError
