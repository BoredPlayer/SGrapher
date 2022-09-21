# Change log

## v. 0.2.9 - column selection!

`Legend Tab` now enables choosing from which column of the file should the data be drawn! It was a really needed change, as not all files were prepared in form of two columns. This required significant changes to `SGProjectExporter` class, `LegendEdit` class, exported project design and the `engine`, as well as creation of a new class - `fileclass`. From now on, this will be the target destination for file metadata. However, even with all those changes, no backwards compatibility was broken.

Moreover it is not necessary to state file types before loading the first file, as it is be generated automatically if the `file types` array is empty.

Bug fixes:\
-> Project should no longer require reloding to be visualised.\
-> After saving from tab other than `File tab`, user is no longer prompted to select new filename.

Known bugs:\
-> Coding of project may break cross-platform compatibility. It is recommended to convert all projects to ANSI.\
-> `Project->Toggle showing/saving graph` updates only when outside of "Graph tab"\

Next milestones:\
-> Project autosaving (general),\
-> Data editing options (new tab, project exporter),\
-> Live object positioning in graph - position of legend, additional texts and primitives (new tab, project exporter)\
-> Grid options - grid on/off, density, major and minor rules, vertical/horizontal rules (Graph tab),\
-> Project settings and files in form of zip or binary files,\
-> Full documentation in form of a README file.

## v. 0.2.8 - better data modding

This update provides a way to automatically insert new data types from GUI. If multiple data sets of the same names are inserted a counter will be initiated ammending repeating values with number of repetitions in brackets.

A new module (`spanaverage.py`) has been added to the package. It's main function is to detect repeating (more or less) values in a column and average all the column values accordingly. The resulting files will have the same name, except a "_spanaveraged" phrase will be added before '.' sign. Level of similarity can be specified with scalar `epsilon`, which is the falf-width of the acceptance zone. In other words, the value will be averaged if it's argument will be in range $$-\varepsilon < x < \varepsilon$$ The syntax of the new module is simmilar to `rescaledata.py` module, having `-p` flag as project containing required data, `-f` as data files, `-d` as data files' directory. It also accepts `-e` or `--epsilon` as $\varepsilon$ scalar.

`rescaledata.py` has been updated with a new functions for finding arguments based on fucntions, data x-axis rescaling to length of symmetrical NACA airfoils and backwords (from length of a symmetrical NACA airfoil to chord position). In order to activate this option it is necessary to pass flag:
```shell
$ python rescaledata.py -d "/path/to/files" -f "file_for_rescaling.xy" --scale-to-naca [airfoil thickness] [angle of attack] --normalise-x
```

Bug fixes:\
-> _No bugs were harmed during the production of this update._

Known bugs:\
-> Coding of project may break cross-platform compatibility. It is recommended to convert all projects to ANSI.\
-> When a new project is saved from tab other than `Files`, a "save project as" dialog opens after each consecutive save.\
-> `Project->Toggle showing/saving graph` sometimes does not change mode. Requires further analysis.\
-> Sometimes project requires reloading to be able to generate graph.

Next milestones:\
-> Project autosaving (general),\
-> Data editing options (new tab, project exporter),\
-> Live object positioning in graph - position of legend, additional texts and primitives (new tab, project exporter)\
-> Grid options - grid on/off, density, major and minor rules, vertical/horizontal rules (Graph tab),\
-> Project settings and files in form of zip or binary files,\
-> Full documentation in form of a README file.

---

## v. 0.2.7 - data rescaling, default types and bug fixes

`rescaledata.py` finally accepts individual files, instead of full project. Just type `-f` and paths to files (yes, even multiple, just separate them with ` ` (space) sign). If you provide `-d` or `--path` flag, you can specify the main path, and the files will be searched in the specified folder. This also applies to project files.\
The `SGProjectExporter` class from now on supports file types auto-generation. This is used to provide a smooth experience during loading individual files during rescaling.

Bug fixes:\
-> You can cancel loading new file from type choicebox without the app crashing. Yes, this was a bug and I'm ashamed for it.\
-> `rescaledata.py` does not change separation char of data anymore.

