import os
import sys
import json
import numpy as np
import random
from PIL import ImageFont

curr_dir = os.path.dirname(os.path.realpath(__file__))
base_dir = os.path.normpath(os.path.join(curr_dir, '..'))
sys.path.append(base_dir)


class ResourceAccess:

    def __init__(self):
        eventlist_path = os.path.join(curr_dir, 'eventlist.json')
        adjs_path = os.path.join(curr_dir, 'adjs.json')
        names_path = os.path.join(curr_dir, 'names.json')
        nouns_path = os.path.join(curr_dir, 'nouns.json')
        verbs_path = os.path.join(curr_dir, 'verbs.json')
        words_path = os.path.join(curr_dir, 'words.json')
        syllables_path = os.path.join(curr_dir, 'syllables.json')
        textcolors_path = os.path.join(curr_dir, 'textcolors.json')
        items_path = os.path.join(curr_dir, 'items.json')
        self.font_path = os.path.join(curr_dir, 'font', 'IBM_VGA8.ttf')

        self.eventlist = json.loads(open(eventlist_path).read())
        self.adjs = json.loads(open(adjs_path).read())
        self.names = json.loads(open(names_path).read())
        self.nouns = json.loads(open(nouns_path).read())
        self.verbs = json.loads(open(verbs_path).read())
        self.words = json.loads(open(words_path).read())
        self.syllables = json.loads(open(syllables_path).read())
        self.textcolors = json.loads(open(textcolors_path).read())
        self.items = json.loads(open(items_path).read())

    def get_font(self, size):
        return ImageFont.truetype(font=self.font_path, size=64)

    def get_event(self, location_type, eventid, prob):
        if eventid is None:
            return self.get_random_event(location_type, prob)
        else:
            return self.get_specific_event(eventid)

    def get_random_event(self, location_type, prob):
        check_location = lambda x: x['location_type'] == location_type
        events = list(filter(check_location, self.eventlist))
        ids = [dic['id'] for dic in events]
        probs = [prob.get(str(x), 0) for x in ids]
        probs = np.array(probs) / sum(probs)
        return np.random.choice(events, p=probs)

    def get_specific_event(self, eventid):
        check_id = lambda x: x['id'] == eventid
        events = list(filter(check_id, self.eventlist))
        return events[0]

    def get_name(self, name_type, **kwargs):
        name = "a"*30
        while len(name) > 29:
            if name_type in ['character']:
                name = random.choice(self.names)
            elif name_type in ['open']:
                name = self.get_open_name()
            elif name_type in ['town']:
                name = self.get_town_name()
            elif name_type in ['shop']:
                owner = kwargs["owner"]
                name = self.get_shop_name(owner)
            elif name_type in ['tavern']:
                name = self.get_tavern_name()
            elif name_type in ['church']:
                name = self.get_church_name()
            elif name_type in ['school']:
                name = self.get_school_name()
            elif name_type in ['dungeon']:
                name = self.get_dungeon_name()
            else:
                name = "Not working time"
        return name

    def get_open_name(self):
        noun = random.choice(self.nouns).capitalize()
        adj = random.choice(self.adjs).capitalize()
        word = random.choice(self.words['open'])
        if noun[-1] == 's' or noun[-2:-1] == 'sh':
            return "The {} of {} {}es".format(word, adj, noun)
        elif noun[-1] == 'y':
            return "The {} of {} {}ies".format(word, adj, noun[:-1])
        else:
            return "The {} of {} {}s".format(word, adj, noun)

    def get_town_name(self):
        num_syll = random.randint(2, 4)
        name_syll = random.choices(self.syllables, k=num_syll)
        return "".join(name_syll).capitalize()

    def get_tavern_name(self):
        noun = random.choice(self.nouns).capitalize()
        adj = random.choice(self.adjs).capitalize()
        return "The {} {}".format(adj, noun)

    def get_school_name(self):
        noun = random.choice(self.nouns).capitalize()
        adj = random.choice(self.adjs).capitalize()
        word = random.choice(self.words['school'])
        if noun[-1] == 's' or noun[-2:-1] == 'sh':
            return "{} for {} {}es".format(word, adj, noun)
        elif noun[-1] == 'y':
            return "{} for {} {}ies".format(word, adj, noun[:-1])
        else:
            return "{} for {} {}s".format(word, adj, noun)

    def get_shop_name(self, owner):
        name = owner['name']
        noun = random.choice(self.nouns).capitalize()
        adj = random.choice(self.adjs).capitalize()
        if noun[-1] == 's' or noun[-2:-1] == 'sh':
            return "{}'s {} {}es".format(name, adj, noun)
        elif noun[-1] == 'y':
            return "{}'s {} {}ies".format(name, adj, noun[:-1])
        else:
            return "{}'s {} {}s".format(name, adj, noun)

    def get_church_name(self):
        noun = random.choice(self.nouns).capitalize()
        adj = random.choice(self.adjs).capitalize()
        word = random.choice(self.words['church'])
        name = "{} of the {} {}".format(word, adj, noun)
        return name

    def get_dungeon_name(self):
        noun = random.choice(self.nouns).capitalize()
        adj = random.choice(self.adjs).capitalize()
        word = random.choice(self.words['dungeon'])
        return "{} of the {} {}".format(word, adj, noun)

    def get_item_name(self):
        items = self.items['items']
        probs = [item['prob'] for item in items]
        probs = np.array(probs) / sum(probs)
        return np.random.choice(items, p=probs)

    def get_item_name_of_type(self, item_type):
        check_type = lambda x: x['item_type'] == item_type
        items = list(filter(check_type, self.items['items']))
        probs = [item['prob'] for item in items]
        probs = np.array(probs) / sum(probs)
        return np.random.choice(items, p=probs)

    def get_item_adjective(self):
        item_adjectives = self.items['adjectives']
        probs = [item['prob'] for item in item_adjectives]
        probs = np.array(probs) / sum(probs)
        return np.random.choice(item_adjectives, p=probs)

    def get_item(self, item_type=None):
        if item_type is None:
            name = self.get_item_name()
        else:
            name = self.get_item_name_of_type(item_type)
        adj = self.get_item_adjective()
        return dict(name=name['name'],
                    price=max(1, name['price']+adj['mod']),
                    adjective=adj['adjective'],
                    item_type=name['item_type'],
                    type='item')


    def get_textcolor(self, text_type):
        return tuple(self.textcolors[text_type])

    def get_textcolors(self):
        return self.textcolors