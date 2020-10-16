# SpectatorHUD
The HUD that is present during an Everglades match playback using the default map.  

**Class Type**&nbsp; &nbsp; &nbsp; &nbsp; Blueprint  
**Parent Class** &nbsp; &nbsp; User Widget  

## Variables
|Variable                   |Type                       |Description                                                        |
|---------------------------|---------------------------|-------------------------------------------------------------------|
|**Arena_Scrollbox**        |*ScrollBox*                |*unused*                                                           |
|**Arenas_Btn**             |*Button*                   |*unused*                                                           |
|**BlueBase**               |*Image*                    |The blue house icon on the minimap.                                |
|**BlueTeam_MV**            |*Image*                    |Blue team's machine vision image.                                  |
|**BottomBar**              |*Image*                    |Aesthetic bar at bottom of HUD.                                    |
|**BottomTextHolder**       |*Image*                    |Aesthetic bar behind text at bottom of HUD.                        |
|**Btn_Maximize**           |*Button*                   |The button that shows the large map.                               |
|**Btn_Pause**              |*Button*                   |The button that pauses playback.                                   |
|**CameraSidebar_Slide**    |*WidgetAnimation*          |*unused*                                                           |
|**ExitButton**             |*Button*                   |The button to exit the game.                                       |
|**GameModeRef**            |*EverGladesGameMode*       |A reference to the game mode.                                      |
|**Group_ScrollBox**        |*ScrollBox*                |*unused*                                                           |
|**Groups_Btn**             |*Button*                   |*unused*                                                           |
|**HUD_LargeMap**           |*HUD_LargeMap*             |A *HUD_LargeMap* reference.                                        |
|**HUD_MiniMap_Zone_A**     |*HUD_MiniMap_Zone*         |An initially neutral node on the minimap.                          |
|**HUD_MiniMap_Zone_B**     |*HUD_MiniMap_Zone*         |An initially neutral node on the minimap.                          |
|**HUD_MiniMap_Zone_Base_1**|*HUD_MiniMap_Zone*         |Player 1's base node on the minimap.                               |
|**HUD_MiniMap_Zone_Base_2**|*HUD_MiniMap_Zone*         |Player 2's base node on the minimap.                               |
|**HUD_MiniMap_Zone_C**     |*HUD_MiniMap_Zone*         |An initially neutral node on the minimap.                          |
|**HUD_MiniMap_Zone_D**     |*HUD_MiniMap_Zone*         |An initially neutral node on the minimap.                          |
|**HUD_MiniMap_Zone_E**     |*HUD_MiniMap_Zone*         |An initially neutral node on the minimap.                          |
|**HUD_MiniMap_Zone_F**     |*HUD_MiniMap_Zone*         |An initially neutral node on the minimap.                          |
|**HUD_MiniMap_Zone_G**     |*HUD_MiniMap_Zone*         |An initially neutral node on the minimap.                          |
|**HUD_MiniMap_Zone_H**     |*HUD_MiniMap_Zone*         |An initially neutral node on the minimap.                          |
|**HUD_MiniMap_Zone_I**     |*HUD_MiniMap_Zone*         |An initially neutral node on the minimap.                          |
|**HUD_UnitLoss_Blue**      |*HUD_UnitLoss*             |An instance of *HUD_UnitLoss* for the blue team.                   |
|**HUD_UnitLoss_Red**       |*HUD_UnitLoss*             |An instance of *HUD_UnitLoss* for the red team.                    |
|**HUD_Winner**             |*HUD_Winner*               |A *HUD_Winner* reference.                                          |
|**LargeMap**               |*WidgetAnimation*          |Animation for opening and closing the large map.                   |
|**LargeMap_Visible**       |*Boolean*                  |Whether the large map is visible.                                  |
|**MachineVisionPanel**     |*CanvasPanel*              |A canvas for machine vision.                                       |
|**Map**                    |*Image*                    |The 2D terrain image of the minimap.                               |
|**MapWorldAnchor_BR**      |*Vector*                   |The position of the bottom-right world anchor.                     |
|**MapworldAnchor_TL**      |*Vector*                   |The position of the top-left world anchor.                         |
|**MiniMap_Base**           |*Image*                    |An aesthetic background image behind the minimap.                  |
|**MV_Toggle**              |*Button*                   |Toggles the machine vision panel.                                  |
|**PauseButtonStyle**       |*ButtonStyle Struct*       |The style of the pause button.                                     |
|**PlayButtonStyle**        |*ButtonStyle Struct*       |The style of the play button.                                      |
|**Player1_ZoneControl**    |*ProgressBar*              |Indirectly used for rotating *ZoneControl_Fill                     |
|**Player2_ZoneControl**    |*ProgressBar*              |Indirectly used for rotating *ZoneControl_Fill                     |
|**PlayerPawn**             |*EvergladesSpectatorPawn*  |An *EvergladesSpectatorPawn* reference.                            |
|**RedBase**                |*Image*                    |The red house icon on the minimap.                                 |
|**RedTeam_MV**             |*Image*                    |Red team's machine vision image.                                   |
|**ReturnMenu**             |*Button*                   |Button to return to the main menu.                                 |
|**ScoreAndUnitsHousing**   |*Image*                    |An image that houses the score and units.                          |
|**SidebarState**           |*Integer*                  |*unused*                                                           |
|**SideDetail**             |*Image*                    |An aesthetic image on the right side of the HUD.                   |
|**Side_Detail_L**          |*Image*                    |An aesthetic image on the left side of the HUD.                    |
|**StateText**              |*Text*                     |*unused*                                                           |
|**Team1_LastUnits**        |*Integer*                  |The amount of units Team 1 had previously.                         |
|**Team2_LastUnits**        |*Integer*                  |The amount of units Team 2 had previously.                         |
|**Team1UnitText**          |*Text*                     |The amount of Team 1's active units.                               |
|**Team2UnitText**          |*Text*                     |The amount of Team 2's active units.                               |
|**Time_Housing**           |*Image*                    |An image that houses the match timer.                              |
|**Timeline**               |*ProgressBar*              |A progress bar at the bottom of the HUD related to the match time. |
|**TopBar**                 |*Image*                    |An aesthetic bar on the top of the HUD.                            |
|**ZoneControl_Fill**       |*Image*                    |A red and blue image used for filling the zone control indicator.  |
|**ZoneControl_Housing**    |*Image*                    |An image used to house the zone control indicator.                 |
|**ZoneControl_Tine**       |*Image*                    |A triangle image used as a marker on the zone control indicator.   |

