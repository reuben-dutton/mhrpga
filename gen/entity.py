import os
import sys
import json
import copy
import numpy as np

curr_dir = os.path.dirname(os.path.realpath(__file__))
base_dir = os.path.normpath(os.path.join(curr_dir, '..'))
sys.path.append(base_dir)


class EntityCreator:

    def __init__(self, resources):
        self.resources = resources

    def gen_event_entities(self, gen_dict):
        characters = [self.gen_character() for i in range(gen_dict['characters'])]
        opens = [self.gen_open() for i in range(gen_dict['opens'])]
        dungeons = [self.gen_dungeon() for i in range(gen_dict['dungeons'])]
        towns = [self.gen_town() for i in range(gen_dict['towns'])]
        items = [self.gen_item() for i in range(gen_dict['items'])]
        return dict(characters=characters,
                    opens=opens,
                    dungeons=dungeons,
                    towns=towns,
                    items=items)

    def gen_character(self):
        name = self.resources.get_name('character')
        no_items = np.random.randint(5) + 1
        inventory = [self.gen_item() for i in range(no_items)]
        gold = np.random.randint(100)
        weapon = self.gen_item(item_type='weapon')
        consume = self.gen_item(item_type='consumable')
        misc = self.gen_item(item_type='misc')
        return dict(name=name,
                    inventory=inventory,
                    gold=gold,
                    weapon=weapon,
                    consumable=consume,
                    misc=misc,
                    type="character")

    def gen_open(self):
        name = self.resources.get_name('open')
        return dict(name=name,
                    type="open")

    def gen_town(self):
        name = self.resources.get_name('town')
        tavern = self.gen_tavern()
        school = self.gen_school()
        shop = self.gen_shop()
        church = self.gen_church()
        return dict(name=name,
                    tavern=tavern,
                    school=school,
                    shop=shop,
                    church=church,
                    type='town')

    def gen_tavern(self):
        name = self.resources.get_name('tavern')
        no_occupants = 5
        occupants = [self.gen_character() for i in range(no_occupants)]
        return dict(name=name,
                    occupants=occupants,
                    type='tavern')

    def gen_school(self):
        name = self.resources.get_name('school')
        no_occupants = 3
        occupants = [self.gen_character() for i in range(no_occupants)]
        return dict(name=name,
                    occupants=occupants,
                    type='school')

    def gen_shop(self):
        owner = self.gen_character()
        name = self.resources.get_name('shop', owner=owner)
        no_occupants = 2
        occupants = [self.gen_character() for i in range(no_occupants)]
        no_items = 3
        items = [self.gen_item() for i in range(no_items)]
        return dict(name=name,
                    owner=owner,
                    occupants=occupants,
                    items=items,
                    type='shop')

    def gen_church(self):
        name = self.resources.get_name('church')
        no_occupants = 3
        occupants = [self.gen_character() for i in range(no_occupants)]
        return dict(name=name,
                    occupants=occupants,
                    type='church')

    def gen_dungeon(self):
        name = self.resources.get_name('dungeon')
        return dict(name=name,
                    type='dungeon')

    def gen_item(self, item_type=None):
        item = copy.deepcopy(self.resources.get_item(item_type))
        item['full_name'] = item['adjective'] + item['name']
        item['shop_desc'] = "{full_name} ({price}g)".format(**item)
        return item
