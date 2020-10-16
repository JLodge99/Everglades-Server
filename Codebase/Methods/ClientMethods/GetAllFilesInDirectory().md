# GetAllFilesInDirectory()
Gets all the files in a given directory.  
## Syntax
```cpp
GetAllFilesInDirectory( const FString directory,
                        const bool fullPath = true,
                        const FString onlyFilesStartingWith = TEXT(""),
                        const FString onlyFilesEndingWith = TEXT(""))
```

## Returns
A list of files including extensions.  

## Parameters
|Parameter                  |Description                                                                            |
|---------------------------|---------------------------------------------------------------------------------------|
|**directory**              |The full path of the directory to iterate.                                             |
|**fullPath**               |*Optional*. Return full path of file or just filename. Default is *True*.              |
|**onlyFilesStartingWith**  |*Optional*. Search only for files starting with the specified string. Default is ""    |
|**onlyFilesEndingWith**    |*Optional*. Search only for files ending with the specified extension. Default is "".  |