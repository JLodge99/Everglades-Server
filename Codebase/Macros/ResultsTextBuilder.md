# ResultsTextBuilder
Creates a single match result string from an array of strings related to the result.  

Target is *StartRunWidget*.  

## Node

## Inputs
|Name       |Type               |Description                                                        |
|-----------|-------------------|-------------------------------------------------------------------|
|**Array**  |*Array\<String\>*  |String elements are Player 0 score, Player 1 score, and win type.  |
|**self**   |*Text*             |A reference to the *ResultsText* variable.                         |

## Outputs
|Name           |Type   |Description                                    |
|---------------|-------|-----------------------------------------------|
|**ReturnValue**|*Text* |A single string containing the match results.  |