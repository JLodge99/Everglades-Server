# EvergladesGameMode
This class is the "main" class of the Everglades client and drives events
and controls playback of the Everglades match.

**Class Type**&nbsp; &nbsp; &nbsp; &nbsp; Blueprint  
**Parent Class** &nbsp; &nbsp; GameModeBase  

## Variables
|Variable                   |Type                               |Description                                                                                |
|---------------------------|-----------------------------------|-------------------------------------------------------------------------------------------|
|**ActiveGroups**           |*Array\<SwarmGroup*\>              |The player groups in the game.                                                             |
|**AITimer**                |*Timer Handle*                     |A reference used to clear the timer. The timer is used for repeated calls to UpdateCamAI.  |
|**CamTargetGroup**         |*SwarmGroup*                       |The swarm for the TrackSwarm camera to follow.                                             |
|**CurrentFocusGroup**      |*SwarmGroup*                       |The swarm for the ArenaCam to follow.                                                      |
|**CurrentFocusGroupID**    |*Integer*                          |The ID of the swarm for the ArenaCam to follow.                                            |
|**CurrentTurn**            |*Integer*                          |The number of the current turn.                                                            |
|**DefaultSceneRoot**       |*SceneComponent*                   |The default root component.                                                                |
|**DefaultViewTarget**      |*Actor*                            |The Actor the player is looking at.                                                        |
|**Events**                 |*Evg Events*                       |This contains the events described in the telemetry files.                                 |
|**EventsCompleted**        |*Integer*                          |The number of events completed.                                                            |
|**EventsSent**             |*Integer*                          |The number of events that have been processed.                                             |
|**FolderName**             |*String*                           |The name of the match to run.                                                              |
|**GameResultString**       |*String*                           |A string stating the match winner and final scores for each player.                        |
|**GameStateRef**           |*EvergladesGameState*              |A reference to the Everglades game state.                                                  |
|**HUDRandomRef**           |*SpectatorHUD_Random*              |A reference to *SpectatorHUD_Random*.                                                      |
|**HUDRef**                 |*SpectatorHUD*                     |A reference to *SpectatorHUD*.                                                             |
|**ImagesRemaining**        |*Integer*                          |                                                                                           |
|**ImageURLs**              |*Array\<String\>*                  |The addresses and names of image files from the match folder.                              |
|**LoadingIndex**           |*Integer*                          |The index in the *ImageURLs* array.                                                        |
|**MainMenuRef**            |*MainMenu*                         |A reference to the *MainMenu* widget.                                                      |
|**MapNodes**               |*Integer*                          |                                                                                           |
|**MapVisible**             |*Boolean*                          |This states whether the large map has been toggled and is visible.                         |
|**MatchStarted**           |*Boolean*                          |This states whether the match has begun.                                                   |
|**NodeCombat**             |*Array\<NodeCombatState\>*         |                                                                                           |
|**NodeControl**            |*Array\<Float\>*                   |The percentages of nodes that Player 1 and Player 2 control.                               |
|**NodePoints**             |*Array\<NodePoint\>*               |An array of nodes (i.e. *NodePoint* objects)                                               |
|**NumUnits**               |*Array\<Integer\>*                 |The amount of each player's active units.                                                  |
|**P0_TurnImages**          |*Map\<Integer, Texture2DDynamic\>* |A map of Player 1's turn number to an image.                                               |
|**P1Score**                |*Integer*                          |Player 1's score.                                                                          |
|**P1_TurnImages**          |*Map\<Integer, Texture2DDynamic\>* |A map of Player 2's turn number to an image.                                               |
|**P2Score**                |*Integer*                          |Player 2's score.                                                                          |
|**SimplifiedMap**          |*Boolean*                          |This is set based on the *SimplifiedMap* checkbox on the UI.                               |
|**SimplifiedMapSequence**  |*LevelSequenceActor*               |This is a reference to the *SimplifiedMap* level sequence.                                 |
|**SpectatorPawn**          |*EvergladesSpectatorPawn*          |A reference to *EvergladesSpectatorPawn* object.                                           |
|**TurnComplete**           |*Boolean*                          |This states whether the turn is finished.                                                  |
|**TurnImages**             |*Array\<Texture2DDynamic\>*        |                                                                                           |
|**Units**                  |*Array\<SwarmUnit\>*               |A collection of swarm units.                                                               |
|**UseCamAI**               |*Boolean*                          |This is used to toggle between free cam and AI cam.                                        |
|**UsingFollow**            |*Boolean*                          |This indicates if the camera is tracking a swarm.                                          |

