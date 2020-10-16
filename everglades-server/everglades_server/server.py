import os
import json
import csv
import datetime
import pdb

import numpy as np
import random as r
import re

from everglades_server.definitions import *
from everglades_server import wind

class EvergladesGame:
    """
    """
    def __init__(self, **kwargs):
        # Get configuration locations
        config_path = kwargs.get('config_dir')
        map_file = kwargs.get('map_file')
        unit_file = kwargs.get('unit_file')
        self.setup_file = config_path + 'GameSetup.json'
        self.debug = kwargs.get('debug', False)
        self.player_names = kwargs.get('pnames')
        self.output_dir = kwargs.get('output_dir')
        #config_file = kwargs.get(

        # Initialize game
        if os.path.exists(map_file):
            self.board_init(map_file)
        elif os.path.exists(config_dir + map_file):
            self.board_init(map_file)
        else:
            # Exit with error
            pass

        if os.path.exists(unit_file):
            self.unitTypes_init(unit_file)
        elif os.path.exists(config_dir + unit_file):
            self.unitTypes_init(unit_file)
        else:
            # Exit with error
            pass

        # Check output directory existance. Create if necessary
        if not os.path.isdir(self.output_dir):
            oldmask = os.umask(000)
            os.mkdir(self.output_dir,mode=0o777)
            os.umask(oldmask)
        assert( os.path.isdir(self.output_dir) ), 'Output directory does not exist \
                and could not be created'


        # Initialize output arrays, to be written to file at game completion
        # Needs the map name to be populated before initialization
        self.output_init()

    def board_init(self,map_file):
        """
        """
        ## Game board initialization
        # Load in map json configuration file
        with open(map_file) as fid:
            self.map_dat = json.load(fid)

        # Load in GameSetup.json file
        with open(self.setup_file) as f:
            self.setup = json.load(f)

        Xsize = self.map_dat['Xsize']
        Ysize = self.map_dat['Ysize']

        # Seed value used for wind Stochasticity from game setup
        windSeed = self.setup['Stochasticity']

        # Positions of every node in board
        nodePos = {}

        # Add positions of every node
        for row in range(0, Xsize):
            for col in range(0, Ysize):
                nodePos[(col + 2) + (Ysize * row)] = (row + 1, col)

        # Initialize maps
        self.evgMap = EvgMap(self.map_dat['MapName'])
        self.evgMap2d = [[-1 for x in range(Xsize + 2)] for y in range(Ysize)]

        self.team_starts = {}
        # Two different types of map keys. Note that they may both be the same
        #   1) Array sorted by index of evgMap node with corresponding node id
        #   2) Array sorted by node id with corresponding index of evgMap node
        self.map_key1 = np.zeros( len(self.map_dat['nodes']), dtype=np.int )
        arrayIDs = []
        # Create the map nodes
        for i, in_node in enumerate(self.map_dat['nodes']):
            # Initialize node
            node = EvgMapNode(
                    ID = in_node['ID'],
                    radius = in_node['Radius'],
                    resource = in_node['Resource'],
                    defense = in_node['StructureDefense'],
                    points = in_node['ControlPoints'],
                    teamStart = in_node['TeamStart']
            )
            if node.teamStart != -1:
                self.team_starts[node.teamStart] = node.ID
            # Add node connections
            for in_conn in in_node['Connections']:
                # Initialize node outbound connections
                conn = EvgNodeConnection(
                        destID = in_conn['ConnectedID'],
                        distance = in_conn['Distance']
                )
                node.connections.append(conn)
                node.connection_idxs.append(conn.destID)
            # end connection creation
            node.connection_idxs = np.array(node.connection_idxs).astype(np.int)
            self.map_key1[i] = in_node['ID']
            # Append node to the map
            self.evgMap.nodes.append(node)
            arrayIDs.append(in_node['ID'])
        # end node creation
        self.map_key2 = np.argsort( self.map_key1 )

        # Recreate game board
        node_num = 1

        for n in self.evgMap.nodes:
            id = n.ID
            if id != 1 and id != (Xsize * Ysize + 2):
                (x,y) = nodePos[id]
                self.evgMap2d[y][x] = node_num
                node_num += 1

        # Add base nodes
        self.evgMap2d[int(Ysize/2)][0] = 0
        self.evgMap2d[int(Ysize/2)][Xsize + 1] = node_num

        # Create wind magnifier dict
        self.winds = wind.exec(self.evgMap2d, Xsize + 2, Ysize, windSeed)

        # Convert p0 nodes numbering to p1
        # Need method to do this when boards are not hand-designed

        array = []

        array.append(Ysize*Xsize + 2)

        #Reverse the node list
        i = Xsize - 1
        while i >= 0:
            j = 0
            while j < Ysize:
                if j + (Ysize * i) + 2 in arrayIDs:
                    array.append(j + (Ysize * i) + 2)
                j = j + 1
            i = i - 1

        array.append(1)

        print(self.map_key1)
        print(array)

        self.p1_node_map = array

        def _convert_node(node_num):
            return self.p1_node_map[list(self.map_key1).index(node_num)]

        self._vec_convert_node = np.vectorize(_convert_node)

        # Fortress defense multiplier for controlling player's units
        # located at the fortress node
        self.fort_bonus = 2
        # Watchtower vision bonus. Extra graph depth of fog of war penetration
        self.watch_bonus = 1


    def unitTypes_init(self,unit_file):
        """
        """
        ## Unit types initialization
        # Load in unit types json configuration file
        with open(unit_file) as fid:
            self.unit_dat = json.load(fid)

        # Initialize unit types
        self.unit_types = []
        uid = 0
        self.unit_ids = {}
        self.unit_names = {}
        for in_type in self.unit_dat['units']:
            # Initialize new unit type
            unit_type = EvgUnitDefinition(
                name = in_type['Name'],
                health = in_type['Health'],
                damage = in_type['Damage'],
                speed = in_type['Speed'],
                control = in_type['Control'],
                cost = in_type['Cost']
            )
            self.unit_types.append(unit_type)
            #pdb.set_trace()
            self.unit_ids[uid] = unit_type.unitType.lower()
            self.unit_names[unit_type.unitType.lower()] = uid
            uid += 1
        # end unit type creation

    def game_init(self, player_dat):
        """
        """

        # Open up connections
        # Wait for two players
        # Assign player numbers
        # Initialize players and units

        self.current_turn = 0
        self.players = {}

        #pdb.set_trace()
        players = list(player_dat.keys())
        # Where to set a random player 0/player 1; here?
        # ...is it even necessary? They both think they start at node 1.
        #np.random.choice(players)
        # Cumulative group ID for output
        map_gid = 1
        # Cumulative unit number for output
        map_units = 1

        # Two lists for displaying unit types and counts for a group for output purposes
        out_count = []
        out_type = []

        for player in players:
            assert(player in self.team_starts), 'Given player number not included in map configuration file starting locations'
            start_node_idx = self.team_starts[player]
            map_node_idx = np.argwhere(self.map_key1 == start_node_idx)[0][0]

            self.players[player] = EvgPlayer(player)

            assert(type(player_dat[player]['unit_config']) is dict), 'Unit configuration must be a dictionary'
            assert(len(player_dat[player]['unit_config']) == 12), 'A player must have 12 groups'

            for i, gid in enumerate(player_dat[player]['unit_config']):
                assert(re.match('^(1[0-1]|[0-9])$', str(gid))), 'Group IDs must be integers 0-11, inclusive'

                newGroup = EvgGroup(
                        groupID = gid,
                        location = start_node_idx,
                        mapGroupID = map_gid
                )

                # Whether there are Recon units in the group. This value updates as the configuration
                # file is checked.
                hasRecon = False

                # Cost counter variable
                counter = 0

                assert(type(player_dat[player]['unit_config'][gid]) is list), 'Group values must be a list'

                # Each group has a list of tuples for their unit_type and amount, so check each tuple
                for pair in player_dat[player]['unit_config'][gid]:
                    assert(type(pair) is tuple), 'Group array must contain tuples'
                    assert(type(pair[0]) is str), 'Unit type must be a string'
                    assert(type(pair[1]) is int), 'Unit count must be an integer'

                    in_type, in_count = pair
                    in_type = in_type.lower()

                    # Input validation
                    assert(in_type in self.unit_names), 'Group type not in unit type config file'
                    assert(in_count <= 100), 'Invalid group size allocation'

                    unit_id = self.unit_names[in_type]

                    # Cost counter to make sure the total unit allocation is correct
                    # Total cost limit was set by multiplying the maximum number of units,
                    # 100, by base cost of 1.
                    counter += (self.unit_types[unit_id].cost * in_count)
                    assert(counter <= 100), 'Total cost cannot exceed 100'

                    newUnit = EvgUnit(
                            unitType = in_type,
                            count = in_count
                    )

                    newGroup.count += in_count

                    # Set each definition field according to unit_types. These are defaults.
                    newUnit.definition.unitType = self.unit_types[unit_id].unitType
                    newUnit.definition.health = self.unit_types[unit_id].health
                    newUnit.definition.damage = self.unit_types[unit_id].damage
                    newUnit.definition.speed = self.unit_types[unit_id].speed
                    newUnit.definition.control = self.unit_types[unit_id].control
                    newUnit.definition.cost = self.unit_types[unit_id].cost

                    # If unit type is Recon, we need to change the speed value to decrease
                    # as the range value increases. An explicit mapping of range to speed would be:
                    # (1, 3), (2, 2), (3, 1). Also, set the mode and range if provided. Default mode
                    # is passive, default range is 1, and default speed is 3.
                    if newUnit.unitType == "recon":
                        hasRecon = True
                        newUnit.wavelength = ""
                        assert(type(player_dat[player]['sensor_config']) is dict), 'Sensor configuration must be a dictionary'

                        if gid in player_dat[player]['sensor_config']:
                            # Check format and values
                            assert(type(player_dat[player]['sensor_config'][gid]) is list), 'Group\'s sensor configuration value must be a list'
                            assert(type(player_dat[player]['sensor_config'][gid][0]) is str), 'Mode must be a string'
                            assert(player_dat[player]['sensor_config'][gid][0] in ('active', 'passive')), 'Mode must be active or passive'
                            assert(type(player_dat[player]['sensor_config'][gid][1]) is int), 'Range must be an integer'
                            assert(1 <= player_dat[player]['sensor_config'][gid][1] <= 3), 'Range must be between 1 and 3, inclusive'

                            newUnit.mode = player_dat[player]['sensor_config'][gid][0]
                            newUnit.range = player_dat[player]['sensor_config'][gid][1]
                            newUnit.definition.speed = 4 - newUnit.range

                            if newUnit.mode == 'active':
                                assert(type(player_dat[player]['sensor_config'][gid][2]) is str), 'Wavelength must be a string'
                                # Wavelength must be of the form X.XX
                                assert(re.match('\d[.]\d\d$',player_dat[player]['sensor_config'][gid][2])), 'Wavelength must be of the form X.XX'
                                assert(0.37 <= float(player_dat[player]['sensor_config'][gid][2]) <= 2.50), 'Wavelength must be between 0.37 and 2.50, inclusive'

                                newUnit.wavelength = str(player_dat[player]['sensor_config'][gid][2])
                        else:
                            newUnit.mode = "passive"
                            newUnit.range = 1

                        sensorString = '[{};{};{};{}]'.format(newUnit.mode,
                                                           newUnit.range,
                                                           newUnit.definition.speed,
                                                           newUnit.wavelength)

                    newGroup.units.append(newUnit)

                    in_type = in_type.capitalize()
                    out_type.append(in_type)
                    out_count.append(in_count)

                    newGroup.speed.append(newUnit.definition.speed)
                    newGroup.mapUnitID.append(map_units)
                    map_units += in_count
                # End Unit loop

                if not hasRecon:
                    sensorString = '[;;;]'

                # Make group.speed[0] the slowest
                newGroup.speed.sort()

                outtype = '[{}]'.format(';'.join(map(str, out_type)))
                mapUnitID = '[{}]'.format(';'.join(map(str, newGroup.mapUnitID)))
                outcount = '[{}]'.format(';'.join(map(str, out_count)))

                # Sensor lags behind current turn
                turn = self.current_turn + 1

                outstr = '{:.6f},{},{},{},{},{},{},{}'.format(turn,
                                                              player,
                                                              map_gid,
                                                              start_node_idx,
                                                              outtype,
                                                              mapUnitID,
                                                              outcount,
                                                              sensorString
                )
                self.output['GROUP_Initialization'].append(outstr)
                map_gid += 1

                # Empty the out_count and out_type lists to be refilled by a new group
                del out_count[:]
                del out_type[:]

                self.players[player].groups.append(newGroup)
                self.evgMap.nodes[map_node_idx].groups[player].append(i)
            # end group loop
        # end player loop
        #pdb.set_trace()

        self.total_groups = map_gid
        self.total_units = map_units
        self.focus = np.random.randint(self.total_groups)
        self.capture()
        self.game_end() # To output initial score for time 0


        return

    def game_turn(self, actions):
        """
        """
        self.current_turn += 1

        ## Apply each player's turn
        #pdb.set_trace()
        for player in self.team_starts:
            if player not in actions:
                print('Player {} not found in input action dictionary'.format(player))
                continue

            action = actions[player]
            # Verify valid shape of action array
            r,c = action.shape[:2]
            assert(c == 2), 'Did not receive 2 columns for player {}s action'.format(player)
            action = action[:7,:] # max 7 actions per turn

            # Verfiy each swarm gets commanded only once
            used_swarms = []
            moves = []
            # group id, node id
            for gid, nid in action.astype(int):
                if player == 1:
                    nid = int( self._vec_convert_node(nid) )
                current_node = self.players[player].groups[gid].location
                map_idx = np.where(self.map_key1 == current_node)[0][0]

                #pdb.set_trace()
                ## Tests
                # Ensure this swarm hasn't been commanded this turn
                test1 = gid not in used_swarms
                # Ensure swarm isn't already in transit
                test2 = self.players[player].groups[gid].moving == False
                # Ensure the new node is connected to the current node
                test3 = False
                for conn in self.evgMap.nodes[map_idx].connections:
                    if conn.destID == nid:
                        test3 = True
                        distance = conn.distance
                        break
                # Ensure group is alive
                test4 = True
                if self.players[player].groups[gid].destroyed == True:
                    test4 = False

                if test1 and test2 and test3 and test4:
                    used_swarms.append(gid)
                    #print('good move')

                    tempMove = MovementTurn()
                    tempMove.currentTurn = self.current_turn
                    tempMove.player = player
                    tempMove.gid = gid
                    tempMove.location = self.players[player].groups[gid].location
                    tempMove.nid = nid

                    moves.append(tempMove)

                    self.players[player].groups[gid].ready = True
                    self.players[player].groups[gid].moving = False
                    self.players[player].groups[gid].travel_destination = nid
                    self.players[player].groups[gid].distance_remaining = distance
            # end action application loop
        # end player loop

        self.combat()

        for move in moves:
            if self.players[move.player].groups[move.gid].destroyed == False:
                    outstr = '{:.6f},{},{},{},{},{}'.format(
                        move.currentTurn,
                        move.player,
                        self.players[move.player].groups[move.gid].mapGroupID,
                        move.location,
                        move.nid,
                        'RDY_TO_MOVE'
                    )
                    self.output['GROUP_MoveUpdate'].append(outstr)

        self.movement()
        self.capture()
        self.build_knowledge_output()

        return self.game_end() # returns scores and status

    def game_end(self):

        # Game end types
        end_states = {}
        end_states['InProgress']   = 0
        end_states['TimeExpired']  = 1
        end_states['BaseCapture']  = 2
        end_states['Annihilation'] = 3
        status = end_states['InProgress']

        scores = {i:0 for i in self.team_starts}
        counts = [0 for i in self.team_starts]
        base_captured = [0 for i in self.team_starts]
        home_loss = {i:0 for i in self.team_starts}
        pids = np.array( list(self.players.keys()) )

        # Add node points to player scores
        for i, node in enumerate(self.evgMap.nodes):
            if (node.teamStart != -1) and \
               (node.controlledBy != -1) and \
               (node.controlledBy != node.teamStart):
                # Extra bonus for capturing the opponent's base
                base_captured[node.teamStart] = 1
                scores[node.controlledBy] += 1000
            if node.controlState != 0:
                # Points for controlling or partially controlling a node
                pid = 0 if node.controlState > 0 else 1
                xer = 2 if np.abs(node.controlState) == node.controlPoints else 1
                points = node.controlPoints if xer == 2 else np.abs(node.controlState)
                scores[pid] += np.abs( points * xer )

        # Add unit points to player scores
        for i, pid in enumerate(self.team_starts):
            for i, group in enumerate(self.players[pid].groups):
                if group.destroyed == False:
                    counts[pid] += np.sum( [i.count for i in group.units] )
                    scores[pid] += np.sum( [(i.count * i.definition.cost) for i in group.units] )

        ## Check progress
        # Time expiration
        if self.current_turn >= 150:
            status = end_states['TimeExpired']
        # Annihilation
        elif np.sum(counts) == 0:
            status = end_states['Annihilation']
        # Base capture
        elif 1 in base_captured:
            status = end_states['BaseCapture']

        if status != 0:
            outstr = '{:.6f},{},{}'.format(
                    self.current_turn,
                    self.player_names[0],
                    self.player_names[1]
            )
            self.output['PLAYER_Tags'].append(outstr)

        if (self.current_turn % 10 == 0):
            self.focus = np.random.randint(self.total_groups)

        outstr = '{:.6f},{},{},{},{}'.format(
                self.current_turn,
                scores[0],
                scores[1],
                status,
                self.focus
        )
        self.output['GAME_Scores'].append(outstr)

        if status != 0:
            self.write_output()

        return scores, status


    def debug_state(self):
        print('!!!! Turn {} !!!!!!!!!!!!!!!!!!!!!!!!!!!'.format(self.current_turn))
        for i, nidx in enumerate(self.map_key2):
            print('Node {}'.format( self.evgMap.nodes[nidx].ID ) )
            print('\t{}'.format( self.evgMap.nodes[nidx].resource) )
            print('\t% Controlled: {}'.format( self.evgMap.nodes[nidx].controlState ) )

            for i, player in enumerate(self.players):
                counts = []
                cnt = 0
                for gid in self.evgMap.nodes[nidx].groups[i]:
                    if self.players[i].groups[gid].moving == False:
                        cnt += self.players[i].groups[gid].count
                        counts.append(gid)
                print('\tPlayer {} units: {}'.format(i, cnt) )
                for gid in counts:
                    print('\t\ttype: {}'.format([x.unitType for x in self.players[i].groups[gid].units]))
                    print('\t\tavg health: {:.2f}'.format(np.average(np.hstack([x.unitHealth for x in self.players[i].groups[gid].units]))))
                    print('\t\t{}'.format([y for x in self.players[i].groups[gid].units for y in x.unitHealth]))
        print()

    def board_state(self, player_num):
        """
         |  Return the state of the game board. Returned shall be a numpy array
         |  with the following index values:
         |    Index 0
         |        0 : turn number
         |    Indices 1-4: node states. Repeats for number of nodes, starting at 5
         |        1 : boolean 'has fortress bonus'
         |        2 : boolean 'has watchtower bonus'
         |        3 : percent controlled [-100:100] player 0 owned = +, player 1 = -
         |        4 : number of opposing player units
        """
        assert( isinstance(player_num, (int, float)) ), '"player_num" was not a number'
        assert(player_num in self.team_starts), 'Given player number not included in map configuration file starting locations'

        # Only works for two players
        players = np.array( list(self.players.keys()) )
        opp_pid = np.where( players != player_num )[0][0]

        # Build valid indices for fog of war
        if self.debug:
            valid_nodes = [True for i in self.map_key2]
        else:
            # Assume False, prove otherwise
            valid_nodes = [False for i in self.map_key2]

            # Loop through nodes to check for validity
            for i, nidx in enumerate(self.map_key2):
                node = self.evgMap.nodes[nidx]
                if node.controlledBy == player_num:
                    # Always can see nodes you control
                    valid_nodes[i] = True
                    # Can also see connections if it has a watchtower bonus
                    if 'OBSERVE' in node.resource:
                        for j, cid in enumerate(node.connection_idxs):
                            cidx = int(np.squeeze(np.where(self.map_key1 == cid)))
                            valid_nodes[cidx] = True
                else:
                    # Must have active groups in the area to see other nodes
                    for gid in node.groups[player_num]:
                        if self.players[player_num].groups[gid].moving == False:
                            valid_nodes[i] = True
                            break
        # end fog of war masking
        #pdb.set_trace()


        num_nodes = len(self.map_key2)
        state = np.zeros(num_nodes * 4 + 1, dtype = np.int)
        idx = 0
        state[idx] = self.current_turn
        idx += 1
        # Loop through nodes from smallest to largest (hence map_key2)
        for i, nidx in enumerate(self.map_key2):
            # Flip board so both players think they start at 1
            if player_num == 1:
                node_id = self._vec_convert_node(self.map_key1[nidx])
                nidx = int(np.squeeze(np.where(self.map_key1 == node_id)))

            node = self.evgMap.nodes[nidx]
            state[idx] = 1 if 'DEFENSE' in node.resource else 0
            state[idx+1] = 1 if 'OBSERVE' in node.resource else 0
            state[idx+2] = node.controlState

            for gid in node.groups[opp_pid]:
                group = self.players[opp_pid].groups[gid]
                for unit in group.units:
                    state[idx+3] += unit.count

            idx += 4
        # end per-node state build
        # pdb.set_trace()


        return state

    def player_state(self, player_num):
        """
         |  Return the state of the player's groups. Return shall be a numpy array
         |  with the following index values:
         |    Index 0
         |        0 : turn number
         |    Indices 1-5: node states. Repeats for number of nodes, starting at 6
         |        1 : location as node number (int)
         |        2 : unit types
         |        3 : average group health [0-100]
         |        4 : boolean 'is group moving'
         |        5 : number of units alive (int)
        """
        player = self.players[player_num]
        state = np.zeros( len(player.groups) * 5 + 1, dtype = np.int)
        idx = 0
        state[idx] = self.current_turn
        idx += 1
        for group in player.groups:
            # Build unit statistics
            units_alive = 0
            health = 0
            unit_types = []
            for unit in group.units:
                units_alive += np.sum( unit.unitHealth > 0 )
                health += np.sum( unit.unitHealth )
                unit_types.append(self.unit_names[unit.unitType.lower()])

            location = group.location
            # Flip board so both players think they start at 1
            if player_num == 1:
                location = int( self._vec_convert_node(location) )

            state[idx] = location

            # Remember that self.unit_names is an integer corresponding with the unit type
            # 0 - Controller, 1 - Striker, 2 - Tank, etc.
            # For player state, the group's unit composition needs to be a single integer representation
            # Unit types should be in descending order to preserve any zeros
            unit_types.sort(reverse = True)

            # Convert the list to a string and then to an integer
            unit_types = int(''.join([str(digit) for digit in unit_types]))
            # Fixed to allow mixed units
            state[idx+1] = unit_types
            state[idx+2] = (health * 1.) / units_alive if (units_alive > 0) else 0
            state[idx+3] = 1 if group.moving else 0
            state[idx+4] = units_alive

            idx += 5
        # end per-group state build

        if player_num == 2:
            pdb.set_trace()

        return state


    def sensor_state(self, player_num):
        """
         |  Return the state of the player's IR sensors. Return shall be a numpy array
         |  with the following index values:
         |    Index 0
         |        0 : turn number
         |    Indices 1-N: sensed units. Repeats for N number of groups
         |        1 : source location as node number (int)
         |        2 : destination location as a node number (int)
         |        Within each group, after the first two elements, the amount of each unit type that was sensed.
         |        Currently:
         |        3 : amount of controllers [0-100]
         |        4 : amount of strikers [0-100]
         |        5 : amount of tanks [0-100]
         |        6 : amount of recons [0-100]
        """
        player = self.players[player_num]

        # Get enemy player ID. Only works with two players of IDs 0 and 1
        if (player_num):
            enemy_num = 0
        else:
            enemy_num = 1

        enemyPlayer = self.players[enemy_num]

        # A dictionary with tuple keys representing source and destination node IDs. The
        # values are a list of the sensed enemy unit counts [controller, striker, tank, recon]
        # with those source and destination nodes. This will be used to construct the final output.
        # Note that if a group was sensed, but not the unit, the count for that unit in the list will be zero.
        sensedUnits = {}
        # A dictionary with group IDs as the key and tuples of (node.ID, node.ID) as values.
        groupNodes = {}

        # Collect groupIDs that contain recon units, their locations, and their destinations.
        for group in player.groups:
            for unit in group.units:
                if unit.unitType == 'recon' and unit.count > 0:
                    groupNodes[group.groupID] = (group.location, group.travel_destination)

        # Loop through enemy player's groups
        for enemyGroup in enemyPlayer.groups:
            # Can only sense enemy groups that are moving
            if enemyGroup.moving == True:

                # If group is flagged as moving but only RDY_TO_MOVE, change ready to False and continue
                if enemyGroup.ready == True:
                    enemyGroup.ready = False
                    continue

                # Is the enemyGroup sensed?
                groupSensed = False
                # Are the recon units in the group sensed at any distance because they are in active mode?
                reconSensed = False

                # An array to hold the count of units in the enemyGroup
                enemyUnits = np.zeros(len(self.unit_types), dtype=int)
                # The mode of the recon unit(s). If there are no recon units, default will be "none".
                enemyMode = "none"
                # Loop through the  enemyGroup's units to fill the enemyUnits array
                for unit in enemyGroup.units:
                    enemyUnits[self.unit_names[unit.unitType]] = unit.count
                    # While looping, get the mode of the recon unit(s) if any
                    if unit.unitType == 'recon':
                        enemyMode = unit.mode

                # Find the enemy group's location and destination nodes
                sourceID = enemyGroup.location
                destinationID = enemyGroup.travel_destination

                # Get the index of the nodes with the source and destination IDs
                for index, nodeID in enumerate(self.map_key1):
                    if nodeID == sourceID:
                        sourceIndex = index
                for index, nodeID in enumerate(self.map_key1):
                    if  nodeID == destinationID:
                        destIndex = index

                # Default values for player's mode and range. These will be changed if there is a recon
                # unit that can detect the enemy group.
                sensorMode = "none"
                sensorRange = 0

                # Check if the enemyGroup is travelling between two nodes that the player's group
                # is also between or if the enemyGroup has recons in active mode that can be sensed.
                # We must also check if the player's group is travelling the other direction.
                for groupID in groupNodes:
                    # Get the group's recon unit's range and mode.
                    for unit in player.groups[groupID].units:
                        if unit.unitType == 'recon':
                            tempMode = unit.mode
                            sensorRange = unit.range

                    # Check if the enemy group has recon units in active mode and if they can be sensed
                    if enemyMode == "active" and (player.groups[groupID].location == sourceID or
                                                    player.groups[groupID].location == destinationID):
                        reconSensed = True
                        if sensorMode != "active":
                            sensorMode = tempMode

                    # If we are in 'active' mode and have detected the enemy group, we have detected all the enemy group's
                    # units and can break.
                    if groupSensed and sensorMode == "active":
                        break

                    # If this occurs, the enemy group is travelling the same direction.
                    if (sourceID, destinationID) == groupNodes[groupID]:
                        # Check that the enemy group is in sensor range. If so, we have sensed the enemy group using
                        # this group's recon unit(s) sensor mode.
                        if abs(player.groups[groupID].distance_remaining - enemyGroup.distance_remaining) <= sensorRange:
                            groupSensed = True
                            sensorMode = tempMode

                    # If this occurs, the enemy group is travelling the opposite direction.
                    if (destinationID, sourceID) == groupNodes[groupID]:
                        # Check that the enemy group is in sensor range. This is more difficult because the 'to' and 'from' travel paths
                        # are not necessarily the same length. Thus, a mean travel path length will be used to calculate whether
                        # the enemy's group is in range.

                        # Connection_idxs are one-indexed while the node array is zero-indexed. So account
                        # for that.
                        for index, connectionID in enumerate(self.evgMap.nodes[sourceIndex].connection_idxs):
                            if connectionID == destinationID:
                                path1Length = self.evgMap.nodes[sourceIndex].connections[index].distance
                        for index, connectionID in enumerate(self.evgMap.nodes[destIndex].connection_idxs):
                            if connectionID == sourceID:
                                path2Length = self.evgMap.nodes[destIndex].connections[index].distance
                        avgLength = (path1Length + path2Length)/2

                        if abs(avgLength - (player.groups[groupID].distance_remaining + enemyGroup.distance_remaining)) <= sensorRange:
                            groupSensed = True
                            sensorMode = tempMode

                # Decide which unit counts from the enemyUnits array are going to be needed according to the above information
                # If we sensed anything, add to the sensedUnits dictionary.
                if groupSensed or reconSensed:
                    sensedUnits[(enemyGroup.location, enemyGroup.travel_destination)] = np.zeros(len(enemyUnits))

                    # Loop through the enemyUnits array. Works with current configuration of [controller, striker, tank, recon].
                    for index, count in enumerate(enemyUnits):
                        # If we are in passive mode, only conrollers and strikers are sensed, unless we detected some enemy
                        # recons that were in active mode.
                        if sensorMode == "passive":
                            if index == 0 or index == 1:
                                sensedUnits[(enemyGroup.location, enemyGroup.travel_destination)][index] = count
                            if index == 3 and reconSensed:
                                sensedUnits[(enemyGroup.location, enemyGroup.travel_destination)][index] = count

                        # If we are in active mode, all unit types are sensed
                        if sensorMode == "active":
                            sensedUnits[(enemyGroup.location, enemyGroup.travel_destination)][index] = count

        # Build up sensor_state output
        state = np.zeros( ((2 + len(self.unit_types)) * len(self.players[enemy_num].groups)) + 1)
        state[0] = self.current_turn
        index = 1

        # Parse sensedUnits entries to create state output
        for key in sensedUnits:
            # Player 0 gets nodes as-is.
            if player_num == 0:
                state[index] = key[0] # the enemy group's source node
                state[index + 1] = key[1] # the enemy group's destination node
            # Flip board so second player thinks they start at 1
            if player_num == 1:
                state[index] = int( self._vec_convert_node(key[0] ) )
                state[index + 1] = int( self._vec_convert_node(key[1] ) )
            # Loop through each unit type to access their index in the sensedUnits entry
            for i in range(2, (len(self.unit_types) + 2)):
                state[index + i] = int(sensedUnits[key][i - 2]) # controller, striker, tank, recon, ...
            index += 6

            # This telemetry output was not necessary, but included to conveniently show sensor
            # data.
            outstr = '{:.6f},{},{},{},[{}]'.format(
                    self.current_turn,
                    player_num,
                    key[0],
                    key[1],
                    ';'.join(str(int(i)) for i in sensedUnits[key])
            )
            self.output['SENSOR_ServerData'].append(outstr)

        #print(state)
        return state


    def combat(self):
        ## Apply combat
        # Combat occurs before movement - a fleeing group could still be within
        # targeting range during the same turn; arriving units need to get
        # bearings before attacking anything.
        all_dmg = {}

        for node in self.evgMap.nodes:
            player_gids = {}
            counts = {}
            tgt_gids = {}
            counts_units = {}

            # Determine which players occupy this node
            for player in self.team_starts:
                #pdb.set_trace()
                if len(node.groups[player]) > 0:
                    player_gids[player] = []
                    counts[player] = []
                    counts_units[player] = {}

                    # Build a list of groups that are available for combat
                    for gid in node.groups[player]:
                        # Discount groups in transit
                        if self.players[player].groups[gid].moving == False:
                            player_gids[player].append(gid)
                            # BUG - if group consists of different units combat is not applied to all
                            count = 0
                            counts_units[player][gid] = []

                            for i, unit in enumerate(self.players[player].groups[gid].units):
                                for j in range(len(unit.unitHealth)):
                                    if unit.unitHealth[j] > 0 :
                                        counts_units[player][gid].append(i)
                                        count += 1

                            counts[player].append(count)

                    # Remove empty list to make combat application work
                    if len(player_gids[player]) == 0:
                        player_gids.pop(player)
                    # end group loop
            # end player loop

            # Only enter combat if previous conditions hold true
            if len(player_gids) >= 2:
                #pdb.set_trace()
                # Build a damage dictionary
                #   keys = player ids
                #   values = array with the opposing unit id that each unit targeted
                infliction = {} # damage to other units
                nulled_ids = {}
                pids = np.array( list(self.players.keys()) )

                # Build damage
                for pid in player_gids:
                    # Only works for two players right now
                    opp_pid = np.where( pids != pid )[0][0]
                    opp_player_units = np.sum( counts[opp_pid] )
                    player_units = np.sum( counts[pid] )

                    infliction[pid] = {}
                    nulled_ids[pid] = {}
                    #pdb.set_trace()
                    for i, gid in enumerate(player_gids[pid]):
                        nulled_ids[pid][i] = []
                        for j in range(counts[pid][i]):
                            unittype_idx = counts_units[pid][gid][j]
                            unittype = self.players[pid].groups[gid].units[unittype_idx]
                            uid = np.random.randint(opp_player_units)
                            if uid in infliction[pid]:
                                infliction[pid][uid] += unittype.definition.damage
                            else:
                                infliction[pid][uid] = unittype.definition.damage
                # end player loop
                #pdb.set_trace()

                all_dmg[node.ID] = {pid:{'groups':[], 'units':[], 'health':[]} for pid in self.team_starts}

                # Apply damage - separate so units don't die before they get to apply their damage
                for pid in player_gids:
                    opp_pid = np.where( pids != pid )[0][0]

                    #pdb.set_trace()
                    # Loop through the infliction array
                    for tgt_idx in sorted( infliction[pid].keys() ):
                        # Determine which opposing group was affected
                        tgt_dmg = infliction[pid][tgt_idx]
                        tgt_group = 0
                        found = False

                        while found == False:
                            if tgt_idx < counts[opp_pid][tgt_group]:
                                #pdb.set_trace()
                                found = True
                                # Determine the opposing unit that was affected
                                tgt_gid = player_gids[opp_pid][tgt_group]
                                group = self.players[opp_pid].groups[tgt_gid]
                                tgt_unit_type_idx = counts_units[opp_pid][tgt_gid][tgt_idx]
                                tgt_unit = group.units[tgt_unit_type_idx]
                                tgt_armor = tgt_unit.definition.health
                                tgt_cntrl = 1 if node.controlledBy == opp_pid else 0

                                fort_bns = 1 if ('DEFEND' in node.resource) else 0
                                strct_def = node.defense
                                node_def = (tgt_cntrl + fort_bns) * strct_def

                                # Determine damage. Damage equation:
                                # ( 10 * damage infliction ) / ( (unit armor + fortress bonus) * structure defense )
                                loss = (10. * tgt_dmg) / (tgt_armor + node_def)

                                # Subtract damage
                                #pdb.set_trace()
                                if (len(nulled_ids[opp_pid][tgt_group]) > 0):
                                    #pdb.set_trace()
                                    tgt_idx -= len(nulled_ids[opp_pid][tgt_group])

                                for unit in group.units:
                                    if tgt_idx < np.sum(unit.unitHealth > 0):
                                        break
                                    tgt_idx -= np.sum(unit.unitHealth > 0)

                                tgt_unit_idx = np.argwhere( tgt_unit.unitHealth > 0 )[tgt_idx]
                                tgt_unit.unitHealth[tgt_unit_idx] -= loss

                                outgroup = group.mapGroupID
                                outunit = group.mapUnitID[tgt_unit_type_idx] + tgt_unit_idx

                                # Remove from node groups if dead
                                if tgt_unit.unitHealth[tgt_unit_idx] <= 0:
                                    outhealth = 0.
                                    tgt_unit.unitHealth[tgt_unit_idx] = 0
                                    tgt_unit.count -= 1
                                    group.count -= 1

                                    if tgt_unit.count == 0:
                                        group.speed.remove(tgt_unit.definition.speed)

                                    # Does not append the original tgt_idx, but we're
                                    # fine because the tgt_idxs were sorted.
                                    nulled_ids[opp_pid][tgt_group].append(tgt_idx)
                                    # Disband the group
                                    if group.count == 0:
                                        #pdb.set_trace()
                                        self.players[opp_pid].groups[tgt_gid].destroyed = True
                                        # Making sure that destroyed group is no longer moving nor ready
                                        self.players[opp_pid].groups[tgt_gid].moving = False
                                        self.players[opp_pid].groups[tgt_gid].ready = False
                                        pop_idx = node.groups[opp_pid].index(tgt_gid)
                                        node.groups[opp_pid].pop(pop_idx)

                                        outstr = '{:.6f},{},{}'.format(
                                                self.current_turn,
                                                opp_pid,
                                                self.players[opp_pid].groups[tgt_gid].mapGroupID
                                        )
                                        self.output['GROUP_Disband'].append(outstr)
                                else:
                                    outhealth = tgt_armor * (tgt_unit.unitHealth[tgt_unit_idx] / 100.)
                                outhealthstr = '{:.6f}'.format(float(outhealth))
                                all_dmg[node.ID][opp_pid]['groups'].append(int(outgroup))
                                all_dmg[node.ID][opp_pid]['units'].append(int(outunit))
                                all_dmg[node.ID][opp_pid]['health'].append(float(outhealthstr))
                            else:
                                tgt_idx -= counts[opp_pid][tgt_group]
                                tgt_group += 1
                        # end target unit search
                    # end target loop

                    # Build combat output message
                    outstr = '{:.6f},{},{},[{}],[{}],[{}]'.format(
                            self.current_turn,
                            opp_pid,
                            node.ID,
                            ';'.join(str(i) for i in all_dmg[node.ID][opp_pid]['groups']),
                            ';'.join(str(i) for i in all_dmg[node.ID][opp_pid]['units']),
                            ';'.join(str(i) for i in all_dmg[node.ID][opp_pid]['health']),
                    )
                    self.output['GROUP_CombatUpdate'].append(outstr)

                # end player loop
                #pdb.set_trace()
            # end if combat check
        # end node loop

    def movement(self):
        ## Apply group movements
        for player in self.team_starts:
            for group in self.players[player].groups:
                if not group.destroyed:
                    if group.ready:
                        # Let a turn pass to make Unreal logic happy
                        group.moving = True
                    elif group.moving:

                        # Get information for adjustments
                        start_idx = int( np.squeeze(np.where(self.map_key1 == group.location)) )
                        end_idx = int( np.squeeze(np.where(self.map_key1 == group.travel_destination)) )

                        wind_value = self.winds[(start_idx, end_idx)]

                        if group.distance_remaining >= .5:
                            wind_mag = self.winds[(start_idx, end_idx)][0]

                        else:
                            wind_mag = self.winds[(start_idx, end_idx)][1]

                        # Apply amount moved
                        # BUG - if group consists of different unit types, it won't move properly
                        group.distance_remaining -= (group.speed[0] + group.speed[0] * wind_mag)

                        # Check for arrival
                        if group.distance_remaining <= 0:
                            # ARRIVED
                            # Adjust locations and groups at each node
                            outstr = '{:.6f},{},{},{},{},{}'.format(
                                    self.current_turn,
                                    player,
                                    group.mapGroupID,
                                    self.evgMap.nodes[start_idx].ID,
                                    self.evgMap.nodes[end_idx].ID,
                                    'ARRIVED'
                            )
                            self.output['GROUP_MoveUpdate'].append(outstr)
                            self.evgMap.nodes[start_idx].groups[player].remove(group.groupID)
                            self.evgMap.nodes[end_idx].groups[player].append(group.groupID)
                            group.distance_remaining = 0
                            group.moving = False
                            group.location = group.travel_destination
                            group.travel_destination = -1

                        else:
                            # IN_TRANSIT
                            outstr = '{:.6f},{},{},{},{},{}'.format(
                                    self.current_turn,
                                    player,
                                    group.mapGroupID,
                                    self.evgMap.nodes[start_idx].ID,
                                    self.evgMap.nodes[end_idx].ID,
                                    'IN_TRANSIT'
                            )
                            self.output['GROUP_MoveUpdate'].append(outstr)

                    # end move adjustments
            # end group loop
        # end player loop

    def capture(self):
        for node in self.evgMap.nodes:
            controllers = []
            points = {}
            # Check for number of current groups at each node
            for pid in node.groups:
                points[pid] = 0
                if len(node.groups[pid]) > 0:

                    ctr = 0
                    for gid in node.groups[pid]:
                        # Discount in-transit groups
                        if self.players[pid].groups[gid].moving == False:
                            ctr += 1
                            for unit in self.players[pid].groups[gid].units:
                                count = unit.count
                                xer = unit.definition.control
                                points[pid] += count * xer
                    if ctr >= 1:
                        controllers.append(pid)

            # If only 1 group, let them capture
            if len(controllers) == 1:

                if (np.abs(node.controlState) < node.controlPoints) or \
                   (controllers[0] != node.controlledBy):
                    # Logistics
                    if controllers[0] == 0:
                        pxer = 1
                        pid = 0
                    else:
                        pxer = -1
                        pid = 1

                    # Capture
                    #pdb.set_trace()
                    neutralize = False
                    if self.current_turn == 0:
                        node.controlState = node.controlPoints * pxer
                    else:
                        oldSign = int(node.controlState < 0)
                        node.controlState += points[pid] * pxer
                        newSign = int(node.controlState < 0)
                        neutralize = True if oldSign != newSign else False

                        # Build output
                        fullctrl = 'true' if np.abs(node.controlState) >= node.controlPoints else 'false'
                        outstr = '{:.6f},{},{},{:.6f},{}'.format(
                                self.current_turn,
                                node.ID,
                                pid,
                                np.abs(node.controlState),
                                fullctrl
                        )
                        self.output['NODE_ControlUpdate'].append(outstr)

                    # Update
                    if np.abs(node.controlState) >= node.controlPoints:
                        node.controlState = node.controlPoints * pxer
                        node.controlledBy = pid
                    if node.controlledBy != -1 and neutralize:
                        print('!!!!!!Neutralize!!!!!!!!')
                        print(node.controlledBy)
                        node.controlledBy = -1
                        print(node.controlledBy)
                        print()


    def output_init(self):
        # Output telemetry files
        date = datetime.datetime.today()
        date_frmt = date.strftime('%Y.%m.%d-%H.%M.%S')
        self.dat_dir = self.output_dir + '/' + self.evgMap.name + '_' + date_frmt

        oldmask = os.umask(000)
        os.mkdir(self.dat_dir,mode=0o777)
        os.umask(oldmask)
        assert( os.path.isdir(self.dat_dir) ), 'Could not create telemetry output directory'

        self.output = {}
        hdr = '0,player1,player2,status,focus'
        self.output['GAME_Scores'] = [hdr]

        hdr = '0,player,node,groups,units,health'
        self.output['GROUP_CombatUpdate'] = [hdr]

        hdr = '0,player,group'
        self.output['GROUP_Disband'] = [hdr]

        hdr = '0,player,group,node,types,start,count,sensorsettings'
        self.output['GROUP_Initialization'] = [hdr]

        hdr = '0,player,unitTypes,unitCount,status,node1,node2'
        self.output['GROUP_Knowledge'] = [hdr]

        hdr = '0,player,group,start,destination,status'
        self.output['GROUP_MoveUpdate'] = [hdr]

        hdr = '0,node,faction,controlvalue,controlled'
        self.output['NODE_ControlUpdate'] = [hdr]

        hdr = '0,player,nodes,knowledge,controller,percent'
        self.output['NODE_Knowledge'] = [hdr]

        hdr = '0,player1,player2'
        self.output['PLAYER_Tags'] = [hdr]

        hdr = 'nodes'
        self.output['MAP_Nodes'] = [hdr]

        for node in self.p1_node_map:
            self.output['MAP_Nodes'].append(str(node))

        hdr = '0,player,enemysource,enemydestination,enemyunitcounts'
        self.output['SENSOR_ServerData'] = [hdr]

    def build_knowledge_output(self):
        players = np.array( list(self.players.keys()) )

        for pid in self.team_starts:
            opp_pid = np.where( players != pid )[0][0]
            knowledge = [0 for i in self.map_key2]
            nodes = []
            controller = []
            percent = []

            # Node knowledge
            for i, nidx in enumerate(self.map_key2):
                node = self.evgMap.nodes[nidx]
                stationed = False
                partial_nodes = []
                for gid in node.groups[pid]:
                    group = self.players[pid].groups[gid]
                    if group.moving == False:
                        stationed = True
                    else:
                        dest = group.travel_destination
                        if dest not in partial_nodes:
                            partial_nodes.append(dest)
                # end node group loop
                adj_watchtower = False
                incoming_units = False

                for j, cid in enumerate(node.connection_idxs):
                    cidx = int(np.squeeze(np.where(self.map_key1 == cid)))
                    conn = self.evgMap.nodes[cidx]

                    # See if adjacent watchtower
                    if ('OBSERVE' in conn.resource) and \
                       (conn.controlledBy == pid) and \
                       (np.abs(conn.controlState) == conn.controlPoints):
                        adj_watchtower = True

                    # See if player groups moving to the area
                    for gid in conn.groups[pid]:
                        in_group = self.players[pid].groups[gid]
                        if (in_group.moving == True) and \
                           (in_group.travel_destination == node.ID):
                               incoming_units = True
                               break
                    # end incoming group check


                if node.controlledBy == pid or stationed:
                    # full knowledge
                    knowledge[i] = 2
                    ctrl = node.controlledBy
                    pcnt = '{:.6f}'.format(100. * node.controlState / node.controlPoints)
                elif adj_watchtower or incoming_units:
                    # partial knowledge knowledge
                    knowledge[i] = 1
                    ctrl = node.controlledBy
                    pcnt = '{:.6f}'.format(100. * node.controlState / node.controlPoints)
                else:
                    # no change
                    ctrl = -1
                    pcnt = '{:.6f}'.format(0)
                nodes.append(node.ID)
                controller.append(ctrl)
                percent.append(pcnt)


            # end node knowledge loop

            # Node Knowledge Outstring
            outstr = '{:.6f},{},[{}],[{}],[{}],[{}]'.format(self.current_turn,
                                              pid,
                                              ';'.join(str(i) for i in nodes),
                                              ';'.join(str(i) for i in knowledge),
                                              ';'.join(str(i) for i in controller),
                                              ';'.join(str(i) for i in percent)
            )
            self.output['NODE_Knowledge'].append(outstr)

            # Group knowledge loop
            opp_k = {}  # player knowledge of enemy groups

            # Loop through nodes again now that we have knowledge of them all
            for i, nidx in enumerate(self.map_key2):
                nid = nodes[i]
                node = self.evgMap.nodes[nidx]
                if knowledge[i] == 1 or knowledge[i] == 2:
                    opp_k[nid] = {} # Dictionary of destinations

                    for opp_gid in node.groups[opp_pid]:
                        opp_group = self.players[opp_pid].groups[opp_gid]

                        for unit in opp_group.units:
                            in_ut = unit.unitType
                            ut = in_ut[0].upper() + in_ut[1:]
                            uc = unit.count
                            if opp_group.moving == False:
                                # Append as group staying put
                                if -1 in opp_k[nid]:
                                    opp_k[nid][-1]['unitTypes'].append(ut)
                                    opp_k[nid][-1]['unitCount'].append(uc)

                                else:
                                    opp_k[nid][-1] = {'unitTypes':[ut],
                                                      'unitCount':[uc],
                                                      'status': 0
                                                     }
                                # end key existence check
                            else:
                                # Check for knowledge of destination
                                opp_dst = opp_group.travel_destination
                                dst_idx = nodes.index(opp_dst)
                                # Check knowledge of node id
                                if knowledge[dst_idx] > 0:
                                    if dst_idx in opp_k[nid]:
                                        opp_k[nid][dst_idx]['unitTypes'].append(ut)
                                        opp_k[nid][dst_idx]['unitCount'].append(uc)

                                    else:
                                        opp_k[nid][dst_idx] = {'unitTypes':[ut],
                                                               'unitCount':[uc],
                                                               'status': 0
                                                              }
                        # end group knowledge addition
                    # end group loop
                    if not bool(opp_k[nid]):
                        opp_k.pop(nid,None)
            # end group knowledge loop

            # Group knowledge outstring
            if bool(opp_k):
                for nid in opp_k.keys():
                    for dst in opp_k[nid].keys():
                        status = 0 if dst == -1 else 1
                        outstr = '{:.6f},{},[{}],[{}],{},{},{}'.format(
                                self.current_turn,
                                opp_pid,
                                ';'.join(str(i) for i in opp_k[nid][dst]['unitTypes']),
                                ';'.join(str(i) for i in opp_k[nid][dst]['unitCount']),
                                status,
                                nid,
                                dst
                        )
                        self.output['GROUP_Knowledge'].append(outstr)
                    # end destination key loop
                # end node key loop
            # end group knowledge outstring

        # end player loop


    def write_output(self):
        for key in self.output.keys():
            #pdb.set_trace()
            key_dir = self.dat_dir + '/' + str(key)
            oldmask = os.umask(000)
            os.mkdir(key_dir,mode=0o777)
            os.umask(oldmask)
            assert( os.path.isdir(key_dir) ), 'Could not create telemetry {} output directory'.format(key)

            key_file = key_dir + '/' + 'Telem_' + key
            with open(key_file, 'w') as fid:
                writer = csv.writer(fid, delimiter='\n')
                writer.writerow(self.output[key])



# end class EvergladesGame
