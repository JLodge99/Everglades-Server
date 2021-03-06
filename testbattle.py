## Static Imports
import os
import importlib
import gym
import gym_everglades
import pdb
import sys
import json

import numpy as np

from everglades_server import server
from everglades_server import generate_map
from everglades_server import generate_3dmap
import testing.target_testing as targetTest

config_dir = os.path.abspath('config')
setup_file = os.path.join(config_dir, "GameSetup.json")
unit_file = os.path.join(config_dir, "UnitDefinitions.json")
output_dir = os.path.abspath('game_telemetry')

debug = 0

with open(setup_file) as fid:
    gamesetup = json.load(fid)

########################################################################################################
## Input Variables
# Agent files must include a class of the same name with a 'get_action' function
# Read in from config/GameSetup.json
agent0_file = 'agents/' + gamesetup['Agents'][0]
agent1_file = 'agents/' + gamesetup['Agents'][1]

# Read in from config/GameSetup.json
mapType = gamesetup['MapType']
map_name = gamesetup['MapFile']
wind = gamesetup['enableWind']

map_file = os.path.join(config_dir, map_name)
########################################################################################################

# Recommended settings for weight
# Bellcurve Enable:   Weightinit should be .3 - .9
# Bellcurve Disable:  Weightinit should be .1 - .3
if mapType == '2D':
    print("Generating 2D map")
    generate_map.exec(3)
elif mapType == '3D':
    print("Generating 3D map")
    generate_3dmap.exec(5, 5, 10, weight=.3, bellcurve=False)

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