## Functions
[**CalculateNodeControl**](../../Methods/ClientMethods/CalculateNodeControl.md)  
[**ConstructionScript**](../../Methods/ClientMethods/ConstructionScript_EvergladesGameMode.md)  
[**CreateGroup**](../../Methods/ClientMethods/CreateGroup.md)  
[**GetAvailableMoveNode**](../../Methods/ClientMethods/GetAvailableMoveNode.md)  
[**GetConnectionSpline**](../../Methods/ClientMethods/GetConnectionSpline.md)  
[**GetGroup**](../../Methods/ClientMethods/GetGroup.md)  
[**GetNode**](../../Methods/ClientMethods/GetNode.md)  
[**GetNumPlayerUnits**](../../Methods/ClientMethods/GetNumPlayerUnits.md)  
[**GetTeamMV**](../../Methods/ClientMethods/GetTeamMV.md)  
[**GetUnit**](../../Methods/ClientMethods/GetUnit_GameMode.md)  
[**LogMapData**](../../Methods/ClientMethods/LogMapData.md)  
[**RemoveGroup**](../../Methods/ClientMethods/RemoveGroup.md)  
[**RemovePlayerUnit**](../../Methods/ClientMethods/RemovePlayerUnit.md)  

## Events
[**AddHUD**](../../Events/AddHUD.md)  
[**AddUnit**](../../Events/AddUnit_GameMode.md)  
[**ArrivedEvent**](../../Events/ArrivedEvent_EvergladesGameMode.md)  
[**DebugWinner**](../../Events/DebugWinner.md)  
[**EndMatch**](../../Events/EndMatch.md)  
[**Event BeginPlay**](../../Events/BeginPlay_EvergladesGameMode.md)  
[**Event Tick**](../../Events/Tick_EvergladesGameMode.md)  
[**InTransitEvent**](../../Events/InTransitEvent.md)  
[**LoadEvents**](../../Events/LoadEvents.md)  
[**LoadImages**](../../Events/LoadImages.md)  
[**OnEventCompleted**](../../Events/OnEventCompleted.md)  
[**ProcessCombatEvent**](../../Events/ProcessCombatEvent.md)  
[**ProcessNodeControlUpdate**](../../Events/ProcessNodeControlUpdate.md)  
[**ProcessTransferUnitsUpdate**](../../Events/ProcessTransferUnitsUpdate.md)  
[**RdyToMoveEvent**](../../Events/RdyToMoveEvent.md)  
[**RunEvents**](../../Events/RunEvents.md)  
[**SetArenaCamTarget**](../../Events/SetArenaCamTarget.md)  
[**SetFocusGroup**](../../Events/SetFocusGroup.md)  
[**SetFollowCam**](../../Events/SetFollowCam.md)  
[**SetFreeCam**](../../Events/SetFreeCam.md)  
[**StartCamAI**](../../Events/StartCamAI.md)  
[**StopCamAI**](../../Events/StopCamAI.md)  
[**TickCam**](../../Events/TickCam.md)  
[**ToggleCamAI**](../../Events/ToggleCamAI.md)  
[**ToggleMap**](../../Events/ToggleMap.md)  
[**ToggleSimplifiedMap**](../../Events/ToggleSimplifiedMap_EvergladesGameMode.md)  
[**TurnPauseToggle**](../../Events/TurnPauseToggle.md)  
[**TurnTimeout**](../../Events/TurnTimeout.md)  
[**UpdateCamAI**](../../Events/UpdateCamAI.md)  

## Event Dispatchers
[**ChangeCamMode**](../../Dispatchers/ChangeCamMode.md)  
[**ImageLoadComplete**](../../Dispatchers/ImageLoadComplete.md)  

## Macros
[**GetGroup_Macro**](../../Macros/GetGroup_Macro.md)  
[**GetLastIndex**](../../Macros/GetLastIndex.md)  
[**IDExists**](../../Macros/IDExists.md)  
[**ImageURLProcessing**](../../Macros/ImageURLProcessing.md)  
[**Message_CombatUpdate**](../../Macros/Message_CombatUpdate.md)  
[**Message_ControlUpdate**](../../Macros/Message_ControlUpdate.md)  
[**Message_CreateNewGroup**](../../Macros/Message_CreateNewGroup.md)  
[**Message_Disband**](../../Macros/Message_Disband.md)  
[**Message_Init**](../../Macros/Message_Init.md)  
[**Message_Move**](../../Macros/Message_Move.md)  
[**Message_Scores**](../../Macros/Message_Scores.md)  
[**Message_TransferUnits**](../../Macros/Message_TransferUnits.md)  
[**ParsePosition**](../../Macros/ParsePosition.md)  
[**ParseScoreString**](../../Macros/ParseScoreString.md)  