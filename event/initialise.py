import os
import sys
import json
import numpy as np

curr_dir = os.path.dirname(os.path.realpath(__file__))
base_dir = os.path.normpath(os.path.join(curr_dir, '..'))
sys.path.append(base_dir)

from data.data import DataAccess
from resources.resources import ResourceAccess
from gen.entity import EntityCreator

resourceAccess = ResourceAccess()

entityGen = EntityCreator(resourceAccess)

dataAccess = DataAccess(entityGen)

area = entityGen.gen_open()

name = sys.argv[1]

dataAccess.event = {"current_event": {}, "previous_event": {"event_s": "Starting Event", "action_s": "Wake up", "result_s": "You wake up with a headache in the middle of an open field.\n\nYou aren't sure of where you are, but there are a wooden sword and shield next to you. For some reason, you also have a knife in your hand.\n\nYou only remember that your name is {}.\n\n(You are now free to explore the world)".format(name), "strings": {"character": [name]}}, "action_choice": 0, "post_id": "", "next_event": "None", "prob": {"100001": 10, "100002": 10, "100003": 10, "100004": 10, "100007": 100, "100008": 100, "100009": 100, "100010": 100, "100011": 100, "100012": 100, "100014": 20, "100015": 10, "100016": 10, "100018": 10, "100019": 10, "100020": 5, "100021": 20, "100022": 10, "100023": 10, "100024": 5, "100025": 5, "100035": 10, "100036": 5, "100045": 10, "100057": 15, "100063": 10}}

null_item = dict(name="None",
                 adjective="",
                 full_name="None",
                 price=0,
                 shop_desc="None",
                 type="item")

wooden_sword = dict(name="Wooden sword",
                    adjective="",
                    item_type="weapon",
                    full_name="Wooden sword",
                    price=3,
                    shop_desc="Wooden sword (3g)",
                    type="item")

wooden_shield = dict(name="Wooden shield",
                    adjective="",
                    item_type="misc",
                    full_name="Wooden shield",
                    price=2,
                    shop_desc="Wooden shield (2g)",
                    type="item")

trusty_knife = dict(name="Knife",
                    adjective="Trusty ",
                    full_name="Trusty Knife",
                    price=5,
                    shop_desc="Trusty Knife (5g)",
                    item_type="weapon",
                    type="item")

dataAccess.char = {"name": name, "health": 100, "gold": 50, "inventory": [wooden_sword, wooden_shield], "quest": [trusty_knife], "for_sale": [wooden_sword, wooden_shield, null_item, null_item], "weapon": wooden_sword, "consumable": null_item, "misc": wooden_shield, "spells": []}

dataAccess.region = {"global": {"outer": area, "inner": area}, "local": area}

dataAccess.savedata()