Known bugs:\
-> Coding of project may break cross-platform compatibility. It is recommended to convert all projects to ANSI.\
-> When a new project is saved from tab other than `Files`, a "save project as" dialog opens after each consecutive save.\
-> `Project->Toggle showing/saving graph` sometimes does not change mode. Requires further analysis.

Next milestones:\
-> Project autosaving (general),\
-> Data editing options (new tab, project exporter),\
-> Live object positioning in graph - position of legend, additional texts and primitives (new tab, project exporter)\
-> Grid options - grid on/off, density, major and minor rules, vertical/horizontal rules (Graph tab),\
-> Project settings and files in form of zip or binary files,\
-> Full documentation in form of a README file.

---

## v. 0.2.6 - some new data edition

This update provides some small upgrades to `rescaledata.py` module, ammending command line options with normalising and scaling data. To be honest it's a bit half-baked, but there was little time to make it a general update like `v.0.2.4`. Works only with exploded files (for now).

Bug fixes:\
-> _No bugs were harmed during the production of this update._

Known bugs:\
-> Coding of project may break cross-platform compatibility. It is recommended to convert all projects to ANSI.

Next milestones:\
-> Project autosaving (general),\
-> Data editing options (new tab, project exporter),\
-> Grid options (Graph tab),\
-> Project settings and files in form of zip or binary files,\
-> Full documentation in form of a README file.

---

## v. 0.2.5 - width and alpha bugfixes.

With the changes of the last update, some new bugs were introduced. Namely - there was no way to save a project, that was created before v. 0.2.4 and loaded. The reason was that alpha and width values were not set properely in project object during loading a project file without the aforementioned values being explicit. This bug required a brand new file loading system in project objects, bringing a dedicated method: `SGProjectExporter.addDataFile()`. This method automatically fills all the required arrays with default values if none besides filename and filetype are specified.\
Moreover, the project is now not cleared until a new project is selected.

Bugfixes:\
-> No more crashing during loading of an old (pre v. 0.2.4) project file.

Known bugs:\
-> Coding of project may break cross-platform compatibility. It is recommended to convert all projects to UTF-8.

Next milestones:\
-> Project autosaving (general),\
-> Grid options (Graph tab),\
-> Project settings and files in form of zip files,\
-> Full documentation in form of a README file.

---

## v. 0.2.4 - And the updates kept coming...
30.08.2022

This is a big one - finally the legend editing has some meaningful updates! Since this version, you can edit line width and opacity. However, you don't have to do it with those pesky buttons at the bottom of the window anymore! **Just doubleclick at the value you want to change and write whatever you need there to be**! No strings attached, at least that I know of. Keep an eye on the `Known bugs` section.

This means, that the `Better legend editing` milestone is finally achieved! :tada:

This version required some changes to `matgrapher` library, so please, update it with whatever method you find the most suitable or with pip command:
```python
pip install git+https://github.com/BoredPlayer/matgrapher.git
```

Bug fixes:\
-> _No bugs were harmed during the production of this update._

Known bugs:\
-> Coding of project may break cross-platform compatibility. It is recommended to convert all projects to ANSI.

Next milestones:\
-> Project autosaving (general),\
-> Grid options (Graph tab),\
-> Project settings and files in form of zip files,\
-> Full documentation in form of a README file.

---

## v. 0.2.3a - multiplatform hotfix
30.08.2022

This version is a result of a realisation, that `python` and `python3` are completly separate things in most of linux distros. It fixes graphing engine execution on linux. Moreover, the `=` sign will no longer break graph title while reloading project.

Bugfixes:
-> Graphing engine execution is now os-dependant\
-> Title no longer broken by `=` sign.

Known bugs:\
-> Coding of project may break cross-platform compatibility. It is recommended to convert all projects to ANSI.

Next milestones:\
-> Project autosaving (general),\
-> Grid options (Graph tab),\
-> Better legend editing (Legend tab),\
-> Project settings and files in form of zip files,\
-> Full documentation in form of a README file.

---

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

---

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