# GetLoadoutTypeArray()
This takes in an identifier for a player and returns a loadout for use in standard gameplay. This function should be used when attempting to retrieve a loadout for any game use as this function uses checks to ensure the loadout being retrieved is valid. If the loadout is not found or determined to be invalid for the game, the default loadout is returned.


## Syntax
```pythons
GetLoadoutTypeArray(int playerIdentifier)
```

## Returns
Returns an array of array of strings representing the loadout

## Parameters
|Parameter      |Description        |
|---------------|-------------------|
|**playerIdentifier**| A number representing the player. For a two person game the numbers would be either 0 or 1. -1 is reserved for the default loadout. Any negative number will result in the default loadout being loaded due to the return conditions of __getLoadoutTypeArrayViaJSON()|