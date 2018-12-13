import os
import sys
import json
import facebook
import requests
import numpy as np

curr_dir = os.path.dirname(os.path.realpath(__file__))
base_dir = os.path.normpath(os.path.join(curr_dir, '..'))
env_path = os.path.join(base_dir, 'env.json')
img_path = os.path.join(curr_dir, 'image.png')
sys.path.append(base_dir)

from data.data import DataAccess
from resources.resources import ResourceAccess
from gen.entity import EntityCreator

resourceAccess = ResourceAccess()

entityGen = EntityCreator(resourceAccess)

dataAccess = DataAccess(entityGen)
dataAccess.readdata()

env = json.loads(open(env_path).read())
page_id = env['page_id']
acstoke = env['page_token']
graph = facebook.GraphAPI(access_token=acstoke)

vr = {"LOVE": 0,
      "HAHA": 1,
      "WOW": 2,
      "SAD": 3,
      "ANGRY": 4}

post_id = dataAccess.get_post_id()

if len(sys.argv) > 1:
    select_index = int(sys.argv[1])
else:
    data = graph.get_object(id=post_id, fields="reactions")

    results = dict()
    for react in data['reactions']['data']:
        react_type = react['type']
        theme = vr[react_type]
        results[theme] = results.get(theme, 0) + 1

    items = list(results.values())
    keys = list(results.keys())
    select_index = keys[items.index(max(items))]



current_event = dataAccess.get_current_event()
requirements = current_event['requirements']
if select_index >= len(current_event['action_s']):
    select_index = 0
elif requirements[select_index] is not "":
    select_index = 0
select_action = current_event['action_s'][select_index]
select_result_prob = current_event['result_prob'][select_index]

possible_results = current_event['result_s'][select_index]

result_index = np.random.choice(len(possible_results), p=select_result_prob)
select_result = possible_results[result_index]
select_conseq = current_event['conseq'][select_index][result_index]

event_results = dict(event_s=current_event['event_s'],
                     action_s=select_action,
                     result_s=select_result,
                     strings=current_event['strings'])

dataAccess.change_previous_event(event_results)

gen = current_event['gen']
spec = current_event['spec']

for command in select_conseq:
            exec('dataAccess.' + command)

dataAccess.savedata()


