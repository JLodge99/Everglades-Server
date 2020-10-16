# EvgUnit
**The class of the Everglades drone unit.**

## Variables
|Variable       |Type               |Description                                                                |
|---------------|-------------------|---------------------------------------------------------------------------|
|**unitType**   |*string*           |The type of the unit for the group.                                        |
|**count**      |*int*              |The amount of this type of unit for the group.                             |
|**unitHealth** |*ndarray\<int>*    |An array of health values for each unit. Its length is the value of count. |
|**definition** |*EvgUnitDefinition*|It contains the definition of the unit type.                               |
