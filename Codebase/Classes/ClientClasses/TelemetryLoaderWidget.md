# TelemetryLoaderWidget
This widget is used for displaying and loading the telemetry files.  

**Class Type**&nbsp; &nbsp; &nbsp; &nbsp; Blueprint  
**Parent Class** &nbsp; &nbsp; User Widget  

## Variables
|Variable               |Type               |Description                                |
|-----------------------|-------------------|-------------------------------------------|
|**CancelButton**       |*Button*           |The "back" button.                         |
|**FileListHousing**    |*Image*            |A black background for the listed files.   |
|**FilesScrollBox**     |*ScrollBox*        |A scroll box for the listed files          |
|**Folders**            |*Array\<String\>*  |The available telemetry folders.           |
|**GraphicalHelper**    |*Image*            |An aesthetic hexagon image.                |
|**Housing**            |*Image*            |A dark background image.                   |
|**LoadButton**         |*Button*           |The "Load" button.**Unused*                |
|**OpenButton**         |*Button*           |The "Open Folder" button.                  |
|**REF_Telemetry**      |*Image*            |A reference image for this widget.         |
|**SimplifiedMapCheck** |*CheckBox*         |The "SimplifiedMap" checkbox.              |
|**Telemetry_Intro**    |*WidgetAnimation*  |An animation for this widget.              |

## Functions
**None**

## Events
[**Event Construct**](../../Events/Construct_TelemetryLoaderWidget.md)  
[**LoadTelemetry**](../../Events/LoadTelemetry.md)  
[**On Check State Changed(SimplifiedMapCheck)**](../../Events/CheckStateChanged_SimplifiedMapCheck.md)  
[**On Clicked(CancelButton)**](../../Events/Clicked_CancelButton_TelemetryLoaderWidget.md)  
[**On Clicked(LoadButton)**](../../Events/Clicked_LoadButton.md)  
[**On Clicked(OpenButton)**](../../Events/Clicked_OpenButton.md)  
[**ReloadTelemetryFolders**](../../Events/ReloadTelemetryFolders.md)  

## Event Dispatchers
[**CancelClicked**](../../Dispatchers/CancelClicked.md)  
[**LoadClicked**](../../Dispatchers/LoadClicked.md)  

## Macros
**None**