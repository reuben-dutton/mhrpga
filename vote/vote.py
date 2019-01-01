import os
import sys
import json
from PIL import Image, ImageDraw, ImageFont
import textwrap as tw
import facebook
import requests
import numpy as np
import re

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

current_event = dataAccess.get_current_event()
previous_event = dataAccess.get_previous_event()

reacts = ["Love",
          "Haha",
          "Wow",
          "Sad",
          "Angry"]

font_size = 64
font = resourceAccess.get_font(font_size)
f_w, f_h = 32, 48
text_colors = resourceAccess.get_textcolors()
f_c = resourceAccess.get_textcolor('reg')
f_c_choice = resourceAccess.get_textcolor('choice')
f_c_disabled = resourceAccess.get_textcolor('disabled')

margins = (1120, 120)
left_margin = margins[0]
top_margin = 120
image_dim = (3200, 2600)
image_col = (0, 0, 0, 255)

display_dim = (image_dim[0] - sum(margins), image_dim[1] - top_margin)
char_width = display_dim[0] // f_w
char_nlgap = 16

pos = (left_margin, top_margin)

image = Image.new("RGBA", image_dim, color=image_col)
canvas = ImageDraw.Draw(image)

previous_action = " > {}".format(previous_event['action_s'])
previous_result = previous_event['result_s'].split('\n\n')
formatted = []
for item in previous_result:
    formatted.append(tw.fill(item, 
                        width=char_width))
previous_result = "\n\n\n".join(formatted)


current_event_s = current_event['event_s'].split('\n\n')
formatted = []
for item in current_event_s:
    formatted.append(tw.fill(item, 
                        width=char_width))
current_event_s = "\n\n".join(formatted)

requirements = current_event['requirements']

poss_actions = current_event["action_s"][:]
color_poss_actions = current_event["action_s"][:]
disabled_actions = current_event["action_s"][:]

for i in range(len(poss_actions)):
    j = len(poss_actions[i])
    k = len(reacts[i])
    space = " " * (int(display_dim[0]/40) - k)
    if requirements[i] is "":
        poss_actions[i] += ""
        color_poss_actions[i] = space + "({})".format(reacts[i])
        disabled_actions[i] = ""
    else:
        disabled_actions[i] += "\n         ({})".format(requirements[i])
        color_poss_actions[i] = "\n"
        poss_actions[i] += "\n"

construct_text = "\n\n".join([previous_action, previous_result])
dot_length = char_width - 8
space_length = (char_width - dot_length) // 2
filler = "\n" * 3 + " "*(space_length) + "."*dot_length + "\n"*4
construct_text = (filler).join([construct_text, current_event_s])

options = "\n\n   > ".join(poss_actions)
main_text = "\n\n\n   > ".join([construct_text, options])
canvas.text(pos, main_text, font=font, fill=f_c)

for key in text_colors.keys():
    if "gold" not in key:
        font_col = resourceAccess.get_textcolor(key)
        array = current_event['strings'].get(key, []) + \
                previous_event['strings'].get(key, [])
    else:
        array = []
    for item in array:
        if item is not "":
            item = item.replace('(', '\\(')
            item = item.replace(')', '\\)')
            item = item.replace('?', '\\?')
            item = item.replace('.', '\\.')
            item = item.replace('^', '\\^')
            regex = re.compile("\s".join(item.split()))
            text_split = regex.split(main_text)
            new = ""
            for i, match in enumerate(regex.finditer(main_text)):
                new += re.sub(r'\S', ' ', text_split[i])
                new += match.group(0)
            new += re.sub(r'\S', ' ', text_split[len(regex.findall(main_text))])
            canvas.text(pos, new, font=font, fill=font_col)

color_options = "\n\n     ".join(color_poss_actions)
empty_construct_text = re.sub(r'\S', ' ', construct_text)
main_text = "\n\n\n     ".join([empty_construct_text, color_options])
canvas.text(pos, main_text, font=font, fill=f_c_choice)

disabled_options = "\n\n     ".join(disabled_actions)
empty_construct_text = re.sub(r'\S', ' ', construct_text)
main_text = "\n\n\n     ".join([empty_construct_text, disabled_options])
canvas.text(pos, main_text, font=font, fill=f_c_disabled)


expressions = dict(angry=(" ", "\\ /", "__"),
                   neutral=(" ", "_\\_", "__"),
                   puzzled=("?", "~ _", "__"),
                   sad=(" ", "/ \\", "__"),
                   surprised=(" ", "~ ~", "o "),
                   love=("♥", "_ _", "__"))

expr = expressions[np.random.choice(list(expressions.keys()))]

face = """     #####  {}       
    #### {}  ________   
    ##=-[.].]| \\      \\
    #(    _\\ |  |------|
     #   {}| |  |||||||| 
      \\  _/  |  ||||||||
   .--'--'-. |  | ____ | 
  / __      `|__|[o__o]| 
_(____nm_______ /____\\__  \n\n"""

face = face.format(expr[0], expr[1], expr[2])

health = int(dataAccess.get_health() / 5)

healthbar = '[' + '='*health + ' '*(20-health) + '] {}%\n\n\n'
healthbar = healthbar.format(dataAccess.get_health())

location = dataAccess.get_global_location()['name']

char_name = "Name: {}\n\n".format(dataAccess.get_name())
char_gold = "Gold: {}\n\n".format(dataAccess.get_gold())
char_loc = tw.fill("Location: {}".format(location), 26) + '\n\n'

character_info = "".join([char_name, char_gold, char_loc])
character_info += "Inventory: \n\n"

for item in dataAccess.get_all_items():
    name = tw.fill(item['adjective'] + item['name'], 24)
    character_info += " " + name + "\n"

sidebar_text = face + healthbar + character_info

character_pos = (85, 120)
canvas.text(character_pos, sidebar_text, font=font, fill=f_c)

line_coords = [(left_margin-100, 90), (left_margin-100, image_dim[1]-90)]
canvas.line(line_coords, fill=f_c, width=5)

image.save(img_path, 'PNG')

# postid = graph.put_photo(image=open(img_path, 'rb'),
#                           message="Test post, please ignore")["post_id"]

# dataAccess.change_post_id(postid)
# dataAccess.savedata()


if len(sys.argv) > 1:
    text_path = os.path.join(curr_dir, 'text.png')
    image = Image.new("RGBA", image_dim, color=image_col)
    canvas = ImageDraw.Draw(image)
    y = 100
    x = 100
    for key, item in text_colors.items():
        color = tuple(item)
        text = key + ":  abcdefghijklmnopqrstuvwxyz"
        pos = (x, y)
        y += 100
        if y > 2400:
          y = 100
          x = 1650
        canvas.text(pos, text, font=font, fill=color)
    image.save(text_path, 'PNG')