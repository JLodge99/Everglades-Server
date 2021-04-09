# GenerateJsonFileLoadout()
This creates a JSON file of the name 'Loadout_X' where X is a number. The JSON is stored in the config folder and represents the loadout of a particular player X

## Syntax
```python
GenerateJsonFileLoadout(string[][] loadout, int playerIdentifier)
```

## Returns
No value is returned. Results in creation of a new squad JSON

## Parameters
|Parameter      |Description        |
|---------------|-------------------|
|**loadout**    |An array holding arrays, representing different squads. Each array subsequently contains strings designating the name of the unit in that squad|
|**playerIdentifier**|The number designation of the player. 0 and 1 are used for the two players. -1 is reserved for the default loadout|