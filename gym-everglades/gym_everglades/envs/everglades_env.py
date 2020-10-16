import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym.spaces import Tuple, Discrete, Box

import everglades_server.server as server

import numpy as np
import pdb


class EvergladesEnv(gym.Env):

    def __init__(self):
        # Game parameters
        self.num_turns = 150
        self.num_units = 100
        self.num_groups = 12
        self.num_nodes = 11
        self.num_actions_per_turn = 7
        self.unit_classes = ['controller', 'striker', 'tank', 'recon']
        
        # Integers are used to represent the unit type (e.g. 0: controller, 1: striker).
        # With 4 types of units, a group containing all 4 would have the maximum value
        # for this part of the observation space. If each unit is designated by index, then
        # this integer would be 3210.
        self.unit_config_high = 3210
        

        # Define the action space
        self.action_space = Tuple((Discrete(self.num_groups), Discrete(self.num_nodes + 1)) * self.num_actions_per_turn)

        # Define the state space
        self.observation_space = self._build_observation_space()

        return

    def step(self, actions):

        scores, status = self.game.game_turn(actions)
        observations = self._build_observations()

        reward = {i:0 for i in self.players}
        done = 0 
        if status != 0:
            done = 1
            if scores[0] != scores[1]:
                reward[0] = 1 if scores[0] > scores[1] else -1
                reward[1] = reward[0] * -1 # flip the sign
            # else reward is 0 for a tie
            print(scores)
        # end status done check
        print(status)

        # return state, reward, done, info
        return observations, reward, done, {}

    def reset(self, **kwargs):
    # kwargs is allowed. https://github.com/openai/gym/blob/master/gym/core.py
        # Get Players
        self.players = kwargs.get('players')
        config_dir = kwargs.get('config_dir')
        map_file = kwargs.get('map_file')
        unit_file = kwargs.get('unit_file')
        output_dir = kwargs.get('output_dir')
        player_names = kwargs.get('pnames')
        self.debug = kwargs.get('debug',False)

        # Input validation
        assert( len(self.players) == 2 ), 'Must have exactly two players' # for now
        self.pks = self.players.keys()
        self.sorted_pks = sorted(self.pks)
        self.player_dat = {}
        for i in self.pks:
            self.player_dat[i] = {}
            
            # This allows individual agents to specify their unit configurations as long as 
            # the agent specifies a dictionary with group number as key and an array of tuples
            #  as values. The tuples consist of ('UnitType', count). The format would be:
            # self.unit_configs = {1: [('Striker', 5), ('Tank', 3)], 2:........}

            # Check if agent provided unit configuration and, if so, use it.
            # If not, use default.
            if hasattr(self.players[i], 'unit_config'):
                self.player_dat[i]['unit_config'] = self.players[i].unit_config
            else:
                self.player_dat[i]['unit_config'] = self._build_groups(i)

            # Get sensor settings from agent if provided
            if hasattr(self.players[i], 'sensor_config'):
                self.player_dat[i]['sensor_config'] = self.players[i].sensor_config
            else:
                self.player_dat[i]['sensor_config'] = {}
            

        # Initialize game
        self.game = server.EvergladesGame(
                config_dir = config_dir,
                map_file = map_file,
                unit_file = unit_file,
                output_dir = output_dir,
                pnames = player_names,
                debug = self.debug
        )
        
        # Initialize players with selected groups
        self.game.game_init(self.player_dat)

        # Get first game state
        observations = self._build_observations()
        #pdb.set_trace()

        return observations

    def render(self, mode='human'):
        pass

    def close(self):
        pass

    def _build_observation_space(self):
        group_low = np.array([1, 0, 0, 0, 0])  # node loc, classes, avg health, in transit, num units rem
        group_high = np.array([self.num_nodes, self.unit_config_high, 100, 1, self.num_units])

        group_state_low = np.tile(group_low, self.num_groups)
        group_state_high = np.tile(group_high, self.num_groups)

        control_point_portion_low = np.array([0, 0, -100, -1])  # is fortress, is watchtower, percent controlled, num opp units
        control_point_portion_high = np.array([1, 1, 100, self.num_units])

        control_point_state_low = np.tile(control_point_portion_low, self.num_nodes)
        control_point_state_high = np.tile(control_point_portion_high, self.num_nodes)

        # Boundaries for the IR sensor observations. The amount of each unit type is the amount that the recon unit has sensed of each
        # unit.
        sensor_low = np.concatenate([np.array([1, 1]), np.tile(0, len(self.unit_classes))]) # source node, target node, amount of each unit type in order of unit_classes indexing (0-controller, 1-striker, etc.)
        sensor_high = np.concatenate([np.array([self.num_nodes, self.num_nodes]), np.tile(self.num_units, len(self.unit_classes))])

        sensor_state_low = np.tile(sensor_low, self.num_groups)
        sensor_state_high = np.tile(sensor_high, self.num_groups)

        observation_space = Box(
            low=np.concatenate([[1], control_point_state_low, group_state_low, sensor_state_low]),
            high=np.concatenate([[self.num_turns + 1], control_point_state_high, group_state_high, sensor_state_high])
        )

        return observation_space


    def _build_groups(self, player_num):
        unit_configs = {}

        num_units_per_group = int(self.num_units / self.num_groups)
        for i in range(self.num_groups):
            unit_type = self.unit_classes[i % len(self.unit_classes)]
            if i == self.num_groups - 1:
                unit_configs[i] = [(unit_type, self.num_units - sum([c[0][1] for c in unit_configs.values()]))]
            else:
                unit_configs[i] = [(unit_type, num_units_per_group)]
        return unit_configs

    def _build_observations(self):
        observations = {}

        for player in self.players:
            board_state = self.game.board_state(player)
            player_state = self.game.player_state(player)
            sensor_state = self.game.sensor_state(player)

            # To make indexing easier
            boardLength = board_state.shape[0]
            playerLength = player_state.shape[0] - 1 # don't need the turn index
            sensorLength = sensor_state.shape[0] - 1 # don't need the turn index

            state = np.zeros(boardLength + playerLength + sensorLength)
            state[0:boardLength] = board_state
            state[boardLength:boardLength + playerLength] = player_state[1:]
            state[boardLength + playerLength:boardLength + playerLength + sensorLength] = sensor_state[1:]

            observations[player] = state

        return observations

# end class EvergladesEnv

if __name__ == '__main__':
    test_env = EvergladesEnv()
