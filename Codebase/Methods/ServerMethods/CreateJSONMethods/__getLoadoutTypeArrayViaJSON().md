# __getLoadoutTypeArrayViaJSON()
This takes in the data from a JSON formatted specifically for loadouts and parses it out into an array of array of strings compatable with other functions. This function is primarily a helper function to convert JSON data representation


## Syntax
```pythons
__getLoadoutTypeArrayViaJSON(string loadedData)
```

## Returns
Returns an array of array of strings representing the loadout

## Parameters
|Parameter      |Description        |
|---------------|-------------------|
|**loadedData**| Data from a JSON formatted specifically for loadouts. The function __loadJsonFileLoadout() will return a compatable data type for this parameter|