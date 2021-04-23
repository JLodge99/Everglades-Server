import numpy as np

class EvgMap:
    def __init__(self, name):
        self.name = name
        self.nodes = []

class EvgMapNode:
    def __init__(self, **kwargs):
        self.ID = kwargs.get('ID',-1)
        self.radius = kwargs.get('radius',1)
        self.resource = kwargs.get('resource',[])
        self.defense = kwargs.get('defense',1)
        self.controlPoints = kwargs.get('points',100)
        self.teamStart = kwargs.get('teamStart',-1)
        self.controlledBy = self.teamStart
        self.controlState = 0
        self.connections = []
        self.connection_idxs = []
        self.groups = {}
        self.groups[0] = []
        self.groups[1] = []

class EvgNodeConnection:
    def __init__(self, **kwargs):
        self.destID = kwargs.get('destID',-1)
        self.distance = kwargs.get('distance',1)

class EvgPlayer:
    def __init__(self, playerNum):
        self.playerNum = playerNum
        self.ready = True
        self.groups = []

class EvgGroup:
    def __init__(self, **kwargs):
        self.groupID = kwargs.get('groupID',-1)
        self.universalIndex = kwargs.get('universalIndex', 0)
        self.mapGroupID = kwargs.get('mapGroupID',-1)
        self.location = kwargs.get('location',-1)
        self.ready = False
        self.moving = False
        self.destroyed = False
        self.hasAttackCommander = False
        self.hasSpeedCommander = False
        self.distance_remaining = 0
        self.mapUnitID = []
        self.travel_destination = -1
        self.units = []
        self.speed = []
        self.counts = {}
        self.pathIndex = 0

# Contains dynamic values for units within a group.
class EvgUnit:
    def __init__(self, **kwargs):
        self.unitType = kwargs.get('unitType', None)
        # Unit index is the local index of the unit within its respective group list.
        # Universal index is the unit's unique ID across all units in the game.
        self.unitIndex = kwargs.get('unitIndex', 0)
        self.universalIndex = kwargs.get('universalIndex', 0)
        self.currentHealth = kwargs.get('currentHealth', 0)
        self.currentSpeed = kwargs.get('currentSpeed', 0)

# Contains static values for units of a single type.
class EvgUnitDefinition:
    def __init__(self, **kwargs):
        self.unitType = kwargs.get('name', None)
        self.health = kwargs.get('health', 0)
        self.damage = kwargs.get('damage', 0)
        self.speed = kwargs.get('speed', 0)
        self.control = kwargs.get('control', 0)
        self.cost = kwargs.get('cost', 0)
        self.jamming = kwargs.get('jamming',0)
        self.commander_damage = kwargs.get('commander_damage',0)
        self.commander_speed = kwargs.get('commander_speed',0)
        self.recon = kwargs.get('recon', 0)
        self.speedbonus_controlled_ally = kwargs.get('speedbonus_controlled_ally', 0)
        self.speedbonus_controlled_enemy = kwargs.get('speedbonus_controlled_enemy', 0)

class MovementTurn:
    def __init__(self, **kwargs):
        self.currentTurn = kwargs.get('currentTurn',-1)
        self.player = kwargs.get('player',-1)
        self.gid = kwargs.get('gid',-1)
        self.location = kwargs.get('location',-1)
        self.nid = kwargs.get('nid',-1)
