import os
import sys
import json
import numpy as np
import copy

curr_dir = os.path.dirname(os.path.realpath(__file__))
base_dir = os.path.normpath(os.path.join(curr_dir))
sys.path.append(base_dir)

test_path = os.path.join(curr_dir, 'eventinmaking.json')
eventlist_path = os.path.join(curr_dir, 'resources', 'eventlist.json')

test = json.loads(open(test_path).read())
eventlist = json.loads(open(eventlist_path).read())

# Assert that action_s and result_s are equal length
if len(test['action_s']) != len(test['result_s']):
    print("action_s not equal in length to result_s")

if len(test['action_s']) != len(test['conseq']):
    print("action_s not equal in length to conseq")

if len(test['action_s']) != len(test['result_prob']):
    print("action_s not equal in length to result prob")

if len(test['action_s']) != len(test['requirements']):
    print("action_s not equal in length to requirements")

for x, item in enumerate(test['result_s'][:]):
    if len(item) != len(test['conseq'][x]):
        print("result {} has incorrect conseq length".format(x))
    if len(item) != len(test['result_prob'][x]):
        print("result {} has incorrect result_prob length".format(x))

for key, item in test['strings'].items():
    for string in item:
        s = string.replace("\\", "")
        boolean = False
        if s in test['event_s']:
            boolean = True
        for action in test['action_s']:
            if s in action:
                boolean = True
        for resultarray in test["result_s"]:
            for result in resultarray:
                if s in result:
                    boolean = True
        if not boolean:
            print("string does not appear in event:\n{}".format(s))

for x, resultarray in enumerate(test['result_prob']):
    if abs(sum(resultarray) - 1) > 10**(-8):
        print("result array {} does not sum to 1".format(x))


print("event looks good!")