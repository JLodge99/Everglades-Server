# EvgGroup
**This is the class of a group of units.**

## Variables
|Variable               |Type               |Description                                                                                |
|-----------------------|-------------------|-------------------------------------------------------------------------------------------|
|**groupID**            |*int*              |The identification number for the group.                                                   |
|**universalIndex**     |*int*              |The universal identification number for the group, e.g. Player 1's first group is 12       |
|**mapGroupID**         |*int*              |A cumulative group identification for outputting the initial number of groups on the map.  |
|**mapUnitID**          |*int*              |A cumulative unit identification for outputting the initial number of units on the map.    |
|**location**           |*int*              |The node where the group is located.                                                       |
|**ready**              |*bool*             |This indicates if the group is ready to move.                                              |
|**moving**             |*bool*             |This indicates if the group is currently moving.                                           |
|**destroyed**          |*bool*             |This indicates if the group has been destroyed.                                            |
|**distance_remaining** |*int*              |The remaining distance the group must travel to reach the destination node.                |
|**travel_destination** |*int*              |The node to which the group is traveling.                                                  |
|**units**              |*list\<EvgUnit>*   |The list of units contained in the group.                                                  |
|**pathIndex**          |*int*              |This property is never referenced.                                                         |
|**speed**              |*int*              |The speed for the group based on the units that comprise it.                               |
|**counts**             |*dict\<int>*       |The numbers of unit types within the group.                                                |
