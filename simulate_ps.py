# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 12:03:59 2022
Features:
    Data visualization
    SQL Database
    File I/O
    Real-time Database
    Cloud Storage
@author: bjord
"""
import time
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import random
import sqlite3

# parse PS identification
host_IP = "127.0.0.1:8005"
idn = "LAMBDA,GEN30-56-LAN,S/N:10M5470C,2U5K:5.1.1-LAN:2.1,00:19:F9:27:D3:B1"
ps_id = idn.split(",")
brand = ps_id[0]       # ['LAMBDA']
model = ps_id[1]       # ['GEN30-56-LAN']
serial = ps_id[2]      # ['S/N:10M5470B']
sn = serial.split(":") # ['S/N', '10M5470B']
firmware = ps_id[3]    # ['2U5K:5.1.1-LAN:2.1']
mac = ps_id[4]         # ['00:19:F9:27:D3:B0']

##################
# Database Setup #
##################

# create database file if it does not exist and open it in append mode
open('hbts_quads.db','a+')
conn = sqlite3.connect('hbts_quads.db')
print("Opened database successfully")

# create table
conn.execute('''CREATE TABLE IF NOT EXISTS TDK_LAMBDA
              (ID INTEGER PRIMARY KEY,
              BRAND      VARCHAR(255),
              MODEL      VARCHAR(255),
              SERIAL     VARCHAR(255),
              FIRMWARE   VARCHAR(255),
              MAC     VARCHAR(255));''')
print("Table successfully created")

# insert records in the table
# issue using {sn[1]} to INSERT serial number into table
conn.execute(f"INSERT INTO TDK_LAMBDA(BRAND,MODEL,SERIAL,FIRMWARE,MAC) \
              VALUES('{brand}','{model}','{sn[1]}','{firmware}','{mac}')")
conn.commit()
print("Records successfully created\n")

# fetch and display records from table
with conn:
    cursor = conn.execute("SELECT ID,BRAND,MODEL,SERIAL,FIRMWARE,MAC from TDK_LAMBDA")
    for row in cursor:
        print("ID = "      , row[0])
        print("BRAND = "   , row[1])
        print("MODEL = "   , row[2])
        print("SERIAL = "  , row[3])
        print("FIRMWARE = ", row[4])
        print("MAC = "     , row[5])
print("Operation done successfully\n")
conn.close()

# parse date/time
now = datetime.now().strftime('%y-%m-%d-%H-%M-%S')
d = now.split("-")
yr = d[0]
mnth = d[1]
dy = d[2]
hr = d[3]
mm = d[4]
sec = d[5]

volt = float(input("Enter PS voltage rating: "))
curr = float(input("Enter PS current rating: "))
curr_out = float(input("Enter desired output current: "))

# calulate bit size and scale
start = time.perf_counter()
v_bit = volt/2**16
c_bit = curr/2**16
scale = curr/volt
print("1-bits of voltage is: {} V\n1-bit of current is: {} A\nScale: 1V = {} Amps."
      .format(v_bit, c_bit, scale))

# pause for dramatic effect
time.sleep(1)

# create file and append if file doesn't already exist
file_path = f'C:\\Users\bjord\PythonScripts\tdk_lambda\{brand}\{model}\{sn[1]}\{now}'
if not os.path.exists(file_path):
    os.makedirs(f'{brand}\{model}\{sn[1]}\{now}')

# open and append content to file
f = open(f'{brand}\{model}\{sn[1]}\{now}\{now}.csv', "a")
f.write(f"Brand: {brand}\n")   
f.write(f"Model: {model}\n")
f.write(f"Serial: {sn[1]}\n")
f.write(f"Firmware Vers: {firmware}\n")
f.write("Date,Time,Output Voltage,Output Current,DCCT, {Host_IP}\n")

# create lists
Load = []
Output_Voltage = []
Set_Current = []
Read_Current = []
Date = []
Time = []
Host_IP = []

# iterate i over 1/16-bit increments
for i in np.arange(0, curr_out, c_bit):
        Host_IP.append(host_IP)
        current_date = datetime.now().strftime('%y-%m-%d')
        Date.append(current_date)
        volt_out = i / scale
        dcct = float(i + random.uniform(-0.015, 0.015)) # artificial current instabiliy
        Output_Voltage.append(volt_out)        
        Set_Current.append(i)        
        Read_Current.append(dcct)
        load_resistance = volt_out/i
        Load.append(load_resistance)
        current_time = datetime.now().strftime('%H:%M:%S:%f')
        Time.append(current_time)
        # dramatically display loop results
        time.sleep(0.0002)
        # create and display dataframe
        data = [
                {'Date':Date,
                  'Time':Time,
                  'Volts_Out (V)':Output_Voltage,
                  'Current_Out (A)':Set_Current,
                  'Current_Read (A)':Read_Current, 
                  'Host_IP':Host_IP}
        ]
        # df = pd.DataFrame(data)
        print(f'{current_date},{current_time},{volt_out:.3f},{i:.3f},{dcct:.3},{host_IP}')
        # append contents to .csv file
        f.write(f'{current_date},{current_time},{volt_out:.3f},{i:.3f},{dcct:.3f},{host_IP}\n')
for i in np.arange(curr_out, 0, -c_bit):
        Host_IP.append(host_IP)
        current_date = datetime.now().strftime('%y-%m-%d')
        Date.append(current_date)
        volt_out = i / scale
        dcct = float(i + random.uniform(-0.015, 0.015)) # artificial current instabiliy
        Output_Voltage.append(volt_out)        
        Set_Current.append(i)        
        Read_Current.append(dcct)
        load_resistance = volt_out/i
        Load.append(load_resistance)
        current_time = datetime.now().strftime('%H:%M:%S:%f')
        Time.append(current_time)
        # dramatically display loop results
        time.sleep(0.0002)
        # append contents to .csv file
        f.write(f'{current_date},{current_time},{volt_out:.3f},{i:.3f},{dcct:.3f},{host_IP}\n')
        # create and display dataframe
        data = [
            {'Date':Date,
             'Time':Time,
             'Volts_Out (V)':Output_Voltage,
             'Current_Out (A)':Set_Current,
             'Current_Read (A)':Read_Current, 
             'Host_IP':Host_IP}
        ]
        df = pd.DataFrame(data)
        print(f'{current_date},{current_time},{volt_out:.3f},{i:.3f},{dcct:.3},{host_IP}')
f.close()

# printing dataframe
print(df)
time.sleep(5)

# Generate plot
print("\nGenerating lineplots...")
time.sleep(0.25)
print("Displaying plots...\n")

##################
# generate plots #
##################

# Output Voltage
fig, ax1 = plt.subplots()
ax1.plot(Set_Current,Output_Voltage,'b--')
ax1.set(xlabel='Volts (V)', ylabel='Current (A)', 
        title=f"Output Voltage\nGenerated: {current_date} {current_time[:8]}")
ax1.grid()
fig.savefig("Output_Voltage.png")
f.close()
plt.show()

# Current Setpoint
f = open(f'{brand}\{model}\{sn[1]}\{now}\Current Setpoint.png',"w")
fig, ax2 = plt.subplots()
ax2.plot(Output_Voltage, Set_Current,'y--')
ax2.set(xlabel='Volts (V)', ylabel='Current (A)', 
        title=f"Current Setpoint\nGenerated: {current_date} {current_time[:8]}")
ax2.grid()
fig.savefig("Current_Setpoint.png")
plt.show()
f.close()

# Current Readback
f = open(f'{brand}\{model}\{sn[1]}\{now}\Current Readback.png',"w")
fig, ax3 = plt.subplots()
ax3.plot(Output_Voltage, Read_Current,'g')
ax3.set(xlabel='Volts (V)', ylabel='Current (A)',  
        title=f"Current Readback\nGenerated: {current_date} {current_time[:8]}")
ax3.grid()
fig.savefig("Current_Readback.png")
plt.show()
f.close()

# Load Resistance
f = open(f'{brand}\{model}\{sn[1]}\{now}\Load_Resistance.png',"w")
fig, ax4 = plt.subplots()
ax4.plot(Read_Current, Load,'m')
ax4.set(xlabel='Current (A)', ylabel='Ohms (\u03A9)', 
        title=f"Load Resistance\nGenerated: {current_date} {current_time[:8]}")
ax4.grid()
fig.savefig("Load_Resistance.png")
plt.show()
f.close()

# vertically stacked plots
f = open(f'{brand}\{model}\{sn[1]}\{now}\Output Summary.png',"w")
fig, axs = plt.subplots(2,2, tight_layout=True)
axs[0,0].plot(Set_Current,Output_Voltage)
axs[0,0].set_title('Output_Voltage')
axs[0,0].set(ylabel='Volts (V)')
axs[0,0].set(xlabel='Current (A)')
axs[0,0].grid(color = 'gray', linestyle = '--', linewidth = 0.5)

axs[0,1].plot(Set_Current,Output_Voltage,'tab:green')
axs[0,1].set_title('Current_SetPoint')
axs[0,1].grid(color = 'gray', linestyle = '--', linewidth = 0.5)

axs[1, 0].sharex(axs[0, 0])
axs[1,0].plot(Output_Voltage,Read_Current,'tab:olive')
axs[1,0].set_title('Current_Readback')
axs[1,0].set(xlabel='Volts (V)')
axs[1,0].set(ylabel='Current (A)')
axs[1,0].grid(color = 'gray', linestyle = '--', linewidth = 0.5)

axs[1, 1].sharex(axs[0, 1])
axs[1,1].plot(Set_Current,Load,'tab:red')
axs[1,1].set_title('Load_Resistance')
axs[1,1].set(xlabel='Current (A)')
axs[1,1].set(ylabel='Ohms (\u03A9)')
axs[1,1].grid(color = 'gray', linestyle = '--', linewidth = 0.5)
fig.savefig("Output_Summary.png")
f.close()

print("The .png files are being saved in two locations.\n")
print("The files are b")



def main():
    pass

if __name__ == '__main__':
    main()