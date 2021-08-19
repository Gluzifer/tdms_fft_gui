import PySimpleGUI as sg
import os.path
from tdms_fft import tdms_fft
from nptdms import TdmsFile
import numpy as np
import re


# First the window layout in 2 columns

list_width = 53
file_list_column = [
    [
        sg.Text("TDMS file folder", key="-SOMETEXT-"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse('browse files'),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(list_width, 10), key="-FILE LIST-"
        )
    ],
    [
        sg.Button("Read File", key="-READ DATA-")
    ],
    [
        sg.Text("Groups"),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(list_width, 10), key="-GROUP LIST-"
        )
    ],
    [
        sg.Text("Channels"),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(list_width, 10), key="-CHANNEL LIST-"
        )
    ]
]

plot_controls_column = [
    [
        sg.Text("Sample rate in Hz:"),
        sg.Input(size=(10, 1), enable_events=True, key="-SAMPLERATE-")
    ],
    [
        sg.HorizontalSeparator()
    ],
    [
        sg.Text("Number of datapoints: "),
        sg.Text("Select file, group and channel first.", key="-N OF DATAPOINTS-")
    ],
    [
        sg.Text("Range of datapoints to process:"),
        sg.Input(size=(10, 1), default_text='0', enable_events=True, key="-DATA START-"),
        sg.Text("to"),
        sg.Input(size=(10, 1), enable_events=True, key="-DATA END-"),
    ],
    [
        sg.Text("(Defaults to all if either field is left empty)"),
    ],
    [
        sg.Text("Warning: Large datasets take some time to process!"),
    ],
    [
        sg.HorizontalSeparator()
    ],
    [
        sg.Checkbox("Truncate to power of two", default=False, key="-TRUNCATE-")
    ],
    [
        sg.Text("FFT runs most efficiently if the number of samples")
    ],
    [
        sg.Text("is a power of two. Maybe for large datasets.")
    ],
    [
        sg.Text("Warning: This TRUNCATES the data meaning part of it")
    ],
    [
        sg.Text("will be ignored!")
    ],
    [
        sg.HorizontalSeparator()
    ],
    [
        sg.Text("Plot type:"),
        sg.Radio('line', "RADIO1", default=True, key="-LINE PLOT RADIO-"),
        sg.Radio('step', "RADIO1", default=False, key="-STEP PLOT RADIO-"),
        sg.Radio('stem', "RADIO1", default=False, key="-STEM PLOT RADIO-")
    ],
    [
        sg.Text("Warning: \"stem\" uses ridiculous amounts of ram"),
    ],
    [
        sg.Text("if there are more than about 10^6 datapoints."),
    ],
    [
        sg.HorizontalSeparator()
    ],
    [
        sg.Text("Line thickness:"),
        sg.Input(size=(10, 1), default_text='1', enable_events=True, key="-LINE THICKNESS-"),
        sg.Text("(positive float)")
    ],
    [
        sg.Text("Line alpha (transparency):"),
        sg.Input(size=(10, 1), default_text='1', enable_events=True, key="-LINE ALPHA-"),
        sg.Text("(value between 0 and 1)")
    ],
    [
        sg.Text("There are ways to input something that does not match")
    ],
    [
        sg.Text("the intended pattern. Don't do it, the plot will not work.")
    ],

    [
        sg.HorizontalSeparator()
    ],

    [
        sg.Button("Calculate fft", key="-CALCULATE FFT-"),
    ]

]


# ----- Full layout -----

layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(plot_controls_column),
    ]
]


window = sg.Window("TDMS fft tool", layout)


# Run the Event Loop

filename = ''
channel_set = False
global tdms_file
global group
global channel

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    # Folder name was filled in, make a list of files in the folder

    if event == "-FOLDER-":
        folder = values["-FOLDER-"]

        try:
            # Get list of files in folder
            file_list = os.listdir(folder)

        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".tdms"))
        ]
        window["-FILE LIST-"].update(fnames)

    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )

        except:
            pass

    elif event == "-READ DATA-" and filename != '':  # The read data button was clicked
        try:
            tdms_file = TdmsFile(filename)
            tdms_groups = tdms_file.groups()
            tdms_group_names = []
            for i in range(len(tdms_groups)):
                tdms_group_names.append(tdms_groups[i].name)

            window["-GROUP LIST-"].update(tdms_group_names)
        except:
            pass

    elif event == "-GROUP LIST-":
        try:
            group = tdms_file[values["-GROUP LIST-"][0]]
            tdms_channels = group.channels()
            tdms_channel_names = []
            for i in range(len(tdms_channels)):
                tdms_channel_names.append(tdms_channels[i].name)

            window["-CHANNEL LIST-"].update(tdms_channel_names)

        except:
            pass

    elif event == "-CHANNEL LIST-":
        try:
            channel = group[values["-CHANNEL LIST-"][0]]
            channel_set = True
            window["-N OF DATAPOINTS-"].update(len(channel))
            try:
                assumed_samplerate = 1/channel.properties['wf_increment']
                window["-SAMPLERATE-"].update(assumed_samplerate)
            except:
                pass

        except:
            pass

    elif event == "-LINE THICKNESS-":
        # Make sure alpha and witdh values are valid
        try:
            cleaned_input = ''
            for i in re.findall("[0-9, .]+", values['-LINE THICKNESS-']):
                cleaned_input += i

            cleaned_input = re.sub(r"\.\.", '.', cleaned_input)
            window['-LINE THICKNESS-'].update(cleaned_input)

            if float(values['-LINE THICKNESS-']) < 0:
                window['-LINE THICKNESS-'].update(abs(float(values['-LINE THICKNESS-'])))
        except:
            pass

    elif event == "-LINE ALPHA-":
        # Make sure alpha and witdh values are valid
        try:
            cleaned_input = ''
            for i in re.findall("[0-9, .]+", values['-LINE ALPHA-']):
                cleaned_input += i

            cleaned_input = re.sub(r"\.\.", '.', cleaned_input)
            window['-LINE ALPHA-'].update(cleaned_input)

            # print(cleaned_input)

            if float(values['-LINE ALPHA-']) < 0:
                window['-LINE ALPHA-'].update(abs(float(values['-LINE ALPHA-'])))

            if float(values['-LINE ALPHA-']) > 1:
                window['-LINE ALPHA-'].update(1)
        except:
            pass

    elif event == "-CALCULATE FFT-" and channel_set and values["-SAMPLERATE-"] != '':
        # tdms_fft(tdms_file, group.name, channel.name, 
        sample_rate = float(values["-SAMPLERATE-"])
        if values["-DATA START-"] == '' or values["-DATA END-"] == '':
            data_start = 0
            if values["-TRUNCATE-"]:
                data_end = int(2**np.floor(np.log2((len(channel)))))
            else:
                data_end = len(channel)
        else:
            data_start = int(values["-DATA START-"])
            if values["-TRUNCATE-"]:
                data_end = int(values["-DATA END-"])
                data_end = int(2**np.floor(np.log2((data_end-data_start)))) + data_start
            else:
                data_end = int(values["-DATA END-"])

        # Plot style
        if values["-STEM PLOT RADIO-"]:
            plot_type = 'stem'
        elif values["-LINE PLOT RADIO-"]:
            plot_type = 'line'
        elif values["-STEP PLOT RADIO-"]:
            plot_type = 'step'

        tdms_fft(tdms_file, group.name, channel.name, sample_rate, data_start, data_end,
                 plot_type, plot_linewidth=float(values['-LINE THICKNESS-']), plot_linealpha=float(values['-LINE ALPHA-']))

window.close()
