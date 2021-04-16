# GenerateUnitAttribute()
This function returns formatted information used when storing Attribute information in a JSON file by taking in multiple fields. Primarily used as a helper function


## Syntax
```pythons
GenerateUnitAttribute(string name, string effect, string description, int modifier, bool isMult, int modPriority, int cost)
```

## Returns
Returns formatted information used when storing Attribute information in a JSON file

## Parameters
|Parameter      |Description        |
|---------------|-------------------|
|**name**| The name of the Attribute|
|**effect**| The name of the Attribute variable to be changed.|
|**description**| The description of the Attribute|
|**modifier**| The value of the Attribute|
|**isMult**| If true this value multiplies the current value, if false this attributes value adds to the current value|
|**modPriority**| This is a relic parameter that has no effect. Intended to help determine in what order attributes effecting the same variable would be applied. Perhaps can be used later in development if attributes functionality are expanded|
|**cost**| The point cost of obtaining an attribute|