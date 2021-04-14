import random
import random as r
import re
from agents import random_actions

# Targeting functions take in 4 parameters:
# - combatActions:  List of what each unit is targeting
# - player:         Index for which units to use
# - activeGroup:    Two lists for each player's active groups
# - activeUnits:    List of units

# enemyGroups = activeGroups[enemy]
# Helper function that returns all enemy drones into a list
def unravelEnemies(self,oppUnits):
    ret = []

    # group : [dorne1, dorone2, drone3],
    # group : [dorne1, drone2, dron3]
    # (1,2)
    # Check each available group
    for oppGroupID in oppUnits.keys():
        # Check each drone in each available group to assign reference to their groupID and unitID
        for index,oppUnit in enumerate(oppUnits[oppGroupID]):
            oppUnit.groupID = oppGroupID
            ret.append(oppUnit)

    return ret

def randomlySelect(self,combatActions,player,opponent,activeGroups,activeUnits):

    for groupID in activeUnits[player]:
        for attackingUnit in activeUnits[player][groupID]:
            random.seed()

            # Get a random group from the list of the opponent's groups at the given node.
            oppGroupList = activeGroups[opponent]
            oppGroupID = random.choice(oppGroupList)

            # Get a random unit from that group.
            oppUnitList = activeUnits[opponent][oppGroupID]
            oppUnitID = random.choice(oppUnitList)

            # Get the attacking unit's ID and base damage.
            unitTypeID = self.unit_names[attackingUnit.unitType.lower()]
            damage = self.unit_types[unitTypeID].damage
            
            # Build the action and append it to combatActions
            action = (opponent, oppGroupID, oppUnitID, damage)
            combatActions.append(action)

def lowestHealth(self,combatActions,player,opponent,activeGroups,activeUnits):

    # activeUnits[player][groupID][unitType][unitID] = unitType
    # Create a list of ALL enemy drones
    enemyDrones = unravelEnemies(self,activeUnits[opponent])

    ## Sort enemy drones based on current drone's targeting priority
    enemyDrones = sorted(enemyDrones, key = lambda i: i.currentHealth)
    
    for groupID in activeUnits[player]:
        for attackingUnit in activeUnits[player][groupID]:

            if len(enemyDrones) == 0:
                 return

            # Get the attacking unit's ID and base damage.
            unitTypeID = self.unit_names[attackingUnit.unitType.lower()]
            damage = self.unit_types[unitTypeID].damage
            
            # Target drone by most viable
            targetedDrone = enemyDrones[idx % len(enemyDrones)]

            # Submit the drone's action
            action = (opponent, targetedDrone.groupID, targetedDrone, damage)
            combatActions.append(action)

def highestHealth(self,combatActions,player,opponent,activeGroups,activeUnits):

    # activeUnits[player][groupID][unitType][unitID] = unitType
    # Create a list of ALL enemy drones
    enemyDrones = unravelEnemies(self,activeUnits[opponent])

    ## Sort enemy drones based on current drone's targeting priority
    enemyDrones = sorted(enemyDrones, key = lambda i: i.currentHealth,reverse=True)
    
    for groupID in activeUnits[player]:
        for idx, attackingUnit in enumerate(activeUnits[player][groupID]):

            if len(enemyDrones) == 0:
                return

            # Get the attacking unit's ID and base damage.
            unitTypeID = self.unit_names[attackingUnit.unitType.lower()]
            damage = self.unit_types[unitTypeID].damage

            # Target drone by most viable
            targetedDrone = enemyDrones[idx % len(enemyDrones)]

            # Submit the drone's action
            action = (opponent, targetedDrone.groupID, targetedDrone, damage)
            combatActions.append(action)

def mostLethal(self,combatActions,player,opponent,activeGroups,activeUnits):

    # activeUnits[player][groupID][unitType][unitID] = unitType
    # Create a list of ALL enemy drones
    enemyDrones = unravelEnemies(self,activeUnits[opponent])

    ## Sort enemy drones based on current drone's targeting priority
    enemyDrones = sorted(enemyDrones, key = lambda i: (self.unit_types[self.unit_names[i.unitType.lower()]].damage, i.currentHealth), reverse=True)
    ## Testing to prove drones are sorted by most highest damage and health
    #for dr in enemyDrones:
    #    print(self.unit_types[self.unit_names[dr.unitType.lower()]].damage)

    for groupID in activeUnits[player]:
        for idx,attackingUnit in enumerate(activeUnits[player][groupID]):

            if len(enemyDrones) == 0:
                return

            # Get the attacking unit's ID and base damage.
            unitTypeID = self.unit_names[attackingUnit.unitType.lower()]
            damage = self.unit_types[unitTypeID].damage

            # Target next viable drone
            targetedDrone = enemyDrones[idx % len(enemyDrones)] 

            # Submit the drone's action
            action = (opponent, targetedDrone.groupID, targetedDrone, damage)
            combatActions.append(action)

def callCustomTargeting(self, combatActions, player, opponent, activeGroups, activeUnits,node):
    # Imported from the agent script
    # Provide a copy of the node so they can't change it
    nodecopy = node
    unreliableCombatActions = customTargeting(self, player, opponent, activeGroups, activeUnits, nodecopy)

    #Keep a list of each attacking unit type that exists
    attackingUnits = []
    for groupID in activeUnits[player]:
        for attackingUnit in enumerate(activeUnits[player][groupID]):
            attackingUnits.append(attackingUnit)

    # Ensure that the actions are not using drones that are not within the group. i.e. they're making a striker attack enemies when the group contains no strikers

    for action in unreliableCombatActions:
        # Check that damage is a number and indexes a unit type so we can get its damage, if all is good then we edit the action with the calculated damage
        try:
            1 + action[3]                                           # Check if value is an integer
            attackingUnits.remove(action[3].lower())                # Check that attacking unit exists, prevents unit from atacking more than once
            action[3] = self.unit_types[action[3].lower()].damage   # Change value to calculated damage
        except:
            print("Damage is not valid")

    combatActions = unreliableCombatActions

    # unreliableCombatActions has the same tuple structure as combatActions, except damage is replaced by the unit type that is attacking
    # After the custom targeting funciton finishes, we need to run through combat actions and replace the unit type that's attacking with
    # the amount of damage it deals