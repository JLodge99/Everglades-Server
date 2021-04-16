# __loadJsonFileLoadout()
This loads a JSON file of the name 'Loadout_X' where X is a number. The JSON is stored in the config folder and represents the loadout of a particular player X. This is a helper function called by GetLoadout(). 

## Syntax
```python
__loadJsonFileLoadout(int playerIdentifier)
```

## Returns
Returns a string[][], which holds the name of each unit in each squad, with the main array indexes being the squads. If playerIdentifier is less then 0, or the loadout requested does not exist, returns the default loadout: 'Loadout_-1'

## Parameters
|Parameter      |Description        |
|---------------|-------------------|
|**playerIdentifier**|The number designation of the player. 0 and 1 are used for the two players. -1 is reserved for the default loadout.|