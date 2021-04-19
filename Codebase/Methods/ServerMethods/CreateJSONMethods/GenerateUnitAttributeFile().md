# GenerateUnitAttributeFile()
This function writes an attribute JSON to be used with unit creation. 


## Syntax
```pythons
GenerateUnitAttributeFile(string[] names, string[] effects, string[] descriptions, int[] modifiers, bool[] isMults, int[] modPrioritys, int[] costs)
```

## Returns
Returns nothing. Causes a JSON file to be generated.

## Parameters
|Parameter      |Description        |
|---------------|-------------------|
|**names**| An array containing the name of each Attribute|
|**effects**| An array containing the name of each Attribute variable to be changed.|
|**descriptions**| An array containing the description of each Attribute|
|**modifiers**| An array containing the value of each Attribute|
|**isMults**| An array containing boolean information for each attribute. If true the corresponding attributes modifier value multiplies the current value, if false this attributes value adds to the current value|
|**modPrioritys**| An array containing stored ints for each attribute. This is a relic parameter that has no effect. Intended to help determine in what order attributes effecting the same variable would be applied. Perhaps can be used later in development if attributes functionality are expanded|
|**costs**| An array containing the point cost of obtaining each attribute|