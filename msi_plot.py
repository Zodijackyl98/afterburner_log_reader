import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

df_get_col_name = pd.read_csv(r"location/to/your/hml/file/HardwareMonitoring.hml", sep = ',', 
                                                   encoding_errors= 'ignore', 
                                                   skiprows = lambda x: x in np.append([0, 1],np.arange(3,100)))

new_col_names = [i.strip() for i in df_get_col_name.columns]
new_col_names[1] = 'Time' #Second column name is the value of the time when logging starts, changing it to "Time"

df = pd.read_csv(r"location/to/your/hml/file/HardwareMonitoring.hml", sep = ',',
                                                   encoding_errors = 'ignore',
                                                   skiprows = lambda x:x in np.arange(2))

df = df[df.iloc[:,0] == 80]

try:
    for i in df.columns[2:]: df.loc[:, i] = df.loc[:, i].astype('float')
except ValueError:
    pass

df.columns = new_col_names
aft_format_data = "%d/%m/%Y %H:%M:%S"
df['format_time_aft'] = df.iloc[:,1].apply(lambda x: ' '.join(str(x.strip()).split(' ')).replace('-','/'))
df['format_time_aft'] = df['format_time_aft'].apply(lambda x: datetime.strptime(x, aft_format_data))
df['Framerate'] = df['Framerate'].apply(lambda x: float('NaN') if (str(x).strip() == 'N/A') else float(x))#replace N/A with NaN
df['Framerate'].fillna(60.0, axis = 0, inplace = True)# shows 60 fps on idle
df.drop(labels = df.columns[0], axis = 1, inplace = True)# Remove meaningless first column


df.to_csv("./afterburner.csv", sep = '\t',header = True, index = False)

core_gen = [i for i in [i.split(' ')[0].split('CPU')[1] for i in df.columns if i.startswith("CPU") ] if i.isnumeric()]
cpu_core_num = max([int(i) for i in core_gen])

for i in range(1,cpu_core_num + 1):
    df[str('CPU') + str(i) + ' ' + 'clock'] = df.loc[:,str('CPU') + str(i) + ' ' + 'clock'].apply(lambda x: int(x))

