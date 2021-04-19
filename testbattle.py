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

########################################################################################################
## Input Variables
# Agent files must include a class of the same name with a 'get_action' function
# Do not include './' in file path
agent0_file = 'agents/random_actions'
agent1_file = 'agents/random_actions'

# Choose which map you want by setting map_name "3D" or "2D"
mapType = "2D"
map_name = "Map.json"
wind = True
########################################################################################################

# Recommended settings for weight
# Bellcurve Enable:   Weightinit should be .3 - .9
# Bellcurve Disable:  Weightinit should be .1 - .3
if mapType == '2D':
    print("Generating 2D map")
    generate_map.exec(3)
elif mapType == '3D':
    print("Generating 3D map")
    generate_3dmap.exec(5, 5, 10, weight=.4, bellcurve=True)

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

# Create the GameSetup.json
gamesetup = {}
gamesetup["__type"] = "Setup"
gamesetup["MapFile"] = map_name
gamesetup["MapType"] = mapType
# Valid options: target_randomlySelect, target_lowestHealth, target_highestHealth, target_mostLethal, target_callCustomTargeting
gamesetup["Targeting"] = ["target_callCustomTargeting", "target_callCustomTargeting"] #targetTest.targetSystems 
gamesetup["Agents"] = ["random_actions.py", "random_actions.py"]
gamesetup["UnitFile"] = "UnitDefinitions.json"
gamesetup["UnitBudget"] = 100
gamesetup["LoadoutPresetLevel"] = 1 #TODO: Read In
gamesetup["TurnLimit"] = 150
gamesetup["CaptureBonus"] = 1000
gamesetup["enableWind"] = wind
gamesetup["Stochasticity"] = 15054
gamesetup["JammerPenalty"] = 0.75
gamesetup["FocusTurnMin"] = 4
gamesetup["FocusTurnMax"] = 6
gamesetup["FocusHeatMovement"] = 15
gamesetup["FocusHeatCombat"] = 25
gamesetup["FocusHeatCooloff"] = 10
gamesetup["RL_IMAGE_X"] = 600
gamesetup["RL_IMAGE_Y"] = 380
gamesetup["RL_ORTHO_X"] = 12
gamesetup["RL_ORTHO_Y"] = 7
gamesetup["RL_Render_P1"] = 1
gamesetup["RL_Render_P2"] = 0
gamesetup["RL_Render_SaveToDisk"] = 0
gamesetup["SubSocketAddr0"] = "opp-agent"
gamesetup["SubSocketPort0"] = 5556
gamesetup["SubSocketAddr1"] = "agent"
gamesetup["SubSocketPort1"] = 5555
FileO = open(os.path.join(config_dir, "GameSetup.json"), "w")
FileO.write(json.dumps(gamesetup, indent = 4))
FileO.close()

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