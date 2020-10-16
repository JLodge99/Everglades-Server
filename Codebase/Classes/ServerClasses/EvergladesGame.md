# EvergladesGame
**This class contains the logic of the Everglades game.**

## Variables
|Variable               |Type                       |Description                                                                                                                                            |
|-----------------------|---------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|  
|**_vec_convert_node**  |*vectorize*                |Vectorized version of _convert_node function.                                                                                                          |
|**current_turn**       |*int*                      |The current turn in the game.                                                                                                                          |
|**dat_dir**            |*string*                   |Folder name containing that game instance’s telemetry files.                                                                                           |
|**debug**              |*bool*                     |This flag allows the masking of fog of war for debugging purposes.                                                                                     |
|**evgMap**             |*EvgMap*                   |This is an instance of the Everglades map.                                                                                                             |
|**focus**              |*list\<int>*               |List of group IDs on which to focus.                                                                                                                   |
|**fort_bonus**         |*int*                      |Fortress defense multiplier.                                                                                                                           |
|**map_dat**            |*dict*                     |This contains the map data read from the configuration file.                                                                                           |
|**map_key1**           |*ndarray\<int>*            |Length is the number of map nodes. Array sorted by index of evgMap node and populated by node IDs.                                                     |
|**map_key2**           |*ndarray\<int>*            |Length is the number of map nodes. Array sorted by node ID and populated by indices of evgMap nodes.                                                   |
|**output**             |*dict*                     |Key is name of telemetry file. Value is the data for that telemetry file. Also contains a header.                                                      |
|**output_dir**         |*string*                   |The destination directory for telemetry output.                                                                                                        |
|**p1_node_map**        |*list\<int>*               |Array of node IDs from player 1 perspective.                                                                                                           |
|**player_names**       |*dict*                     |This contains the names of the agent modules.                                                                                                          |
|**players**            |*dict*                     |The key is the player key (0 or 1). The value is an instance of EvgPlayer.                                                                             |
|**team_starts**        |*dict*                     |Contains team’s starting nodes, pulled from map_dat, which got it from the map json file. 0 = player 1 start, 1 = player 2 start, -1 = neutral nodes.  |
|**total_groups**       |*int*                      |Total amount of groups in the game.                                                                                                                    |
|**total_units**        |*int*                      |Total amount of units in the game.                                                                                                                     |
|**unit_dat**           |*dict*                     |Read Unit data from .json file. Contains the types and stats of the units (health, damage, speed, etc.).                                               |
|**unit_ids**           |*dict*                     |Key is int uid, the order that the types were processed, starting at 0. Value is unit_type.                                                            |
|**unit_names**         |*dict*                     |Key is unit_type. Value is int uid, the order that the types were processed, starting at 0.                                                            |
|**unit_types**         |*list\<EvgUnitDefinition>* |List of each type of unit with respective stats as retrieved from the .json file.                                                                      |
|**watch_bonus**        |*int*                      |Watchtower vision bonus.                                                                                                                               |





## Methods
[_convert_node()](../../Methods/ServerMethods/_convert_node().md)  
[board_init()](../../Methods/ServerMethods/board_init().md)  
[board_state()](../../Methods/ServerMethods/board_state().md)  
[build_knowledge_output()](../../Methods/ServerMethods/build_knowledge_output().md)  
[capture()](../../Methods/ServerMethods/capture().md)  
[combat()](../../Methods/ServerMethods/combat().md)  
[debug_state()](../../Methods/ServerMethods/debug_state().md)  
[game_end()](../../Methods/ServerMethods/game_end().md)  
[game_init()](../../Methods/ServerMethods/game_init().md)  
[game_turn()](../../Methods/ServerMethods/game_turn().md)  
[movement()](../../Methods/ServerMethods/movement().md)  
[output_init()](../../Methods/ServerMethods/output_init().md)  
[player_state()](../../Methods/ServerMethods/player_state().md)  
[unitTypes_init()](../../Methods/ServerMethods/unitTypes_init().md)  
[write_output()](../../Methods/ServerMethods/write_output().md)  
