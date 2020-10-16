import os
import numpy as np
import time
import json

class random_actions:
    def __init__(self, action_space, player_num, map_name):
        self.action_space = action_space
        self.num_groups = 12
        
        with open('/everglades/config/' + map_name) as fid:
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
        self.unit_config = {
            0: [('controller',1), ('striker', 4), ('recon', 1)],# 6
            1: [('controller',2), ('striker', 2), ('tank', 3), ('recon', 2)],# 15
            2: [('tank', 5)],# 20
            3: [('controller', 2), ('tank', 1), ('recon', 3)],# 26
            4: [('striker', 5), ('recon', 5)],# 36
            5: [('controller', 3), ('striker', 2), ('recon', 1)],# 42
            6: [('striker', 3), ('recon', 1)],# 46
            7: [('controller', 1), ('striker', 2), ('tank', 2), ('recon', 1)],# 52
            8: [('controller', 1), ('recon', 2)],# 55
            9: [('controller', 1), ('striker', 3), ('recon', 2)],# 61
            10: [('striker', 9)],# 70
            11: [('controller', 10), ('striker', 8), ('tank', 2), ('recon', 10)],# 100
        }

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

    def get_action(self, obs):
        #print('!!!!!!! Observation !!!!!!!!')
        #print(obs)
        #print(obs[0])
        #for i in range(45,101,5):
        #    print(obs[i:i+5])
        #print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        action = np.zeros(self.shape)
        action[:, 0] = np.random.choice(self.num_groups, self.num_actions, replace=False)
        action[:, 1] = np.random.choice(self.nodes_array, self.num_actions, replace=False)
        #print(action)
        return action


