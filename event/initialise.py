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

dataAccess.event = {"current_event": {}, "previous_event": {"event_s": "Starting Event", "action_s": "Wake up", "result_s": "You wake up with a headache in the middle of an open field.\n\nYou aren't sure of where you are, but there are a wooden sword and shield next to you.\n\nYou only remember that your name is {}.\n\n(You are now free to explore the world)".format(name), "strings": {"character": [name]}}, "action_choice": 0, "post_id": "", "next_event": "None", "prob": {"100000": 10, "100001": 10, "100002": 10, "100003": 10, "100004": 10, "100007": 100, "100008": 100, "100009": 100, "100010": 100, "100011": 100, "100012": 100, "100014": 20, "100015": 10, "100016": 10, "100018": 10, "100019": 10, "100020": 5, "100021": 20, "100022": 10, "100023": 10, "100024": 5, "100025": 5, "100035": 10, "100036": 5}}

default_sale_item = dict(name="None",
                         adjective="",
                         full_name="None",
                         type="item")

wooden_sword = dict(name="Wooden sword",
                    adjective="",
                    full_name="Wooden sword",
                    type="item")

wooden_shield = dict(name="Wooden shield",
                    adjective="",
                    full_name="Wooden shield",
                    type="item")

dataAccess.char = {"name": name, "health": 100, "gold": 50, "inventory": [wooden_sword, wooden_shield], "quest": [], "for_sale": [wooden_sword, wooden_shield, default_sale_item, default_sale_item], "spells": []}

dataAccess.region = {"global": {"outer": area, "inner": area}, "local": area}

dataAccess.savedata()