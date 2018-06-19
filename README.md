# monomial-staircase
Draw the staircase diagram of a given monomial ideal.

* Supports 3-dimensional monomial ideals of any size.  
* Optionally draws Buchberger graphs.  
* Several different "angles" (that is, 3D perspectives) are built in.  
* Feature requests are encouraged, just send me an email!

You can find action shots in the `samples` folder.  

Please note that this is an *alpha version* and subject to change without notice.  

## License
numsgps-sage is released under the terms of the [GNU General Public License Version 3](https://www.gnu.org/licenses/gpl-3.0.en.html).  

## Usage
To set up your machine to use monomial-staircase, do the following.  

* Download and unzip monomial-staircase.  It does not need to be placed in any particular location
* Download and unzip [PyX](https://pypi.org/project/PyX).  
* Move the `pyx` folder (the one with a whole bunch of `.py` files in it) into the same folder as `staircase.py`.

To use monomial-staircase, use your favorite Python interpreter, or open the command prompt and run the following commands (replace `PATH_TO_MONOMIAL_STAIRCASE` with the path of whichever folder contains `staircase.py`).  

	cd PATH_TO_MONOMIAL_STAIRCASE
	python staircase.py --help
	python staircase.py samples/millersturmfels.txt
	python staircase.py -b samples/millersturmfels.txt

Note: the newest version of PyX requires Python 3.  If you are running Python 2, or if you try to run staircase.py and encounter an error of the form

	PyX 0.14.1 requires Python 3.2 or higher

use [PyX 12.1](https://pypi.org/project/PyX/0.12.1) instead.  
