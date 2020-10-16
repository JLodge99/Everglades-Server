## Static Imports
import os
import importlib
import gym
import gym_everglades
import pdb
import sys

import numpy as np

from everglades_server import server
from everglades_server import generate_map

## Input Variables
# Agent files must include a class of the same name with a 'get_action' function
# Do not include './' in file path
if len(sys.argv) > 1:
    agent0_file = 'agents/' + sys.argv[1]
else:
    agent0_file = 'agents/random_actions'
    
if len(sys.argv) > 2:
    agent1_file = 'agents/' + sys.argv[2]
else:
    agent1_file = 'agents/random_actions'

if len(sys.argv) > 3:
    map_name = sys.argv[3] + '.json'
else:
    map_name = 'RandomMap.json'

if map_name == 'RandomMap.json':
    generate_map.exec(7)
    
config_dir = '/everglades/config/'  
map_file = config_dir + map_name
setup_file = config_dir + 'GameSetup.json'
unit_file = config_dir + 'UnitDefinitions.json'
output_dir = '/everglades/game_telemetry/'

debug = 1

## Specific Imports
agent0_name, agent0_extension = os.path.splitext(agent0_file)
agent0_mod = importlib.import_module(agent0_name.replace('/','.'))
agent0_class = getattr(agent0_mod, os.path.basename(agent0_name))

agent1_name, agent1_extension = os.path.splitext(agent1_file)
agent1_mod = importlib.import_module(agent1_name.replace('/','.'))
agent1_class = getattr(agent1_mod, os.path.basename(agent1_name))

## Main Script
env = gym.make('everglades-v0')
players = {}
names = {}

players[0] = agent0_class(env.num_actions_per_turn, 0, map_name)
names[0] = agent0_class.__name__
players[1] = agent1_class(env.num_actions_per_turn, 1, map_name)
names[1] = agent1_class.__name__

observations = env.reset(
        players=players,
        config_dir = config_dir,
        map_file = map_file,
        unit_file = unit_file,
        output_dir = output_dir,
        pnames = names,
        debug = debug
)

actions = {}

## Game Loop
done = 0
while not done:
    if debug:
        env.game.debug_state()

    for pid in players:
        actions[pid] = players[pid].get_action( observations[pid] )

    observations, reward, done, info = env.step(actions)

print(reward)
