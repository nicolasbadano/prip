**PRip** is a tool for digitizing scientific plots and graphs, getting numeric data. It works similarly to the popular g3data application, but has a greater enphasis on usability, precision and portability.

PRip is written in Python, and used the Qt toolkit through the PyQt bindings. This language and toolkit selection hopefully makes it very portable.

PRip is entirely **open-source**, and everyone is free to propose changes or maintain their own, customized version as long as they make their changes open to the public in accordance with the GNU General Public License (for more information check the license file attached to this project).

### Current Features
*   Import plots captured on typical image formats (jpg, png, etc).
*   Define reference points for x and y axis.
*   Digitize data using the free zoom view, which allow fast input and great precision.
*   Drag data points to improve the fit.
*   Export data as plain text.
*   Store the digitizing project for latter review or improvement.
*   Digitize multiple datasets per plot

### Planned Features
*   Manage the style of the datasets.
*   Export gnuplot input to automatically recreate original plot digitaly.
*   Additional reference points for more accurate results on distorted plots.

### Running from binaries
Packaged versions of PRip are available for both Windows and Linux, generated with [PyInstaller](http://www.pyinstaller.org/). Simply unpack the executable and `.ui` files to a folder and double-click. No dependencies should be required.

Check the [releases page](https://github.com/esteldunedain/prip/releases) on GitHub for the download links.

### Running from source
PRip can also be run from source. In that case ou need to install the python interpreter and the PyQt bindings.

It is currently tested on Python 2.7.2 and PyQt 4.8.6, but should run on other versions of Python 2.* and PyQt 4.* as well.

#### On Windows
- Download the source code
- Install the latest version of python 2 from https://www.python.org/downloads/
- Install the corresponding version of PyQt from http://www.riverbankcomputing.com/software/pyqt/download
- Double click on the `PRip.py` file

#### On Ubuntu/Mint/Debian
If you have a distribution based on KDE you most likely already have what's needed. In any case, this instructions should be enough:

- Download the source code
- `sudo apt-get update && sudo apt-get install python-qt4`
- On the source code folder, run `python PRip.py`

Or, if you want to automatically download and execute the latest code, installing dependencies if needed:

- `sudo apt-get update && sudo apt-get install git python-qt4 && git clone https://github.com/esteldunedain/prip.git && cd prip && python PRip.py`

### Contributing
If you want to help put with the ongoing development, you can do so by looking for possible bugs or by contributing new features. To become one of the developers, simply fork this repository and submit your pull requests for review.

To report a bug, propose a feature, or suggest a change to the existing one — please, use our [Issue Tracker](https://github.com/esteldunedain/prip/issues).

### Author
Written by Nicolás Diego Badano < nicolas.d.badano at gmail.com >

### Changelog

#### v0.3
- Added the possibility of digitizing multiple datasets per plot.
- Path to the source image is now stored as relative to the project file.
- Slightly reduced the size of markers

#### v0.2
- Code structure refactored to a MVC pattern.

#### v0.1
- First released version.