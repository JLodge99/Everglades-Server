# ConvertLoadoutToObject()
This converts an array of array of strings representing a loadout, into an object


## Syntax
```pythons
ConvertLoadoutToObject(int playerIdentifier)
```

## Returns
Returns a configuration required for the storing of loadout data

## Parameters
|Parameter      |Description        |
|---------------|-------------------|
|**playerIdentifier**| A number representing the player. For a two person game the numbers would be either 0 or 1. -1 is reserved for the default loadout. Any negative number will result in the default loadout being loaded due to the return conditions of __getLoadoutTypeArrayViaJSON()|