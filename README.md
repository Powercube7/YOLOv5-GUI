# YoloV5 GUI

Ever get tired of remembering the syntax when running YOLOv5 jobs? Wish it could be easier? Then you may have stumbled on something you were looking for! This project consists of a GUI made using PySimpleGUI with the aim of creating your YOLOv5 jobs.

## Features
The project consists of 3 files:

 1. free_memory.py: This file's purpose is freeing up memory occupied by Nvidia fatbins (Credits: [cobryan05](https://github.com/cobryan05))
 2. GUI.pyw: The GUI code is contained within this file. The extension of the file hides command lines that serve no purpose (see Questions & Answers).
 3. Functions.py: This file contains most of the functions that can be used by the other scripts in this package.

## Prerequisites
This program requires [a clone of the YOLOv5 repository](https://github.com/ultralytics/yolov5)  to be installed on the computer in order to function properly.

## Installation
In order to run this program, you will need to install its dependencies by running the following command:
      
      pip install -r requirements.txt

## Usage

 1. Firstly, start the script and then pick your options (if any errors occur when creating the job, they will be displayed as a message).
	- The following code will allow you to initiate the script without getting a command prompt: ```pythonw gui.pyw```
	- However, if you do not mind the command prompt, you can simply execute it by typing: ```python gui.pyw```
 2. Enjoy your newly-created job!

## Questions & Answers

Q: Why does the main GUI file end with the .PYW extension?

A: The main use case for this extension is hiding an optional command prompt when starting the script. You can read more about it [here](https://stackoverflow.com/questions/34739315/pyw-files-in-python-program).

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.