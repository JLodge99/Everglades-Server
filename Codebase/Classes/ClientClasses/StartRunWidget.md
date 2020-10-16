# StartRunWidget
This widget allows the user to select inputs for running a match on the server.  

**Class Type**&nbsp; &nbsp; &nbsp; &nbsp; Blueprint  
**Parent Class** &nbsp; &nbsp; evgUserWidget  

## Variables
|Variable                   |Type               |Description                                                                                                    |
|---------------------------|-------------------|---------------------------------------------------------------------------------------------------------------|
|**AwaitingText**           |*TextBlock*        |"Awaiting results..."                                                                                          |
|**Border_ContinueBTN**     |*Border*           |Continue button border.                                                                                        |
|**Btn_Back_ServerRunning** |*Button*           |The button to go back instead of running server.                                                               |
|**CancelButton**           |*Button*           |The button to go back to the main menu.                                                                        |
|**Continue_BTN**           |*Button*           |The button to run a match playback after the servers have finished.                                            |
|**Divider**                |*Image*            |A thin bar separating the top and bottom halves of the settings panel.                                         |
|**GraphicalHelper**        |*Image*            |An aesthetic hexagon image.                                                                                    |
|**GraphicalHelper_SR**     |*Image*            |An aesthetic hexagon image.                                                                                    |
|**Housing**                |*Image*            |An image to house the settings panel.                                                                          |
|**Housing_Running**        |*Image*            |An image to house the loading panel.                                                                           |
|**ListHousing**            |*Image*            |Image to house the server running results.                                                                     |
|**LoadingBar**             |*ProgressBar*      |Bar showing the running server progress.                                                                       |
|**LoadingPanel**           |*CanvasPanel*      |Canvas for displaying the server running portion of the widget.                                                |
|**LoadingText**            |*TextBlock*        |Text displaying a ratio of the current run number over the total number of runs desired.                       |
|**Map_Name_ComboBox**      |*ComboBoxString*   |Drop-down for selecting which map to use (e.g., "Random").                                                     |
|**Player0_AI_ComboBox**    |*ComboBoxString*   |Drop-down for selecting Player 0's AI script (often referenced as Player 1 or Blue Team in Unreal blueprints). |
|**Player1_AI_Combobox**    |*ComboBoxString*   |Drop-down for selecting Player 1's AI script (often referenced as Player 1 or Red Team in Unreal blueprints).  |
|**pythonPath**             |*EditableTextBox*  |The text box where the user inputs the full path to their *python.exe* file.                                   |
|**REF_Run**                |*Image*            |Reference image for "run server".                                                                              |
|**REF_ServerRunning**      |*Image*            |Reference image for "server running".                                                                          |
|**ResultsText**            |*TextBlock*        |Text shows the results of each match that was run.                                                             |
|**RunButton**              |*Button*           |The button that runs the matches according to the selected options.                                            |
|**runs**                   |*EditableTextBox*  |The text box where the user inputs the number of desired runs.                                                 |
|**RunServer_Intro**        |*WidgetAnimation*  |The animation related to "run server".                                                                         |
|**serverPath**             |*EditableTextBox*  |The text box where the user inputs the full path to the Everglades server.                                     |
|**ServerRunning_Intro**    |*WidgetAnimation*  |The animation related to "server running".                                                                     |
|**SettingsPanel**          |*CanvasPanel*      |Canvas for displaying the run server portion of the widget.                                                    |

## Functions
[**Get_LoadingBar_Percent_0**](../../Methods/ClientMethods/Get_LoadingBar_Percent_0.md)  

## Events
[**Event Add Results**](../../Events/AddResults.md)  
[**Event Construct**](../../Events/Construct_StartRunWidget.md)  
[**Event Tick**](../../Events/Tick_StartRunWidget.md)  
[**On Clicked(CancelButton)**](../../Events/Clicked_CancelButton_StartRunWidget.md)  
[**On Clicked(Continue_BTN)**](../../Events/Clicked_Continue_BTN.md)  
[**On Clicked(RunButton)**](../../Events/Clicked_RunButton.md)  
[**ResetView**](../../Events/ResetView.md)  

## Event Dispatchers
[**CancelClicked**](../../Dispatchers/CancelClicked.md)  
[**RunClicked**](../../Dispatchers/RunClicked.md)  
[**ServersFinished**](../../Dispatchers/ServersFinished.md)  

## Macros
[**ResultsTextBuilder**](../../Macros/ResultsTextBuilder.md)  