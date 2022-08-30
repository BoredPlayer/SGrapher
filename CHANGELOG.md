# Change log

## v. 0.2.4 - And the updates kept coming...
30.08.2022

This is a big one - finally the legend editing has some meaningful updates! Since this version, you can edit line width and opacity. However, you don't have to do it with those pesky buttons at the bottom of the window anymore! **Just doubleclick at the value you want to change and write whatever you need there to be**! No strings attached, at least that I know of. Keep an eye on the `Known bugs` section.

This means, that the `Better legend editing` milestone is finally achieved! :tada:

This version required some changes to `matgrapher` library, so please, update it with whatever method you find the most suitable or with pip command:
```python
pip install git+https://github.com/BoredPlayer/matgrapher.git
```

Bug fixes:\
-> _No bugs were harmed during making of this update._

Known bugs:
-> Coding of project may break cross-platform compatibility. It is recommended to convert all projects to UTF-8.

Next milestones:\
-> Project autosaving (general),\
-> Grid options (Graph tab),\
-> Project settings and files in form of zip files,\
-> Full documentation in form of a README file.

## v. 0.2.3a - multiplatform hotfix
30.08.2022

This version is a result of a realisation, that `python` and `python3` are completly separate things in most of linux distros. It fixes graphing engine execution on linux. Moreover, the `=` sign will no longer break graph title while reloading project.

Bugfixes:
-> Graphing engine execution is now os-dependant\
-> Title no longer broken by `=` sign.

Known bugs:
-> Coding of project may break cross-platform compatibility. It is recommended to convert all projects to UTF-8.

Next milestones:\
-> Project autosaving (general),\
-> Grid options (Graph tab),\
-> Better legend editing (Legend tab),\
-> Project settings and files in form of zip files,\
-> Full documentation in form of a README file.

## v. 0.2.3 - Quality of life update
30.08.2022

This version fixes major bugs in `Graph settings` and `Legend settings` tabs. Also, the project is now cleared during loading of a new `.sgp` file. New milestone achieved! :tada:\
Another upgrade is, that the file selection will be performed with native file dialog, which I often find much easier to use, than Qt5's one.

Bug fixes:\
-> No more crashing file emptying `Graph width` and `Graph heights` text boxes,\
-> File path to graph image auto-updates when edited via text box in `Graph settings` tab.\
-> Deleting file from project will no longer mess up legend.

Next milestones:\
-> Project autosaving (general),\
-> Grid options (Graph tab),\
-> Better legend editing (Legend tab),\
-> Project settings and files in form of zip files,\
-> Full documentation in form of a README file.

## v. 0.2.2 - data exploder and minor bugfixes
26.08.2022

This version brings a new data editing module to the table. Ever needed to chop one file with multiple sets of data exploded into multiple files? Just turn on the `data exploder` module and pull a Kerbal Space Program on the file!

Bug fixes:\
-> If labels are limited by ' " ' sign, the label separator sign will be ignored during preparation of returnable labels in projectexporter.readData() function.\
-> Default graphing engine is set to "modules/engine.py"

Known bugs:\
-> Deleting file from project will mess up legend.

Next milestones:\
-> Project autosaving (general),\
-> Grid options (Graph tab),\
-> Editing file name in text box to automatically update output file name (Graph tab),\
-> Better legend editing (Legend tab),\
-> Project settings and files in form of zip files,\
-> Full documentation in form of a README file.

----

## v. 0.2.1 - hotfix
25.08.2022

Even though this update is a hotfix, it also introduces an option for forcing absolute values while making log-scale graph. Just to make those graphs even tidier. The main functionality of this option is placed in `engine.py` graphing module. It does not change the loaded data.

Version 0.2.1 fixes some recent bugs:\
-> It appears not all `.xy` (fluent graph files) are separated with `'\t'` sign. Fixed.\
-> Projects were not properly saved in all tabs. Fixed.\
-> Fixed the `'=' sign destroys your legend` bug.\
-> Fixed the `no '\n' in graph titles` bug.\
-> Fixed potential problems with loading log scale options from project

Known bugs:\
-> Deleting file from project will mess up legend.

Next milestones:\
-> Project autosaving (general),\
-> Grid options (Graph tab),\
-> Editing file name in text box to automatically update output file name (Graph tab),\
-> Better legend editing (Legend tab),\
-> Project settings and files in form of zip files,\
-> Full documentation in form of a README file.

## v. 0.2.0 - bugfixes and log scale.
25.08.2022

Version 0.2.0 introduces new feature: log scale on x and y axis! The `.sgp` project file is now ammended with new option representing log scale.

Moreover there are several bug fixes:\
-> projects are now properly saved in all tabs,\
-> projects are loaded in all tabs and update all options automatically,\
-> if no row is selected in Legend tab, a message box will be shown instead of crashing the app.

Known bugs:\
-> Deleting file from project will mess up legend.

Next milestones:\
-> Project autosaving (general),\
-> Grid options (Graph tab),\
-> Editing file name in text box to automatically update output file name (Graph tab),\
-> Better legend editing (Legend tab),\
-> Project settings and files in form of zip files,\
-> Full documentation in form of a README file.

----

## v. 0.1.1 - Graphing engine and data normaliser.
18.08.2022

From now on, the graphing engine will be able to differentiate .csv and .xy files. Moreover, the project now has basic data rescaling capabielities.

----
## v0.1.0 - initial code upload

This commit has initial version of the public code. It provides user with basic launcher and graph generating engine.\
Project needs a full README file.