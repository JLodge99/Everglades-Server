# EvergladesEnv
**This class contains the OpenAI Gym and is the Everglades environment.**

## Variables
|Variable                   |Type               |                       Description                                                             |
|---------------------------|-------------------|-----------------------------------------------------------------------------------------------|
|**action_space**           |*Tuple*            |This defines the range of actions an agent may take.                                           |
|**debug**                  |*bool*             |This flag allows the masking of fog of war for debugging purposes.                             |
|**game**                   |*EvergladesGame*   |This is an instance of the Everglades game.                                                    |
|**num_actions_per_turn**   |*int*              |The number of actions a player may take per turn.                                              |
|**num_groups**             |*int*              |The number of groups per player.                                                               |
|**num_nodes**              |*int*              |The number of nodes in the map.                                                                |
|**num_turns**              |*int*              |The number of turns in a game.                                                                 |
|**num_units**              |*int*              |The total number of units per player.                                                          |
|**observation_space**      |*Box*              |This defines the boundaries of observation.                                                    |
|**pks**                    |*list<dict_keys>*  |The list of keys for the player dictionary.                                                    |
|**player_dat**             |*dict*             |This contains the unit groups for each player.                                                 |
|**players**                |*dict*             |The keys are 0 and 1, the values are an instance of the agent class for the respective player. |
|**sorted_pks**             |*list<dict_keys>*  |The sorted list of keys for the player dictionary.                                             |
|**unit_classes**           |*list\<string>*    |The types of units in the game.                                                                |

## Methods
[**_build_groups()**](../../Methods/ServerMethods/_build_groups().md)  
[**_build_observations()**](../../Methods/ServerMethods/_build_observations().md)  
[**_build_observation_space()**](../../Methods/ServerMethods/_build_observation_space().md)  
[**reset()**](../../Methods/ServerMethods/reset().md)  
[**step()**](../../Methods/ServerMethods/step().md)  