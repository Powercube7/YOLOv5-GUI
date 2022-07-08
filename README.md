# YOLOv5 GUI
Ever get tired of remembering the syntax when running YOLOv5 jobs? Wish it could be easier? Then you may have stumbled on something you were looking for!
This project consists of a GUI made using PySimpleGUI with the aim of creating your YOLOv5 jobs.

## Features
The project consists of 3 files:
- free_memory.py: This file's purpose is freeing up memory occupied by NVidia fatbins (credits for this script goes to [cobryan05](https://github.com/cobryan05))
- gui.pyw: This file contains the main code of the GUI. The extension of this file hides some command lines without purpose (see the FAQ below)
- functions.py: This fule contains most of the functions, which are used by the rest of the files

## Installation
In order to use this program, you will need [PyTorch](https://pytorch.org/get-started/locally/) and [a clone of the YOLOv5 repository](https://github.com/ultralytics/yolov5) installed on your computer.
Due to the project using a very low number of libraries otherwise, I have added a function to install them automatically if missing.

## Usage
1. After creating your custom dataset, MAKE SURE that the dataset YAML file uses the global path (starting from the disk drive) instead of using a relative path
2. Start the script and pick your options (any errors will be shown when trying to create the job)

   To start the script without the command prompt use: ```pythonw gui.py```
   
   If you don't mind the command prompt, you can just start it normally by using ```python gui.py```

3. Create the job and enjoy

NOTE: After successfully creating the first job, the following will be added as user settings in a file called settings.json: your YOLOv5 path, the name of the training file and the location of the torch package.
If any of these change, just delete the json file to fix the program in case it breaks.

## Questions & Answers
Q: Why does the main GUI file end with the PYW extension?
A: The main use case for this extension is hiding an optional command prompt when starting the script. You can read more about it [here](https://stackoverflow.com/questions/34739315/pyw-files-in-python-program).

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
