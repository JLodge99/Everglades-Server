## Static Imports
import os
import importlib
import gym
import gym_everglades
import pdb
import sys
import random
import json
import pytest
import numpy as np

from everglades_server import server
from everglades_server import generate_map
from everglades_server import generate_3dmap

# TODO Change this so that it's using the agent Jerold made for the test script
agent0_file = 'agents/random_actions'
agent1_file = 'agents/random_actions'

## Specific Imports
agent0_name, agent0_extension = os.path.splitext(agent0_file)
agent0_mod = importlib.import_module(agent0_name.replace('/','.'))
agent0_class = getattr(agent0_mod, os.path.basename(agent0_name))
agent1_name, agent1_extension = os.path.splitext(agent1_file)
agent1_mod = importlib.import_module(agent1_name.replace('/','.'))
agent1_class = getattr(agent1_mod, os.path.basename(agent1_name))
config_dir = os.path.abspath('config')

# Choose which map you want by setting map_name.
# To enable wind go to server.py and in the init() for EvergladesGame set self.enableWind = 1
# ********WARNING - ENABLING BOTH 3DMAP AND WIND WILL BREAK THE SERVER.***********
# 3dmap.json     -  3D
# RandomMap.json -  2D

def createSetupJson(map_name, mapType, wind):
    gamesetup = {}
    gamesetup["__type"] = "Setup"
    gamesetup["MapFile"] = map_name
    gamesetup["MapType"] = mapType
    gamesetup["Agents"] = ["random_actions.py", "random_actions.py"]
    gamesetup["UnitFile"] = "UnitDefinitions.json"
    gamesetup["PlayerFile"] = "PlayerConfig.json"
    gamesetup["UnitBudget"] = 100
    gamesetup["TurnLimit"] = 150
    gamesetup["CaptureBonus"] = 1000
    gamesetup["enableWind"] = wind
    gamesetup["Stochasticity"] = random.randint(0, 1000)
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

@pytest.mark.parametrize("mapType,wind", [
    ("2D", False),
    ("2D", True),
])
def test_runGame(mapType, wind):
    debug = 1
    # map_name = "Map.json"
    # createSetupJson(map_name, mapType, wind)
    
    map_name = "pytestmap.json"
    createSetupJson(map_name, mapType, wind)
    if mapType == '2D':
        print("Generating 2D map")
        generate_map.exec(7)
    elif mapType == '3D':
        print("Generating 3D map")
        generate_3dmap.exec(7, 7, 10)
    elif mapType == 'Static':
        print("Static map specified. No map generated.")

    map_file = os.path.join(config_dir, map_name)
    setup_file = os.path.join(config_dir, "GameSetup.json")
    unit_file = os.path.join(config_dir, "UnitDefinitions.json")
    output_dir = os.path.abspath('game_telemetry')

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