while True:
    
    print("{a:<10} --> 1\n{b:<10} --> 2\n{c:<10} --> 3\n{d:<10} --> 4".format(a = 'CPU',
                                                      b = 'GPU',
                                                      c = 'GPU-win',
                                                      d = 'RAM'), sep = '', end = '\n')
    que_1 = input('Options("q" to quit) = ')

    try: 

        if que_1 == '1':
            
            cpu_temp_names = ['CPU'+str(i)+' temperature' for i in range(1,cpu_core_num + 1)]

            fig, ax = plt.subplots()
            fig.suptitle('CPU Core Temperatures', y = 0.93)

            for i in cpu_temp_names: ax.plot(df['format_time_aft'], df[i], linestyle = '--', linewidth = 0.5)

            ax.legend([i[:9] for i in cpu_temp_names],bbox_to_anchor=(1, 0.5), loc="center left",mode="expand", borderaxespad=0, ncol=1)

            ax.set_ylabel('CPU Core Temperatures(C)')
            plt.xticks(rotation = 45)

            ax.scatter(df['format_time_aft'], df['CPU temperature'], s = 15)
            ax.plot(df['format_time_aft'], df['CPU temperature'], linewidth = 1.5)
            ax.grid()                

            core_temp_names = ['Core' + ' ' + str(i) + ' ' +'Temperature' for i in range(0, cpu_core_num)]

            fig, ax = plt.subplots()
            fig.suptitle('CPU Core Usages', y = 0.93)
            cpu_usage_names = ['CPU'+str(i)+' usage' for i in range(1,cpu_core_num+1)]

            for i in cpu_usage_names: ax.plot(df['format_time_aft'], df[i], linestyle = '--', linewidth = 0.5)#CPU usage core by core


            ax.scatter(df['format_time_aft'], df['CPU usage'], s = 20, marker = 'x', c = 'r')  #CPU usage overall   
            ax.legend([i[:10] for i in cpu_usage_names],bbox_to_anchor=(1, 0.85), loc="upper center",
                                    mode="expand", borderaxespad=0, ncol=1)
            plt.xlabel('Time')
            ax.set_ylabel('CPU Usage(%)')
            ax.set_yticks(np.arange(0,+110,10), minow = True)
            plt.xticks(rotation = 45)
            ax.grid(axis = 'both')
      

            fig, ax = plt.subplots()
            fig.suptitle('CPU Power - Time', y = 0.93)
            plt.plot(df['format_time_aft'], df['Power'], linewidth = 0.6)
            plt.yticks(np.arange(0,300,25))
            plt.xticks(rotation = 45)
            plt.xlabel('Time')
            plt.ylabel('Power(Watt)')
            plt.grid(axis = 'both')
            plt.show()

            fig, ax = plt.subplots()
            fig.suptitle('CPU Power Percentage - Time', y = 0.93)
            plt.plot(df['format_time_aft'], df['CPU power'], linewidth = 0.6)
            plt.yticks(np.arange(0,130,10))
            plt.xticks(rotation = 45)
            plt.xlabel('Time')
            plt.ylabel('CPU Power(%)')
            plt.grid(axis = 'both')
            plt.show()

            cpu_freq_names = ['CPU'+str(i)+' clock' for i in range(1,cpu_core_num + 1)]

            for i in cpu_freq_names: plt.plot(df['format_time_aft'], df[i], linestyle = '--', linewidth = 1)
            
            plt.scatter(df['format_time_aft'], df['CPU clock'], marker = 'x', c = 'r', s = 15)
            
            plt.legend([i[:10] for i in cpu_freq_names + ['CPU clock']],bbox_to_anchor=(1, 0.85), loc="upper center",
                            mode="expand", borderaxespad=0, ncol=1)
            
            plt.title('CPU Core Frequencies(Mhz) - Time')
            plt.yticks(np.arange(0, 6000, 500))
            plt.xticks(rotation = 45)
            plt.xlabel('Time')
            plt.ylabel('CPU Core Frequency(Mhz)')
            plt.grid()
            plt.show()

        # '---------------------------------------------------------------------------------------------------------------------------------------------------------------'    

        if que_1 == '2':

            fig, ax = plt.subplots(5, sharex = True)
            ax[0].plot(df['format_time_aft'], df['GPU temperature'], label = 'GPU temperature', linewidth = 0.5, c = 'r') 
            ax[0].set_yticks(np.arange(35,90,10))

            ax[1].plot(df['format_time_aft'], df['GPU usage'], label = 'GPU Usage', linewidth = 0.5, c = 'r') 
            ax[1].set_yticks(np.arange(0,120,20))

            ax[2].plot(df['format_time_aft'], df['Power percent'], label = 'Power Percent(%)', linewidth = 0.5, c = 'y')
            ax[2].set_yticks(np.arange(0,110,20))

            ax[3].plot(df['format_time_aft'], df['Power'], label = 'Power(W)', linewidth = 0.5, c = 'k')
            ax[3].set_yticks(np.arange(0,300,50))

            ax[4].plot(df['format_time_aft'], df['Fan speed'], label = 'Fan speed', linewidth = 0.5)
            ax[4].set_yticks(np.arange(0,110,20))
            plt.xticks(rotation = 45)

            try:
                ax[4].plot(df['format_time_aft'], df['Fan speed 2'], linewidth = 0.5 , label = 'Fan speed 2')
            except KeyError:
                pass
            
            ax[4].set_yticks(np.arange(0,100,10))
            
            [ax[i].legend(loc = 'upper left') for i in range(5)]
            [ax[i].grid(axis = 'y', ls = '--') for i in range(5)]
            [ax[i].grid(axis = 'x', ls = '-') for i in range(5)]
            plt.show()

            plt.plot(df['format_time_aft'], df['Framerate'], linewidth = 0.75)
            plt.title('FPS - Time')
            plt.xlabel('Time')
            plt.ylabel('FPS')
            plt.xticks(rotation = 45)
            plt.grid()
            plt.show()

            plt.plot(df['format_time_aft'], df['Memory usage'].astype('float'))
            plt.title('GPU Memory Usage - Time')
            plt.xlabel('Time')
            plt.ylabel('RAM(Mb)')
            plt.yticks(np.arange(0, 13000, 1000))
            plt.xticks(rotation = 45)
            plt.grid()
            plt.show()

            plt.plot(df['format_time_aft'], df['Core clock'].astype('float'), linewidth = 0.55)
            plt.title('GPU Core Clock - Time')
            plt.xlabel('Time')
            plt.ylabel('Core Clock(Mhz)')
            plt.grid(axis = 'y', ls = '--')
            plt.xticks(rotation = 45)
            plt.show()

            print(df[['GPU usage', 'GPU temperature','Power percent','Power','Fan speed','Framerate']].astype('float').aggregate(['mean','min','max',np.median, 'std', 'sem']))

        if que_1 == '3':

            print("Selectable Time Interval = ", min(df['format_time_aft']), '-' ,max(df['format_time_aft']))
            str_time = input('Time to Start(YYYY/MM/DD hh:mm:ss) = ')
            end_time = input('Time to Stop(YYYY/MM/DD hh:mm:ss) = ')
            aft_format_data = "%Y/%m/%d %H:%M:%S"
            start = datetime.strptime(str_time, aft_format_data)
            end = datetime.strptime(end_time, aft_format_data)

            fig, ax = plt.subplots(1)
            plt.plot(df['format_time_aft'][(df['format_time_aft'] >= start) & (df['format_time_aft'] <= end)],
            df['Framerate'][(df['format_time_aft'] >= start) & (df['format_time_aft'] <= end)])
            plt.grid()
            fig.autofmt_xdate()
            plt.show()

            aft_win_len = len(df[['format_time_aft', 'CPU1 temperature']][(df['format_time_aft'] >= start) & (df['format_time_aft'] <= end)])
            
            plt.plot(df['format_time_aft'][(df['format_time_aft'] >= start) & (df['format_time_aft'] <= end)],
            df['CPU1 temperature'][(df['format_time_aft'] >= start) & (df['format_time_aft'] <= end)])

            plt.scatter(df['format_time_aft'][(df['format_time_aft'] >= start) & (df['format_time_aft'] <= end)],
            df['CPU temperature'][(df['format_time_aft'] >= start) & (df['format_time_aft'] <= end)])
            plt.show()


            print(df[['GPU usage', 'GPU temperature','Power percent','Power','Fan speed','Framerate']][(df['format_time_aft'] >= start) & (df['format_time_aft'] <= end)].aggregate(['mean','min','max',np.median, 'std', 'sem']), sep = '\n'*2)

        if que_1 == '4':

            plt.plot(df['format_time_aft'], df['RAM usage'], linewidth = 0.6)
            plt.yticks(np.arange(5000,36000,4000))
            plt.xlabel('Time')
            plt.xticks(rotation = 45)
            plt.ylabel('RAM Usage(MB)')
            plt.grid(axis = 'both')
            plt.show()

        if que_1 == 'q':
            break
    
    except KeyError as e:
        print('Possible Missing Column = ', e)
