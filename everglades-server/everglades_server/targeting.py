import random
import random as r
import re
import numpy as np

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
            # The predicted health is used to help targeting drones when the criteria is based on health
            oppUnit.predictedHealth = oppUnit.currentHealth

            ret.append(oppUnit)

    return ret

# This simulates the damage equation used by combat() to help better coordinate attacks.
def predictHealth(self, targetedUnit, targetedTeam, attackingUnit, attackingTeam, node):
    # Calculate the node defense bonus.
    nodeControlled = 1 if node.controlledBy == attackingTeam else 0
    fortBonus = 1 if ('DEFEND' in node.resource) else 0
    nodeDefense = (nodeControlled + fortBonus) * node.defense

    # Get the attacking unit's ID and base damage.
    attackerTypeID = self.unit_names[attackingUnit.unitType.lower()]
    baseDamage = self.unit_types[attackerTypeID].damage

    targetTypeID = self.unit_names[attackingUnit.unitType.lower()]
    targetBaseHealth = self.unit_types[targetTypeID].health
    
    # Calculate the true damage that will be applied to the targeted unit.
    trueDamage = (10. * baseDamage) / (targetBaseHealth + nodeDefense)
    appliedDamage = targetedUnit.predictedHealth - trueDamage

    if appliedDamage < 0.:
        appliedDamage = 0

    targetedUnit.predictedHealth = appliedDamage

# Randomly selects targets by:
# 1. Randomly selecting a single group from enemy groups that are at the node
# 2. Randomly selects a drone from that chosen group
# Information about the selected drone is added to a list of combat actions
def randomlySelect(self, combatActions, player, opponent, activeGroups, activeUnits, node):
    # Loop through all units in the current player and select an enemy for them to target.
    for groupID in activeUnits[player]:
        for attackingUnit in activeUnits[player][groupID]:
            # Get a random group from the list of the opponent's groups at the given node.
            oppGroupList = activeGroups[opponent]
            oppGroupID = np.random.choice(oppGroupList)
            
            # Get a random unit from that group.
            oppUnitList = activeUnits[opponent][oppGroupID]
            unitChoice = np.random.randint(len(oppUnitList))

            oppUnitID = oppUnitList[unitChoice]

            # Used to quickly debug targeting.
            # print("Player", player, "'s unit", attackingUnit.unitIndex, "is attacking unit", oppUnitID.unitIndex, "from group", oppGroupID)
            # print("Player", player, "'s unit", attackingUnit.unitIndex, "is attacking unit", oppUnitID.unitIndex)

            # Get the attacking unit's ID and base damage.
            unitTypeID = self.unit_names[attackingUnit.unitType.lower()]
            damage = self.unit_types[unitTypeID].damage

            # Build the action and append it to combatActions
            action = (opponent, oppGroupID, oppUnitID, damage)
            combatActions.append(action)

# This is a sample targeting function.
# It targets enemy drones by lowest health first. If all enemy drones have the same amount of health,
# or if any set of drones within the enemyDrones list have the same health, the list is sorted by a random number instead.
# FUTURE TEAM: This random sorting is not necessary. It was added to put some spice into targeting. It's entirely up to you what you want to do with it.
def lowestHealth(self, combatActions, player, opponent, activeGroups, activeUnits, node):
    # Create a list of ALL enemy drones
    enemyDrones = unravelEnemies(self,activeUnits[opponent])

    # Sort enemy drones based on current drone's targeting priority
    # If the values of the drones are the same, random numbers are generated and compared instead to sort the list randomly.
    # The sorting allows us to easily find the next valid target. The target that best-fits the criteria will always be at index 0,
    # with the next-best being at consequent indexes. We can then simulate damage on these drones, and if an enemy is "marked for death" - meaning
    # enough drones target that enemy for it to have a guaranteed death next turn - we can move to the next-best enemy in the list. Thus, no
    # drone is needlessly targeting an enemy which is guaranteed to die.
    enemyDrones = sorted(enemyDrones, key = lambda i: (i.currentHealth, random.random()))

    index = 0
    targetedDrone = enemyDrones[index]
    
    # Loop through all units in the current player and select an enemy for them to target.
    for groupID in activeUnits[player]:
        for attackingUnit in activeUnits[player][groupID]:
            if len(enemyDrones) == 0:
                 return

            # Get the attacking unit's ID and base damage.
            unitTypeID = self.unit_names[attackingUnit.unitType.lower()]
            damage = self.unit_types[unitTypeID].damage

            # See if the enemy at the current index meets the targeting criteria.
            # If not, move to the next index.
            if enemyDrones[index].predictedHealth > 0: 
                targetedDrone = enemyDrones[index]
            else:
                index = index + 1

            predictHealth(self, targetedDrone, opponent, attackingUnit, player, node)
            
            # Submit the drone's action
            action = (opponent, targetedDrone.groupID, targetedDrone, damage)
            combatActions.append(action)

            # Prevent a possible overflow. If all drones have been targeted and possibly killed,
            # then there is no reason to continue targeting.
            if index >= len(enemyDrones):
                return

