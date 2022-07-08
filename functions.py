import os
def importLibraries():
    try:
        import os
        import PySimpleGUI
        import pefile
    except:
        os.system("pip install -q PySimpleGUI pefile")
        return importLibraries()
    else: return PySimpleGUI, pefile

def find_torch_directory():
    output = None
    for root, dirs, files in os.walk("C:\\"):
        if "torch_cpu.dll" in files:
            output = os.path.join(root, "*.dll")
            output = output.replace("\\", "/")
    return output

def flushTemporaryFiles(yolo_path):
    for file in os.listdir(yolo_path):
        if file.endswith("temp.yaml"): 
            os.remove(os.path.join(yolo_path, file))

def removeExtraSpaces(inputs):
    if type(inputs) == list:
        new_inputs = []
        for i in range(len(inputs)):
            new_inputs.append(" ".join(str(inputs[i]).split()))
        return new_inputs

    elif type(inputs) == str:
        return " ".join(inputs.split())

def checkNumeric(inputs):
    if type(inputs) == list:
        errors = []
        for i in range(len(inputs)):
            if not removeExtraSpaces(str(inputs[i])).isnumeric(): errors.append(i)
        return errors
    elif type(inputs) == str:
        return True if removeExtraSpaces(inputs).isnumeric() else False

def checkValidRange(inputs, ranges, ignore=[]):
    isError = []
    for i in range(len(inputs)):
        if i in ignore: isError.append(None)
        elif int(inputs[i]) < ranges[i][0] or int(inputs[i]) > ranges[i][1]: isError.append(True)
        elif int(inputs[i]) > ranges[i][0] and int(inputs[i]) < ranges[i][1]: isError.append(False)

    return isError

def checkErrors(dictionary):
    errors = []
    if dictionary['yolo_path'] == '':
        errors.append("No path to the YOLO training file was specified")

    if not dictionary['yaml'].endswith('.yaml') and not dictionary['yaml'].endswith('.yaml"'):
        errors.append("No YAML file has been supplied")

    if not checkNumeric(dictionary['batch_size']) and dictionary[1] == True:
        errors.append("No valid batch size was provided")
    elif dictionary[1] == False and dictionary[0] == False:
        errors.append("No batch size was selected")

    if dictionary[2] == False and dictionary[3] == False:
        errors.append("No caching strategy was selected")

    if dictionary[4] == False and dictionary[5] == False and dictionary[6] == False and dictionary[7] == False:
        errors.append("No model type was selected")

    epochs, workers, image_size, patience = removeExtraSpaces([dictionary['epochs'], dictionary[8], dictionary[9], dictionary[10]])
    legend_dict = {
        0: 'Epochs',
        1: 'Workers',
        2: 'Image size',
        3: 'Patience'
    }
    ignore = checkNumeric([epochs, workers, image_size, patience])
    ranges = [(50, 2001), (0, 9), (320, 1281), (25, 251)]
    range_errors = checkValidRange([epochs, workers, image_size, patience], ranges, ignore)

    for err in ignore: errors.append(f"{legend_dict[err]} value is not numeric")
    for i in range(len(range_errors)):
        if range_errors[i] == True:
            errors.append(f"{legend_dict[i]} value is not in the valid range. Minimum value: {ranges[i][0]}, maximum value: {ranges[i][1] - 1}")

    return errors