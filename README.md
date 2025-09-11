![Alt text](https://github.com/Smiley-Boy00/Smiley-Boy00/blob/main/Resources/Smitools_Banner.png?raw=true)
![Python](https://img.shields.io/badge/python-ffdd54?logo=python&logoColor=white) ![Autodesk Maya](https://img.shields.io/badge/Autodesk%20Maya-00AEEF?logo=autodesk&logoColor=white) ![Unreal Engine](https://img.shields.io/badge/Unreal%20Engine-0E1128?logo=unrealengine&logoColor=white) ![Latest Commit](https://img.shields.io/github/last-commit/Smiley-Boy00/smitools) ![Latest Release](https://img.shields.io/github/v/release/Smiley-Boy00/smitools) ![OS](https://img.shields.io/badge/OS-Windows-blue?logo=windows) ![Free for Commercial Use](https://img.shields.io/badge/Free%20for%20Commercial%20Use-✔-brightgreen)

## Table of Contents
- [About](#fax-about)
- [Tool Versions & Content](#bulb-tool-versions-and-content)
- [How to Install](#bookmark_tabs-sparkles-how-to-install)
- [Download Latest Release](#inbox_tray-download-latest-release)
- [Feedback](#speech_balloon-feedback)
- [Contacts](#-contacts)

## :fax: About
Smiley Tools is a python script/tool that comes packaged as a plugin for Autodesk Maya DCC with functionality to link Unreal Engine for quick export/import.

**Important**: As of the latest release, manual installation/linking is required in order for the Unreal Engine to work as desired.

## :bulb: Tool Versions and Content
### Maya Tools:
Maya to Unreal Exporter (MtoU Maya side): ver. 1.0.0
**Details**: *MtoU* allows you to directly export to your currently loaded UE project, creates a custom folder that's place inside the UE project's content folder.

Flexible Shape Creator Library (FSL): ver. 1.0.0
**Details**: *FSL* allows you to create NURBSCurve shapes for your control rigs inside Maya. Made or have a shape that isn't in the library? No worries, you can use the save shape functionality to store the shape into the library for future use.

UE Control Rig Shapes Maker & Exporter: ver. 0.2.0
**Details**: This tool allows you to convert NURBSCurve shapes made in maya into geometry shapes to be used inside Control Rigs in Unreal. Similarly to *MtoU*, it will allow you to easily export your shapes into your Unreal project with ease.

### Unreal Engine Source Code:
mtouLoader (Mtou Unreal side): ver. 1.0.0
**Details**: This script saves and stores the currently active Unreal project path, required for the exporters to run properly.

Unreal Mtou Reload Button: ver. 0.1.0
**Details**: This script creates a reload button inside Unreal Engine that executes the mtouLoader script when pressed.

## :bookmark_tabs: :sparkles: How to Install
[![Installation Video](https://img.shields.io/badge/Installation%20Video-FF0000?logo=youtube&logoColor=white)](https://youtu.be/ALA_9gwyVl4)

### Maya Side:
> - Extract **smitools** and place the folder contents into your Maya directory folder and inside your plug-ins folder, if no plug-ins folder exists create one:
**/maya/plug-ins** (this directory is usually found in the documents folder).
> - Place the icons folder inside /maya/prefs. If you already have an icons folder, place the contents inside that folder.
> - Inside Maya, go to **Windows -> Settings/Preferences -> Plug-in Manager**.
> - In the **Plug-in Manager** enable the Smiley_Tools.py plugin, a tab named "Smiley Tools" should appear where you can start using the tools.
### Unreal Side:
> - Launch the Unreal Engine project where you would like the import capability enabled and linked.
> - Go to **Settings -> Plugins**, search for **Python Editor Script Plugin** and make sure is enabled.
> - Once enabled, go to **Settings -> Project Settings -> Plugins -> Python**:
> - In **Additional Paths**, add the folder directory where the mtouLoader.py is saved in your system.
> - In **Startup Scripts**, add a section and write "mtouLoader.py" in order to load the file into the project.
> - Optionally, add a section and write "mtouReloadButton.py" in order to load the button reloader file into the project.
> - Restart your Unreal Engine Project. <br>
**Note**: This process has to be set for every project you would like to enable the loader module.

## :inbox_tray: Download Latest Release

:rocket: **Grab the Latest Build Here:**  

[![Download Release](https://img.shields.io/github/v/release/Smiley-Boy00/smitools?label=Download&color=blue)](https://github.com/Smiley-Boy00/smitools/releases/latest)  

> 📦 Current Version: **v0.1.1**  
> 🛠 This tool is in **Alpha** — expect changes and possible bugs as I add new features and improve workflows.  
> ✅ **Free for Commercial Use** — This tool can be used for both personal and professional projects without restrictions.  

**Download Notes:**  
- Alpha builds may have partial or experimental features.  
- Manual setup is required for Unreal Engine linkage (see [How to Install](#-how-to-install)).  
- Feedback and bug reports are encouraged to help improve stability.  

## :speech_balloon: Feedback  

We welcome contributions, bug reports, and feature requests!  
If you encounter a problem or have an idea for improvement:  
1. Open an **[Issue](https://github.com/Smiley-Boy00/smitools/issues)** describing your problem, suggestion, or request.  
2. Include as much detail as possible — logs, screenshots, reproduction steps.  
3. If you're a developer, feel free to submit a **Pull Request** with proposed changes.  

💡 Your feedback will influence future releases!  

## 📇 Contacts  

Want to connect, ask a question, or collaborate? Here's how to reach me:  

- 📧 **Email:** david.e.margon@hotmail.com  
- 💬 **Discord:** `smiley_boy`  
- 🌐 **Portfolio / Website:** [Artstation](https://www.artstation.com/david_martinez)  