# This is a sample targeting function.
# It functions in the exact same manner as lowestHealth(), except it targets drones
# by highest health first.
def highestHealth(self, combatActions, player, opponent, activeGroups, activeUnits, node):
    # Create a list of ALL enemy drones
    enemyDrones = unravelEnemies(self,activeUnits[opponent])

    # Sort enemy drones based on current drone's targeting priority
    # If the values of the drones are the same, random numbers are generated and compared instead to sort the list randomly.
    enemyDrones = sorted(enemyDrones, key = lambda i: (i.currentHealth, random.random()), reverse = True)
    largestHealth = max(enemyDrones, key = lambda i: (i.currentHealth)).currentHealth

    index = 0
    targetedDrone = enemyDrones[index]
    
    # Loop through all units in the current player and select an enemy for them to target.
    for groupID in activeUnits[player]:
        for attackingUnit in activeUnits[player][groupID]:
            if len(enemyDrones) == 0:
                 return

            # Get the attacking unit's ID and base damage.
            unitTypeID = self.unit_names[attackingUnit.unitType.lower()]
            damage = self.unit_types[unitTypeID].damage
            
            # See if the enemy at the current index meets the targeting criteria.
            # If not, move to the next index.
            if enemyDrones[index].predictedHealth >= largestHealth: 
                targetedDrone = enemyDrones[index]
            else:
                index = index + 1

            predictHealth(self, targetedDrone, opponent, attackingUnit, player, node)
            
            # Submit the drone's action
            action = (opponent, targetedDrone.groupID, targetedDrone, damage)
            combatActions.append(action)

            # Prevent a possible overflow. If all drones have been targeted and possibly killed,
            # then there is no reason to continue targeting.
            if index >= len(enemyDrones):
                return

# This is a sample targeting function.
# It prioritizes enemies based on unique conditions, labelling enemies as being more of a threat than others.
# Enemies who have the highest health and the highest damage are attacked before other enemies.
def mostLethal(self, combatActions, player, opponent, activeGroups, activeUnits, node):
    # Create a list of ALL enemy drones
    enemyDrones = unravelEnemies(self,activeUnits[opponent])

    # Sort enemy drones based on current drone's targeting priority
    # If the values of the drones are the same, random numbers are generated and compared instead to sort the list randomly.
    enemyDrones = sorted(enemyDrones, key = lambda i: (self.unit_types[self.unit_names[i.unitType.lower()]].damage, i.currentHealth, random.random()), reverse=True)
    strongestUnit = max(enemyDrones, key = lambda i: (self.unit_types[self.unit_names[i.unitType.lower()]].damage))
    largestDamage = self.unit_types[self.unit_names[strongestUnit.unitType.lower()]].damage
    largestHealth = max(enemyDrones, key = lambda i: (i.currentHealth)).currentHealth

    index = 0
    targetedDrone = enemyDrones[index]
    
    # Loop through all units in the current player and select an enemy for them to target.
    for groupID in activeUnits[player]:
        for attackingUnit in activeUnits[player][groupID]:
            if len(enemyDrones) == 0:
                 return

            # Get the attacking unit's ID and base damage.
            unitTypeID = self.unit_names[attackingUnit.unitType.lower()]
            damage = self.unit_types[unitTypeID].damage
            
            # If the enemy at the present index has a predicted health value that rivals that of the largest found thus far,
            # and if it has a damage output value that also rivals the largest found thus far, target that enemy.
            if enemyDrones[index].predictedHealth >= largestHealth and self.unit_types[self.unit_names[enemyDrones[index].unitType.lower()]].damage >= largestDamage: 
                targetedDrone = enemyDrones[index]
            # Otherwise, begin targeting the drone at the next index.
            else:
                index = index + 1

            predictHealth(self, targetedDrone, opponent, attackingUnit, player, node)
            
            # Submit the drone's action
            action = (opponent, targetedDrone.groupID, targetedDrone, damage)
            combatActions.append(action)

            # Prevent a possible overflow. If all drones have been targeted and possibly killed,
            # then there is no reason to continue targeting.
            if index >= len(enemyDrones):
                return

def callCustomTargeting(self, combatActions, player, opponent, activeGroups, activeUnits, node):
    # Imported from the agent script
    # Provide a copy of the node so they can't change it, or remove the node information entirely
    unreliableCombatActions = customTargeting(self, player, opponent, activeGroups, activeUnits, node)
    # Ensure that the actions are not using drones that are not within the group. i.e. they're making a striker attack enemies when the group contains no strikers, or
    # they're allowing a single unit to attack every enemy multiple times

    # for action in unreliableCombatActions:
    #     if action[3] is not an integer:
    #         say "stop cheating"
    #     elif action[3] is a valid unit ID:
    #         convert that ID into the damage that unit type deals
    action[3] = self.unit_types[action[3].lower()].damage

    combatActions = unreliableCombatActions


    # unreliableCombatActions has the same tuple structure as combatActions, except damage is replaced by the unit type that is attacking
    # After the custom targeting funciton finishes, we need to run through combat actions and replace the unit type that's attacking with
    # the amount of damage it deals
