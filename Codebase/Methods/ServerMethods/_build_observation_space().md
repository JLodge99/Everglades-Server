# build_observation_space()
This is called when the Everglades environment is initialized. It sets the boundaries and creates the observation space.

## Syntax
```python
_build_observation_space()
```

## Returns
A Box datatype with lower and upper bounds for the observations space. The boundaries are created for both groups and 
control points. These boundaries are:

#### Groups
|Field                      |Min Value  |Max Value                                                          |
|---------------------------|-----------|-------------------------------------------------------------------|
|Node Location              |1          |Number of Nodes                                                    |
|Class                      |0          |Number of Unit Classes                                             |
|Average Health             |0          |100                                                                |
|In Transit                 |0          |1                                                                  |
|Number of Units Remaining  |0          |A player's initial number of units according to game parameters.   |

#### Control Points
|Field                      |Min Value  |Max Value                                                          |
|---------------------------|-----------|-------------------------------------------------------------------|
|Is Fortress                |0          |1                                                                  |
|Is Watchtower              |0          |1                                                                  |
|Percent Controlled         |-100       |100                                                                |
|Number of Opposing Units   |-1         |A player's intitial number of units according to game parameters.  |
 
## Parameters
**None**