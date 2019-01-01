import os
import sys
import json
import numpy as np
import copy

curr_dir = os.path.dirname(os.path.realpath(__file__))
base_dir = os.path.normpath(os.path.join(curr_dir, '..'))
sys.path.append(base_dir)

char_path = os.path.join(curr_dir, 'char.json')
region_path = os.path.join(curr_dir, 'region.json')
event_path = os.path.join(curr_dir, 'event.json')

null_item = {"name": "None", 
             "adjective": "",
             "full_name": "None",
             "price": 0,
             "shop_desc": "None",
             "type": "item"}

class DataAccess:

    def __init__(self, entitygen):
        self.char = {}
        self.region = {}
        self.event = {}
        self.entitygen = entitygen

    # READING AND SAVING DATA METHODS

    def readdata(self):
        self.char = json.loads(open(char_path).read())
        self.region = json.loads(open(region_path).read())
        self.event = json.loads(open(event_path).read())

    def savedata(self):
        with open(char_path, 'w') as j:
            json.dump(self.char, j)
        with open(region_path, 'w') as j:
            json.dump(self.region, j)
        with open(event_path, 'w') as j:
            json.dump(self.event, j)

    # METADATA METHODS

    def get_next_event_id(self):
        next_event_id = self.event["next_event"]
        if next_event_id == "None":
            next_event_id = None
        return next_event_id

    def get_event_probs(self):
        return self.event["prob"]

    def format_event(self, eventjson, gen):
        format_dict = dict(char=self.char,
                           region=self.region,
                           event=self.event,
                           gen=gen,
                           spec=eventjson['spec'])
        event_s = eventjson['event_s']
        action_s = eventjson['action_s']
        result_s = eventjson['result_s']
        new_event_s = event_s.format(**format_dict)
        new_action_s = []
        for item in action_s:
            new_item = item.format(**format_dict)
            new_action_s.append(new_item)
        new_result_s = []
        for sublist in result_s:
            new_sublist = []
            for item in sublist:
                new_sublist.append(item.format(**format_dict))
            new_result_s.append(new_sublist)
        strings = eventjson['strings']
        new_strings = dict()
        for key, item in strings.items():
            new_item = []
            for entry in item:
                new_item.append(entry.format(**format_dict))
            new_strings[key] = new_item
        return_dict = {'event_s': new_event_s,
                       'action_s': new_action_s,
                       'result_s': new_result_s,
                       'strings': new_strings}
        return return_dict

    def check_requirements(self, requirements):
        boolean_array = []
        satisfied = ""
        for requirement in requirements:
            append = ""
            for item in requirement:
                result = eval('self.{}'.format(item))
                if not result[0]:
                    append = result[1]
            if len(requirement) == 0:
                append = ""
            boolean_array.append(append)
        return boolean_array

    def get_current_event(self):
        return copy.deepcopy(self.event['current_event'])

    def change_current_event(self, eventjson):
        self.event['current_event'] = eventjson

    def get_previous_event(self):
        return copy.deepcopy(self.event['previous_event'])

    def change_previous_event(self, eventjson):
        self.event['previous_event'] = eventjson

    def get_choice(self):
        return self.event['choice']

    def change_choice(self, choice):
        self.event['choice'] = choice

    def get_post_id(self):
        return self.event['post_id']

    def change_post_id(self, post_id):
        self.event['post_id'] = post_id

    def add_string(self, type, string):
        self.event['previous_event']['string']['type'].append(string)


    # REGION METHODS


    def get_location_type(self):
        return self.region['local']['type']

    def get_global_location(self):
        return self.region['global']['inner']

    def change_open(self, newopen):
        self.region['global']['outer'] = newopen
        self.region['global']['inner'] = newopen
        self.region['local'] = newopen

    def enter_town(self, town):
        self.region['global']['inner'] = town
        self.region['local'] = town

    def enter_dungeon(self, dungeon):
        self.region['global']['inner'] = dungeon
        self.region['local'] = dungeon

    def enter_church(self):
        church = self.region['global']['inner']['church']
        self.region['local'] = church

    def enter_tavern(self):
        tavern = self.region['global']['inner']['tavern']
        self.region['local'] = tavern

    def enter_shop(self):
        shop = self.region['global']['inner']['shop']
        self.region['local'] = shop

    def enter_school(self):
        school = self.region['global']['inner']['school']
        self.region['local'] = school

    def leave_building(self):
        self.region['local'] = self.region['global']['inner']

    def leave_dungeon(self):
        self.region['local'] = self.region['global']['outer']
        self.region['global']['inner'] = self.region['global']['outer']

    def leave_town(self):
        self.region['local'] = self.region['global']['outer']
        self.region['global']['inner'] = self.region['global']['outer']

    def remove_store_item(self, index):
        if self.region['local']['type'] == 'town':
            self.region['local']['shop']['items'].pop(index)
            self.update_store_inventory()
        elif self.region['local']['type'] == 'shop':
            self.region['local']['items'].pop(index)
            self.update_store_inventory()
        else:
            pass

    def update_store_inventory(self):
        if self.region['local']['type'] == 'town':
            current_inventory = self.region['local']['shop']['items']
            size = len(current_inventory)
            new_items = [self.entitygen.gen_item() for i in range(4-size)]
            current_inventory.extend(new_items)
            self.region['global']['inner']['shop']['items'] = current_inventory
            self.region['local']['shop']['items'] = current_inventory
        elif self.region['local']['type'] == 'shop':
            current_inventory = self.region['local']['items']
            size = len(current_inventory)
            new_items = [self.entitygen.gen_item() for i in range(4-size)]
            current_inventory.extend(new_items)
            self.region['global']['inner']['shop']['items'] = current_inventory
            self.region['local']['items'] = current_inventory
        else:
            pass


    # EVENT METHODS


    def change_event_id(self, new_event_id):
        self.event["next_event"] = new_event_id

    def reset_event_id(self):
        self.event["next_event"] = "None"

    def change_event_prob(self, event_id, event_weight):
        self.event['prob'][event_id] = event_weight

    def alter_event_prob(self, event_id, multiplier):
        prob = self.event['prob'][event_id] * multiplier
        self.event['prob'][event_id] = int(prob)

    def reset_event_prob(self, event_id):
        self.event['prob'][event_id] = 0


    # CHARACTER METHODS


    def get_name(self):
        return self.char['name']

    def change_name(self, new_name):
        self.char['name'] = new_name

    def get_status(self):
        return self.char['status']

    def change_status(self, status):
        self.char['status'] = status

    def get_gold(self):
        return self.char['gold']

    def change_gold(self, gold_change, change_type="relative"):
        if change_type is 'relative':
            self.char['gold'] += gold_change
        elif change_type is 'absolute':
            self.char['gold'] = gold_change
        else:
            pass

    def get_items(self):
        return self.char['inventory']

    def get_quest_items(self):
        return self.char['quest']

    def get_all_items(self):
        return self.get_items() + self.get_quest_items()

    def buy_store_item(self, index):
        item = self.region['local']['items'][index]
        self.buy_item(item)
        self.remove_store_item(index)

    def buy_item(self, item):
        self.add_item(item)
        self.change_gold(-item['price'])

    def add_item(self, item, quest=False, index=None):
        if index is None:
            if quest:
                self.char['quest'].append(item)
            else:
                self.char['inventory'].append(item)
        else:
            if quest:
                self.char['quest'].insert(index, item)
            else:
                self.char['inventory'].insert(index, item)
        self.update_sale_items()
        self.update_item_types()

    def remove_item(self, name):
        correct_item = None
        for item in self.char['inventory']:
            if item['name'] == name:
                correct_item = item
        if correct_item is not None:
            self.char['inventory'].remove(correct_item)
        for item in self.char['quest']:
            if item['name'] == name:
                correct_item = item
        self.char['quest'].remove(correct_item)
        self.update_sale_items()
        self.update_item_types()

    def remove_specific_item(self, full_name):
        correct_item = None
        for item in self.char['inventory']:
            if item['full_name'] == full_name:
                correct_item = item
        if correct_item is not None:
            self.char['inventory'].remove(correct_item)
        for item in self.char['quest']:
            if item['full_name'] == full_name:
                correct_item = item
        self.char['quest'].remove(correct_item)
        self.update_sale_items()
        self.update_item_types()

    def sell_sale_item(self, item_index):
        removed_item = self.char['for_sale'].pop(item_index)
        self.char['inventory'].remove(removed_item)
        self.update_sale_items()
        self.update_item_types()
        self.change_gold(removed_item['price'])

    def lose_sale_item(self, index):
        removed_item = self.char['for_sale'].pop(index)
        self.char['inventory'].remove(removed_item)
        self.update_sale_items()
        self.update_item_types()

    def lose_random_sale_item(self):
        item_count = 0
        for item in self.char['for_sale']:
            if item['name'] != 'None':
                item_count += 1
        if item_count > 0:
            random_index = np.random.randint(item_count)
            removed_item = self.char['for_sale'].pop(random_index)
            self.char['for_sale'].append(null_item)
            self.char['inventory'].remove(removed_item)
            self.update_sale_items()
            self.update_item_types()

    def update_sale_items(self):
        new_sale_items = []
        for item in self.char['inventory']:
            if item not in new_sale_items:
                new_sale_items.append(item)
        if len(new_sale_items) > 4:
            new_sale_items = new_sale_items[:3]
        else:
            for i in range(4 - len(new_sale_items)):
                new_sale_items.append(null_item)
        self.char['for_sale'] = new_sale_items

    def update_item_types(self):
        for item in self.get_all_items():
            if item['item_type'] == 'weapon':
                if self.char['weapon'] not in self.get_all_items():
                    self.char['weapon'] = item
            elif item['item_type'] == 'consumable':
                if self.char['consumable'] not in self.get_all_items():
                    self.char['consumable'] = item
            elif item['item_type'] == 'misc':
                if self.char['misc'] not in self.get_all_items():
                    self.char['misc'] = item
            else:
                pass

    def get_health(self):
        return self.char['health']

    def change_health(self, health_change, change_type="relative"):
        if change_type is 'relative':
            self.char['health'] += health_change
            if self.char['health'] <= 0:
                self.char['health'] = 0
                self.die()
            elif self.char['health'] > 100:
                self.char['health'] = 100
        elif change_type is 'absolute':
            self.char['health'] = health_change
        else:
            pass

    def die(self):
        self.change_event_id('100018')


    # REQUIREMENTS METHODS


    def has_item(self, name):
        for item in self.get_all_items():
            if item['name'] == name:
                return (True, "")
        return (False, "Requires {}".format(name))

    def has_item_type(self, item_type):
        if self.char[item_type]['name'] == 'None':
            if item_type == "misc":
                return (False, "Requires a misc item")
            return (False, "Requires a {}".format(item_type))
        return (True, "")

    def has_specific_item(self, full_name):
        for item in self.get_all_items():
            if item['full_name'] == full_name:
                return (True, "")
        return (False, "Requires {}".format(full_name))

    def has_enough_gold(self, gold_amount):
        if self.char['gold'] < gold_amount:
            return (False, "Requires {} gold".format(gold_amount))
        return (True, "")

    def can_buy_store_item(self, index):
        cost = self.region['local']['items'][index]['price']
        return self.has_enough_gold(cost)

    def has_sale_item(self, index):
        if self.char['for_sale'][index]['name'] == "None":
            return (False, "Requires an item")
        else:
            return (True, "")

    def custom_requirement(self, requirement):
        return (False, requirement)
