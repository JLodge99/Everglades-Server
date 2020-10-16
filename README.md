# Everglades-Server
# Installation Instructions
## Dependencies
Everglades runs in a Python3 environment. Ensure the python packages ***gym*** and ***numpy*** are installed. This can be done with:
```bash
$ pip install numpy
$ pip install gym
```
If your computing environment requires it, make sure to include the --cert and --proxy flags with the pip commands.

## Installation
From the root Everglades directory, install the Everglades environment with:
```bash
pip install -e gym-everglades/
```
Next, install the Everglades server with:
```bash
pip install -e everglades-server/
```
Finally, edit the ***test_battle.py*** script to reflect the current working environment. Update the following lines with their path in the filesystem:
*  agent 0 file
*  agent 1 file
*  config directory
*  output directory

# File and Directory Descriptions

### ./agents/

This is a common directory where any created agents for the Everglades game can be stored. Some example files are included with the package.

### ./config/

This directory containes setup files which are used for game logic. Currently only the DemoMap.json and UnitDefinitions.json files are used for gameplay. They can be swapped for files defining a different map or units, but note that any swaps likely will cause inflexible server logic to break.

### ./everglades-server/

This directory contains the main logic for the Everglades game. 

### ./game_telemetry/

This is the default output directory for any match telemetry output. It is only populated locally and not stored in the git repository.

### ./gym-everglades/

This directory is the OpenAI Gym for project Everglades. It follows the Gym API standards.

### ./test_battle.py

This is the script to execute for running two agents against each other.

### ./README.md

This file, explaining important directory structure and installation requirements.

### ./.gitignore

This file tells git to ignore compiled files and telemetry output. 