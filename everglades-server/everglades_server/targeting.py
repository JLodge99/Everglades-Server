import random
import random as r
import re

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
            # Get the attacking unit's ID and base damage.
            #unitTypeID = self.unit_names[oppUnit.unitType.lower()]
            #oppUnit.damage = self.unit_types[unitTypeID].damage
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

    #print("Combat with ", len(enemyDrones), "drones")
    
    for groupID in activeUnits[player]:
        for attackingUnit in activeUnits[player][groupID]:

            if len(enemyDrones) == 0:
            #     print("No one is home")
                 return
            ##  Testing to prove that the drones are sorted by lowest health            
            # else:
            #     print("Drones:")
            #     for x in range(len(enemyDrones)): 
            #         print(enemyDrones[x].currentHealth)

            # Get the attacking unit's ID and base damage.
            unitTypeID = self.unit_names[attackingUnit.unitType.lower()]
            damage = self.unit_types[unitTypeID].damage
            
            targetedDrone = enemyDrones[0]

            enemyDrones[0].currentHealth = enemyDrones[0].currentHealth - damage

            # Make sure that we remove the most viable drone if it has been destroyed
            if enemyDrones[0].currentHealth <= 0.:
                del enemyDrones[0]

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
        for attackingUnit in activeUnits[player][groupID]:

         if len(enemyDrones) == 0:
        #    print("No one is home")
            return
        #Testing to prove that the drones are sorted by highest health
        # else:
        #    print("Drones:")
        #    for x in range(len(enemyDrones)): 
        #         print(enemyDrones[x].currentHealth)

            # Get the attacking unit's ID and base damage.
            unitTypeID = self.unit_names[attackingUnit.unitType.lower()]
            damage = self.unit_types[unitTypeID].damage
            targetedDrone = enemyDrones[0]
            enemyDrones[0].currentHealth = enemyDrones[0].currentHealth - damage

            # Make sure that we remove the most viable drone if it has been destroyed
            if enemyDrones[0].currentHealth <= 0.:
                del enemyDrones[0]

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
        for attackingUnit in activeUnits[player][groupID]:

            if len(enemyDrones) == 0:
            #     print("No one is home")
                return

            # Get the attacking unit's ID and base damage.
            unitTypeID = self.unit_names[attackingUnit.unitType.lower()]
            damage = self.unit_types[unitTypeID].damage
            targetedDrone = enemyDrones[0]

            enemyDrones[0].currentHealth = enemyDrones[0].currentHealth - damage

            # Make sure that we remove the most viable drone if it has been destroyed
            if enemyDrones[0].currentHealth <= 0.:
                del enemyDrones[0]

            # Submit the drone's action
            action = (opponent, targetedDrone.groupID, targetedDrone, damage)
            combatActions.append(action)
