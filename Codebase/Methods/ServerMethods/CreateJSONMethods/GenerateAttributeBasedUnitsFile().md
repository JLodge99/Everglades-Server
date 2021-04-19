# GenerateAttributeBasedUnitsFile()
This function takes information on the units names and corresponding list of attributes and generates a JSON file to store the data. Whenever the units present in the game would be updated, this is the function to run the new information through.


## Syntax
```pythons
GenerateAttributeBasedUnitsFile(string[] names, string[][] attributeSlugsList)
```

## Returns
Returns the data necessary to store all units with respect to what attributes a unit has.

## Parameters
|Parameter      |Description        |
|---------------|-------------------|
|**names**| An array of strings designating the names to be used by each unit.|
|**attributeSlugsList**| An array of arrays, containing the name designation of each attribute that each unit is considered to have. The index of the primary array matches to the index of the names list in terms of which names are linked to which list of attributes.|
