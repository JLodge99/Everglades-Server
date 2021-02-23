import os
import numpy as np
import time
import json
from gym_everglades.envs import everglades_env
from everglades_server import CreateJsonData

class reggtest:
    def __init__(self, action_space, player_num, map_name):
        self.action_space = action_space
        self.num_groups = 12
        config_dir = os.path.abspath('config')
        with open(os.path.join(config_dir, map_name)) as fid:
            self.map_dat = json.load(fid)

        self.nodes_array = []
        for i, in_node in enumerate(self.map_dat['nodes']):
            self.nodes_array.append(in_node['ID'])

        self.num_nodes = len(self.map_dat['nodes'])
        self.num_actions = action_space

        self.shape = (self.num_actions, 2)

        # Types:
        #   0 - Controller
        #   1 - Striker
        #   2 - Tank
        #   3 - Recon
        self.unit_config = CreateJsonData.ConvertLoadoutToObject(player_num)
        print("Successfully loaded player", player_num, "loadout")

        # Recon sensor settings. Format is
        # {Group #: [mode, range, wavelength], ...}
        # Mode is 'active' or 'passive'. Range is
        # an integer of 1, 2, or 3. Wavelength is
        # a string of a decimal between 0.37 and 2.50 inclusive.
        # Wavelength must be of the form 'X.XX'.
        self.sensor_config = {
            0: ['active', 3, '0.38'],
            1: ['active', 3, '0.45'],
            3: ['active', 3, '1.20'],
            4: ['active', 2, '2.30'],
            5: ['active', 3, '0.40'],
            6: ['active', 3, '2.20'],
            7: ['active', 1, '1.13'],
            8: ['active', 3, '1.08'],
            9: ['active', 3, '0.77'],
            11: ['passive', 3]
        }

    # end __init__

    # This is what is determining the actions for the current turn
    def get_action(self, obs):
        action = np.zeros((1,2))
        action[0, 0] = 0 # Group 0
        action[0, 1] = 14 # Node ID 14
        return action