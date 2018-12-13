import os
import sys
import json

curr_dir = os.path.dirname(os.path.realpath(__file__))
base_dir = os.path.normpath(os.path.join(curr_dir, '..'))
sys.path.append(base_dir)

from data.data import DataAccess
from resources.resources import ResourceAccess
from gen.entity import EntityCreator

resourceAccess = ResourceAccess()

entityGen = EntityCreator(resourceAccess)

dataAccess = DataAccess(entityGen)
dataAccess.readdata()

if len(sys.argv) > 1:
    next_event_id = sys.argv[1]
else:
    next_event_id = dataAccess.get_next_event_id()
location_type = dataAccess.get_location_type()
event_probs = dataAccess.get_event_probs()

event = resourceAccess.get_event(location_type, next_event_id, event_probs)
gen = entityGen.gen_event_entities(event['gen'])

requirements = dataAccess.check_requirements(event['requirements'])

formatted_event = dataAccess.format_event(event, gen)
formatted_event['conseq'] = event['conseq']
formatted_event['result_prob'] = event['result_prob']
formatted_event['spec'] = event['spec']
formatted_event['gen'] = gen
formatted_event['requirements'] = requirements

dataAccess.change_current_event(formatted_event)
dataAccess.savedata()

