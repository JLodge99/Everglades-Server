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
from everglades_server import generate_3dmap

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

# Choose which map you want by setting map_name.
# To enable wind go to server.py and in the init() for EvergladesGame set self.enableWind = 1
# ********WARNING - ENABLING BOTH 3DMAP AND WIND WILL BREAK THE SERVER.***********
# 3dmap.json     -  3D
# RandomMap.json -  2D

map_name = '3dmap.json'
#map_name = 'RandomMap.json'

if map_name == 'RandomMap.json':
    print("Generating 2D map")
    generate_map.exec(7)
elif map_name == '3dmap.json':
    print("Generating 3D map")
    generate_3dmap.exec(5, 5, 7) #(X, Y, Z)

config_dir = os.path.abspath('config')
map_file = os.path.join(config_dir, map_name)
setup_file = os.path.join(config_dir, "GameSetup.json")
unit_file = os.path.join(config_dir, "UnitDefinitions.json")
output_dir = os.path.abspath('game_telemetry')

debug = 0

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
        setup_file = setup_file,
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
    #print("ACTIONS: ", actions)
    for pid in players:
        actions[pid] = players[pid].get_action( observations[pid] )

    observations, reward, done, info = env.step(actions)
print("Reward: ", reward)
