# GenerateAttributeBasedUnit()
This function is a helper function that formats and returns the data necessary to store a unit with respect to what attributes a unit has. GenerateAttributeBasedUnitsFile() directly uses this function as a helper function


## Syntax
```pythons
GenerateAttributeBasedUnit(string name, string[] attributeSlugs)
```

## Returns
Returns the data necessary to store a unit with respect to what attributes a unit has.

## Parameters
|Parameter      |Description        |
|---------------|-------------------|
|**name**| A string designating the name to be used by a unit.|
|**attributeSlugs**| An array containing the name designation of each attribute the unit is considered to have.|
