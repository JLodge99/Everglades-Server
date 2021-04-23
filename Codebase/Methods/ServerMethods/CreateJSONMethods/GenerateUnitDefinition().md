# GenerateUnitDefinition()
This helper function generates the JSON string required to store a single unit in a JSON. This storage is not attribute based, rather as definitial information loaded on game start. This function is called by GenerateUnitDefinitions()


## Syntax
```pythons
GenerateUnitDefinition(string name, string[] attributeList)
```

## Returns
Returns a string JSON representation used in the creation of the JSON file.

## Parameters
|Parameter      |Description        |
|---------------|-------------------|
|**name**| The name of the unit to be created.|
|**attributeList**| A list of all the attributes the unit possesses.|
