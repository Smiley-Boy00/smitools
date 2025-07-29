# Smiley Tools v0.1.0 for Autodesk Maya & Unreal Engine

Smiley Tools is a script/tool package that comes as a plugin for Autodesk Maya DCC with linking for quick export/import for Unreal Engine.
Note: As of the current version, some manual installation/linking is required in order for the Unreal Engine to work as expected. 

## Included tools and current versions
### Maya Source Code:
Maya to Unreal Exporter (MtoU Maya side): ver. 1.0<br />
Flexible Shape Creator Library (FLS): ver. 1.0<br />
UE Control Rig Shapes Maker & Exporter: ver. 0.2.0<br />

### Unreal Engine Source Code:
Maya to Unreal Loader (Mtou Unreal side): ver. 0.1.0<br />
Unreal Mtou Reload Button: ver. 0.1.0<br />

## Installation Process:
- Download the smitools.zip file and extract its contents
### Maya Side:
- Place the folder contents into your Maya directory folder and inside your plug-ins folder, if no plug-ins folder exists create one: <br />
  /maya/plug-ins (the maya folder is usually found in the documents folder).<br />
  IMPORTANT: Do not place the smitools folder itself, just its contents.
- Inside Maya, go to Windows -> Settings/Preferences -> Plug-in Manager.<br />
  In the Plug-in Manager enable the Smiley_Tools.py plugin, a tab named "Smiley Tools" should appear where you can start using the tools.
### Unreal Side:
- Launch the Unreal Engine project where you would like the import capability enabled and linked.
- Go to Settings -> Plugins, search for Python Editor Script Plugin and make sure is enabled.
- Once enabled, go to Settings -> Project Settings -> Plugins -> Python:<br />
  In Additional Paths, add the folder directory where the mtouLoader.py is saved in your system.<br />
  In Startup Scripts, add a section and write "mtouLoader.py" in order to load the file into the project.<br />
  Optionally, add a section and write "mtouReloadButton.py" in order to load the button reloader file into the project.<br />
- Restart your Unreal Engine Project.<br />
Note: This procress has to be set for every project you would like to enable the loader module.