## Functions
[**GetBlueTeamMV_Turn**](../../Methods/ClientMethods/GetBlueTeamMV_Turn.md)  
[**GetCameraText**](../../Methods/ClientMethods/GetCameraText.md)  
[**GetPlayer1Score**](../../Methods/ClientMethods/GetPlayer1Score.md)  
[**GetPlayer2Score**](../../Methods/ClientMethods/GetPlayer2Score.md)  
[**GetPlayer1ZoneControlPercent**](../../Methods/ClientMethods/GetPlayer1ZoneControlPercent.md)  
[**GetPlayer2ZoneControlPercent**](../../Methods/ClientMethods/GetPlayer2ZoneControlPercent.md)  
[**GetRedTeamMV_Turn**](../../Methods/ClientMethods/GetRedTeamMV_Turn.md)  
[**GetTeam1UnitText**](../../Methods/ClientMethods/GetTeam1UnitText.md)  
[**GetTeam2UnitText**](../../Methods/ClientMethods/GetTeam2UnitText.md)  
[**GetTimelinePercent**](../../Methods/ClientMethods/GetTimelinePercent.md)  
[**GetTurnText**](../../Methods/ClientMethods/GetTurnText.md)  
[**GetWinText**](../../Methods/ClientMethods/GetWinText.md)  

## Events
[**Event Construct**](../../Events/Construct_SpectatorHUD.md)  
[**Event Tick**](../../Events/Tick_SpectatorHUD.md)  
[**GetPlayerPawn**](../../Events/GetPlayerPawn.md)  
[**HideMap**](../../Events/HideMap.md)  
[**Map_SetNodes**](../../Events/Map_SetNodes.md)  
[**On Clicked(Btn_Maximize)**](../../Events/Clicked_Btn_Maximize.md)  
[**On Clicked(Btn_Pause)**](../../Events/Clicked_Btn_Pause.md)  
[**On Clicked(ExitButton)**](../../Events/Clicked_ExitButton_SpectatorHUD.md)  
[**On Clicked(MV_Toggle)**](../../Events/Clicked_MV_Toggle.md)  
[**On Clicked(ReturnMenu)**](../../Events/Clicked_ReturnMenu.md)  
[**RemoveGroupIndicator**](../../Events/RemoveGroupIndicator.md)  
[**ToggleSimplifiedMap**](../../Events/ToggleSimplifiedMap_SpectatorHUD.md)  
[**Winner**](../../Events/Winner.md)  

## Event Dispatchers
**None**

## Macros
[**GetZoneControlAngle**](../../Macros/GetZoneControlAngle.md)  
[**WorldPosToMapPos**](../../Macros/WorldPosToMapPos.md)  