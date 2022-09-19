# SGrapher
A simple launcher for matgrapher- and matplotlib-based graph generators. It provides a GUI for preparing projects of graphs, which can be turned into matplotlib graphs using built-in graph generator.

## Table of contents
1. [Installation](#1-installation)\
1.1. [Dependencies](#11-dependencies)\
1.2. [Git clone](#12-git-clone)\
1.3. [Manual download](#13-manual-download)
2. [Usage](#2-usage)\
2.1. [Modules](#21-modules)\
&emsp;2.1.1. [Data rescaler](#211-rescale-data)


## 1. Installation
To install the software, user can choose one of the two recommended paths:
1. Cloning with git
2. Manually downloading files

However, SGrapher is highly dependant on python and some python libraries. In order to correctly install full package, please follow instructions from [Dependencies](#11-dependencies) section.

### 1.1. Dependencies
In order to work correctly, SGrapher needs:
1. [Python 3](https://www.python.org/downloads/) interpreter
2. [numpy](https://numpy.org/install/) - highly advanced math library
3. [matplotlib](https://matplotlib.org/stable/users/getting_started/index.html#installation-quick-start) - a powerful plotting library
4. [matgrapher](https://github.com/BoredPlayer/matgrapher) - a simple matplotlib wraper for better code readability
5. [PyQt5](https://pypi.org/project/PyQt5/) - a library aiding GUI creation

Please install all of the above before downloading SGrapher.

### 1.2. Git clone

Due to the project being in early phase of development, it will receive updates fairly often. Therefore, cloning may be a better option, as it makes it much easier to download the newest version of the software.

In order to download SGrapher via git cloning, all that needs to be done is:
1. Ensure you have [git](https://www.git-scm.com/downloads) and all of the [Dependencies](#11-dependencies) installed on your computer
2. Open terminal (on Windows go to `Start->cmd.exe`)
3. Go to your desired folder (for example `cd Documents/git/`)
4. Execute command `git clone https://github.com/BoredPlayer/SGrapher.git`

After these steps SGrapher should be installed on your computer.

### 1.3. Manual download

If you do not wish to have all of the repository's history stored on your computer, you may choose downloading a zip file containing all of the files. In order to do it:
1. Ensure you have all of the [Dependencies](#11-dependencies) installed on your computer,
2. Head to the green `Code` button at the top of the site,
3. Click on `Download ZIP` button,
4. Extract all of the stored files into your desired path.

After these steps SGrapher should be installed on your computer.

## 2. Usage

### 2.1. Modules:

The software is provided with several modules ammending basic functionality of the launcher:
1. `rescaledata.py` - basic data manipulation such as rescaling both X and Y data axis
2. `explodedata.py` - multiple-column data divider

Currently, the functionality of the above modules is available only via TUI. In order to perform the data modification run the modules with python.

#### 2.1.1. Data rescaler

`rescaledata.py` provides resources for basic data manipulation. Data can be rescaled with a scalar or with function of length of symmetrical NACA airfoils. Available flags:

| flag | alternative flag | comment |
| :---:| :---: | ------- |
| `--path` | `-d` | set path to folder containing data files |
| `--project` | `-p` | read files from project |
| `--files` | `-f` | read files from list |
| `--normalise-x` | N/A | normalise all X-axis (column 0) arguments |
| `--normalise-y` | N/A | normalise all Y-axis (column 1) values |
| `--scale-x [float]` | N/A | scale all X-axis (column 0) arguments with a _scalar_ |
| `--scale-y [float]` | N/A | scale all Y-axis (column 1) values with a _scalar_ |
| `--scale-to-naca [float] [float]`| N/A | scale all X-axis (column 0) arguments to length of symmetrical NACA airfoil with its _thickness_ and _angle of attack_ (assumption: all data points are from the airfoil's surface) |
| `--scale-from-naca [float] [float] [float]`| N/A | scale all X-axis (column 0) arguments from symmetrical NACA airfoil length to chord position with its _thickness_, _chord_, and _angle of attack_ |

TODO: Complete the user guide.
```
I know, I know. I will take care of that as soon as possible.
~ BoredPlayer
```