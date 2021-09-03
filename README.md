# tdms fft tool with gui

Just a simple gui tool to take the fft of a tdms file as produced by NI LabView.
Does just that. Nothing more. Nothing sophisticated so it might crash at times if the user does something unintended.

# Usage
Use the "Browse" button to select the directory containing the .tdms file.
The file itself may not be displayed in the filebrowser.

If the correct directory is selected, the .tdms file will appear in the 
"File List" below the browse button. 
To load the file, select it from the list by clicking on it and click the 
"Load File" button.

After the file was loaded (depending on the size that may take some time)
the contained groups will be displayed in the "group list".
Once a group is selected, the contained data channels will be displayed
in the "channel list". 
Finally, after selecting a channel the app will attempt to calculate 
the sample rate automatically by reading the properties contained in the
.tdms file. Also the total number of contained datapoints will be 
displayed in the right column.

Set the desired options in the right column and click "Run FFT" to run
the fft and display the output. 
The output will be displayed in the default matplotlib plot viewer. 
From there the plot may be saved as a image file if desired.
For more information on how to use the matplotlib plot viewer see the 
[matplotlib documentation](https://matplotlib.org/3.2.2/users/navigation_toolbar.html).
