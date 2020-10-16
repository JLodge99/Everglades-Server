# MainMenu
The Everglades main menu widget.  

**Class Type**&nbsp; &nbsp; &nbsp; &nbsp; Blueprint  
**Parent Class** &nbsp; &nbsp; User Widget  

## Variables
|Variable                       |Type                   |Description                                                |
|-------------------------------|-----------------------|-----------------------------------------------------------|
|**BG**                         |*FontEndBG*            |The menu's background.                                     |
|**Border_Exit_Button**         |*Border*               |The *ExitButton*'s border.                                 |
|**Border_LoadTelemetry_Button**|*Border*               |The *LoadTelemetry_Button*'s border.                       |
|**Border_RunServer_Button**    |*Border*               |The *RunServer_Button*'s border.                           |
|**Dimmer**                     |*Image*                |Black image that fades in when *Fade* animation occurs.    |
|**ExitButton**                 |*Button*               |The button for exiting the game.                           |
|**Fade**                       |*WidgetAnimation*      |Animation appears to fade *MainMenu* to black.             |
|**FadeInvis**                  |*WidgetAnimation*      |Animation fades *TelemetryLoader* and *BG* to invisible.   |
|**FrontEndBG**                 |*FrontEndBG*           |*Not used*                                                 |
|**GameModeRef**                |*EvergladesGameMode*   |A reference to the game mode.                              |
|**GraphicalHelper**            |*Image*                |A hexagon image.                                           |
|**LoadingCanvas**              |*CanvasPanel*          |Canvas where loading progress appears.                     |
|**LoadingProgress**            |*ProgressBar*          |Bar denoting the loading progress.                         |
|**LoadTelemetry_Button**       |*Button*               |The button for loading telemetry files.                    |
|**Logo_CubicIntific**          |*Image*                |The Cubic Intific logo.                                    |
|**Logo_Lockheed**              |*Image*                |The Lockheed Martin logo.                                  |
|**MainMenu_Intro**             |*WidgetAnimation*      |The animation                                              |
|**Parent**                     |*CanvasPanel*          |The canvas for the main menu.                              |
|**RunServer_Button**           |*Button*               |The button for running a match.                            |
|**StartRunWidget**             |*StartRunWidget*       |The *StartRun* widget.                                     |
|**TelemetryLoader**            |*TelemetryLoaderWidget*|The *TelemetryLoader* widget.                              |
|**TextBlock_61**               |*TextBlock*            |"Project Everglades" text.                                 |

## Functions
[**Get_LoadingProgress_Percent_0**](../../Methods/ClientMethods/Get_LoadingProgress_Percent_0.md)  

## Events
[**AddedToViewport**](../../Events/AddedToViewport.md)  
[**BackToMainMenu**](../../Events/BackToMainMenu.md)  
[**Event Construct**](../../Events/Construct_MainMenu.md)  
[**LoadLevel**](../../Events/LoadLevel.md)  
[**On Clicked(ExitButton)**](../../Events/Clicked_ExitButton_MainMenu.md)  
[**On Clicked(LoadTelemetry_Button)**](../../Events/Clicked_LoadTelemetry_Button.md)  
[**On Clicked(RunServer_Button)**](../../Events/Clicked_RunServer_Button.md)  
[**RunClicked**](../../Events/RunClicked.md)  
[**RunLevel**](../../Events/RunLevel.md)  
[**RunTransistion**](../../Events/RunTransition.md)  

## Event Dispatchers
**None**

## Macros
**None**