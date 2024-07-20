# afterburner_log_reader
To read MSI Afterburner .hml log files, create useful plots to check the status of your PC components system wide.

MSI Afterburner is a really useful tools when it comes to check the status of your PC components in real time. It's widely used to learn you CPU, GPU usages while play games on your machine. It can also be used to monitor your PC idle It does not matter whether you run some specific apps or not. Usually people only use it's real time monitoring option to check the GPU temperature, CPU Usage, RAM/VRAM Usage, Power Consumption etc. but It also supports logging option which creates log file with "hml" extension. As I stated above, main functionality of this program I wrote is to read .hml files correct and to give users freedom to make analysis not only in real time but also after logging finishes. Righ after execution of the program, It also creates a csv file based on the hml file you specified in the program. Since most of the people are not even aaware of logging functionality of MSI Afterburner, I'll show you how to start and stop logging process. 

I run MSI Afterburner v4.6.5 at the moment but I have also log files created in 2022 and because there hasn't been any changes since then, you can also work with old hml files. Python requirements are simple; Numpy, Pandas and Matplotlib libraries are required. Tested with various versions of the libraries and Python versions and haven't seen any problem yet but I need to mention that I use Python 3.10.4 currently without any issue and I believe there won't be any for newer versions also. 

MSI Afterburner offers different interface options for its users but they are just graphical changes, everything is the same for all User Interfaces. First thing to do is to open settings/MSI Afterburner Properties and go to the Monitoring tab.

![MSI_AFT_monitoring_1](https://github.com/user-attachments/assets/a27176d5-f699-4213-b36e-c746dee6f113)

You will see "Hardware Polling period" or let's say your sampling rate in miliseconds. Adjust it as you wish 1 second is optimum to catch any major events in general.
Below that, in Graph options to test all of the graphs I put into the program just select every option it offers by holding down shift while selecting options from the top to the bottom and after selection, click any of the tick mark icons located on left side of every parameter. If you also want to see them on your screen in real time, you must tick "Show in On-Screen Display" box. Scroll down and you'll see "hardware monitoring history logging properties", under that option you can if you tick "log history to file" and then click apply button, It'll start logging process until you untick and click apply again to end the logging process. It saves every hml file under the main directory of MSI AFterburner with .hml extension and it names it "HardwareMonitoring.hml" in default. Below you'll see "global monitoring hotkeys", you can attach a key or some combination of keys to start/stop logging processs easily just be carefull the combination you choose does not ıntersect any key combo in the game. Also, depending on the user interface options, some supports graphical interfaces and you can right click to graph windows to start and stop logging process. It does not matter which option you decided to choose, just make sure you have .hml file in you computer. 

In the msi_plot.py, there are two read process, one to get parameters which then will be our columns in our main DataFrame, and the other to read values. Just specify the same directory where you put your hml file in for both processes and that's it. Then, you need to select which of your compenent you want to learn information from, CPU, GPU, GPU-win(shows values only in user specified time interval) and RAM. It'll create various kind of graphs regarding with the hml file you put into and also create a csv file inside the same directory you run the program. Below you'll find the result of a log file I recorded while I was watching a video on youtube and while playing a video game. Framerate value shows N/A default when you don't run any program but I adjusted it to show 60 at all times.

Program runs without an issue if you record the log on a Desktop PC with 1 external GPU like most of the cases. With more GPU's or CPU's, building a dataframe and creating csv file is not an issue but column names would be different than usual names especially for laptops since they come with both internal graphics in CPU and an external GPU graphics. One must pay attention if MSI Afterburner runs on a laptop. There won't be GPU Usage but instead GPU1 and GPU2 Usage or GPU1 Memory Usage, GPU1 Core Clock, GPU1 Temperature and so on. 

![MSI_AFT_monitoring_core_usages](https://github.com/user-attachments/assets/a6922e72-2b85-46fa-b267-607273556d5a)

![MSI_AFT_monitoring_core_usages_game](https://github.com/user-attachments/assets/a7ab707d-055b-476e-8d8e-ea1f82988db4)
CPU Core Usages are drawn individually with different colours in one graph and 'X' marks the spot overall CPU usage.


![MSI_AFT_monitoring_cpu_power_percentage](https://github.com/user-attachments/assets/2e9255a3-3723-4c64-9ac1-f4894f29a69b)

![MSI_AFT_monitoring_core_frequencies](https://github.com/user-attachments/assets/35ad3604-6660-4636-94c7-e05d0e7f3885)
![MSI_AFT_monitoring_core_frequencies_zoom](https://github.com/user-attachments/assets/a42a6b86-452f-407d-aee0-197274451e13)

CPU Core Frequencies are drawn individually with different colours in one graph and 'X' marks the spot overall CPU frequency. Second one is zoomed in.

![MSI_AFT_monitoring_core_temps](https://github.com/user-attachments/assets/8cea4c59-b8af-485f-96f4-cda64279fda6)
![MSI_AFT_monitoring_core_temps_game](https://github.com/user-attachments/assets/66278939-5cc6-4c07-93d1-a9f1e814071c)

CPU Core Temps are drawn individually with different colours in one graph and thick line shows overall CPU Temp.

For GPU graphs, I only used a video game as my source,

![MSI_AFT_monitoring_gpu_mix](https://github.com/user-attachments/assets/706fa70c-a1aa-469c-9766-4998d35cbe6d)

![MSI_AFT_monitoring_gpu_fps](https://github.com/user-attachments/assets/9c7b5019-98f6-4a54-9262-af6d1590fc84)

![MSI_AFT_monitoring_gpu_core_clock](https://github.com/user-attachments/assets/8d7652a6-ebbb-41b6-8d03-23626c287672)

![MSI_AFT_monitoring_gpu_ram](https://github.com/user-attachments/assets/ce4493a8-859a-403f-9cfe-ffaea3f7547b)

