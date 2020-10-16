# EvgMapNode
**This is the class of the nodes that make up the Everglades map.**

## Variables
|Variable           |Type                       |Description                                                                                                                                        |
|-------------------|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
|**ID**             |*int*                      |The identification number of the node.                                                                                                             |
|**radius**         |*float*                    |The radius of the node.                                                                                                                            |
|**resource**       |*list\<string>*            |A list of the resources for the node. It contains ‘OBSERVE’ for watchtower, ‘DEFENSE’ for fortress, and an empty list for a node with no resources.|
|**defense**        |*int*                      |The defense value for the node.                                                                                                                    |
|**controlPoints**  |*int*                      |The amount of points a player receives for controlling the node.                                                                                   |
|**teamStart**      |*int*                      |Indicates the node is a team’s home base. It is 0 for player 0, 1 for player 1, and -1 for all neutral nodes.                                      |
|**controlledBy**   |*int*                      |Indicates which player controls the node. It uses the same integer values as teamStart.                                                            |
|**controlState**   |*int*                      |This is the percentage that the node is under control.                                                                                             |
|**connections**    |*list\<EvgNodeConnections>*|The list of tuples containing valid connections from this node and the respective distances.                                                       |
|**connection_idxs**|*list\<int>*               |The list of valid connections from this node.                                                                                                      |
|**groups**         |*dict*                     |The key is the player number (0 or 1) and the value is a list of group IDs for groups located at this node.                                        |
