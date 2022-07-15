import functions
from shutil import copy as copyFile
import os
import time
sg = functions.importLibraries()[0]

sg.theme('DarkBlack')
sg.user_settings_filename(filename='settings.json', path='.')
end_dict = None
yolo_path = sg.user_settings_get_entry('yolo_path', '')
train_file = sg.user_settings_get_entry('train_file', '')
torch_location = sg.user_settings_get_entry('torch_location', None)


layout = [
        [sg.Push(), sg.Text("YOLO Model Trainer GUI", auto_size_text=True, font='arial 18 bold'), sg.Push()],
        [sg.Text("YOLO Training File", auto_size_text=True), sg.Push(), sg.Input(f"{yolo_path}/{train_file}" if yolo_path != '' else '', key='yolo_path', enable_events=True), sg.FileBrowse(key='yolo_browse')],
        [sg.Text("Dataset YAML file", auto_size_text=True), sg.Push(), sg.Input(key='yaml', enable_events=True), sg.FileBrowse()],
        [sg.Text("Job Customization", auto_size_text=True, font='arial 14 bold')],
        [sg.Text('_'  * 100, size=(65, 1))],
        [sg.Text("Batch Size", auto_size_text=True, font='arial 12 bold')],
        [sg.Radio('Automatic', 'batch', auto_size_text=True, enable_events=True)],
        [sg.Radio('Manual', 'batch', auto_size_text=True, enable_events=True), sg.Input(key='batch_size', disabled=True, enable_events=True)],
        [sg.Text('_'  * 100, size=(65, 1))],
        [sg.Text("Cache Strategy", auto_size_text=True, font='arial 12 bold')],
        [sg.Radio('RAM', 'cache', auto_size_text=True), sg.Radio('Disk', 'cache', auto_size_text=True)],
        [sg.Text('_'  * 100, size=(65, 1))],
        [sg.Text("Model Type", auto_size_text=True, font='arial 12 bold')],
        [sg.Radio('Nano', 'model', auto_size_text=True), sg.Radio('Small', 'model', auto_size_text=True), sg.Radio('Medium', 'model', auto_size_text=True), sg.Radio('Large', 'model', auto_size_text=True)],
        [sg.Text('_'  * 100, size=(65, 1))],
        [sg.Text("Other Arguments", auto_size_text=True, font='arial 12 bold')],
        [sg.Text('Epochs', size=(8, 1)), sg.Input('300', key='epochs', size=(4,1), enable_events=True), sg.Text('Workers', size=(7,1)), sg.Spin([i for i in range(9)], initial_value=1)],
        [sg.Text("Image Size", auto_size_text=True), sg.Input('640', size=(4,1)), sg.Text("Patience", auto_size_text=True), sg.Input('100', size=(3,1))],
        [sg.Text(auto_size_text=True, text_color='red', visible=False, key="job_errors")],
        [sg.Push(), sg.Button('Create Job', auto_size_button=True), sg.Exit()]
    ]

window = sg.Window('Model Training GUI', layout)
start_job = False

while True:
    event, values = window.read()
    if event == 'Exit' or event == sg.WIN_CLOSED:
        break

    # print(values)
    end_dict = values

    if values[1] == True:
        window['batch_size'].update(disabled=False)
    else:
        window['batch_size'].update('', disabled=True)

    if event == 'Create Job':
        errors = functions.checkErrors(end_dict)
        window['job_errors'].update("Looking for PyTorch installation...\nWARNING: If the application stops responding, please keep waiting", visible=True, text_color='white')
        window.refresh()
        time.sleep(0.25)

        if len(errors) > 0:
            window['job_errors'].update(f"The following {len(errors)} error(s) were encountered:\n- " + "\n- ".join(errors), visible=True, text_color='red')

        elif torch_location is None:
            torch_location = functions.find_torch_directory()
            sg.user_settings_set_entry('torch_location', torch_location)
        
            if torch_location is None:
                window['job_errors'].update("Error: PyTorch installation was not found.", visible=True, text_color='red')

            else:
                window['job_errors'].update("Cleaning memory to avoid leaks...", visible=True, text_color='white')
                window.refresh()
                os.system(f'cd {os.getcwd()} && python free_memory.py --input "{torch_location}"')
                window['job_errors'].update("Starting Job...")
                window.refresh()
                start_job = True
                break

window.close()

if start_job:
    yolo_path = end_dict['yolo_path'].replace('\\', '/')
    yolo_path = yolo_path.split('/')
    train_file = yolo_path.pop()
    yolo_path = "/".join(yolo_path)
    yaml_path = end_dict['yaml'].replace('\\', '/')
    yaml_path = yaml_path.split('/')
    yaml_name = yaml_path.pop()
    yaml_path = "/".join(yaml_path)
    sg.user_settings_set_entry('train_file', train_file)
    sg.user_settings_set_entry('yolo_path', yolo_path)
    functions.flushTemporaryFiles(yolo_path)

    batch_size = 0
    model_dict = {
        4: 'n',
        5: 's',
        6: 'm',
        7: 'l'
    }
    model = None
    for i in range(4, 8):
        if end_dict[i] == True: model = 'yolov5{}.pt'.format(model_dict[i])
    
    functions.createYaml(yolo_path, yaml_path, yaml_name)
    command = f'cd {yolo_path} && echo Checking for new commits... && git pull && echo Starting training... && python {train_file} --img {end_dict[9]} --batch {-1 if end_dict[0] == True else int(end_dict["batch_size"])} --epochs {int(end_dict["epochs"])} --cache {"disk" if end_dict[3] == True else "ram"} --data {yaml_name[:-5]}_temp.yaml --weights {model} --patience {int(end_dict[10])} --workers {int(end_dict[8])}'
    start = time.time()
    os.system(command)
    total_time = round(time.time() - start)
    sg.popup(f"Model training finished!\nTime Elapsed: {int(total_time / 3600)} hours, {int((total_time - int(total_time / 3600) * 3600) / 60)} minutes and {total_time%60} seconds", title="Training Ended")