# Everglades-Server
# Installation Instructions
## Dependencies
Everglades runs in a Python3 environment. Ensure the python packages ***gym***,  ***numpy***, ***pandas***, ***noise***, ***matplotlib*** are installed. This can be done with:
```bash
$ pip install numpy
$ pip install gym
$ pip install pandas
$ pip install noise
$ pip install matplotlib
```
If your computing environment requires it, make sure to include the --cert and --proxy flags with the pip commands.

Noise has a C++ dependencies so if it flags an error while pip install then download the dependencies from the [MS C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

## Installation
From the root Everglades directory, install the Everglades environment with:
```bash
pip install -e gym-everglades/
```
Next, install the Everglades server with:
```bash
pip install -e everglades-server/
```
Finally, edit the ***config\GameSetup.json*** file to reflect the current working environment. Edit any of the entries to the desired configuration.

# File and Directory Descriptions

### ./agents/

This is a common directory where any created agents for the Everglades game can be stored. Some example files are included with the package.

### ./Codebase/

This directory hold markdown files for all of the server attributes such has methods and variables.

### ./config/

This directory contains setup files which are used for game logic. It contains the entire loadout JSON system, GameSetup.json which is used to configure game instances with the desired settings, and Map.json which holds the map.

### ./everglades-server/

This directory contains the main logic for the Everglades game.

### ./game_telemetry/

This is the default output directory for any match telemetry output. It is only populated locally and not stored in the git repository.

### ./gym-everglades/

This directory is the OpenAI Gym for project Everglades. It follows the Gym API standards.

### ./testing/

This directory holds scripts primarily for testing and debugging combat.

### ./ui/

This directory holds UI scripts to generate custom loadouts, units, and attributes.

### ./testbattle.py

This is the script to execute for running two agents against each other.

### ./testcombat.py

This script always ensures that combat happens for testing purposes.

### ./README.md

This file, explaining important directory structure and installation requirements.

### ./.gitignore

This file tells git to ignore compiled files and telemetry output.