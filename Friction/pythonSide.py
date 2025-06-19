import serial
import keyboard  # pip install keyboard
import time
import csv
import numpy as np
ser = serial.Serial('COM6', 921600, timeout=1)  # Adjust to your Arduino port

def get_reading(timeout=0.5):
    start = time.time()
    ser.write(b'r')
    while True:
        if time.time() - start > timeout:
            ser.write(b'r')
        response = ser.readline().decode('utf-8').strip()
        if response:
            #print(f"Arduino response: {response}")
            try:
                return float(response)
            except ValueError:
                pass
def run_trial():
    t=time.time()
    force_readings=[]
    for i in range(35): #push forward to reset 
        ser.write(b'w')
        #data=get_reading()
        time.sleep(0.5)
    print("Ready...")
    input(">")
    forces=[]
    time_stamps=[]
    print("Recording...")
    for i in range(35):
        ser.write(b's')
        time.sleep(0.5)
        data=get_reading()
        force_readings.append(data)
        time_stamps.append(time.time()-t)
    return force_readings,time_stamps
def process_data(force_readings):
    # Normal force (N)
    normal_force = mass * g

    # Calculations
    avg_friction = np.mean(force_readings)
    max_friction = max(force_readings)
    static_friction = force_readings[0]  # assuming first value is peak static force

    # Coefficients
    mu_avg = avg_friction / normal_force
    mu_max = max_friction / normal_force
    mu_static = static_friction / normal_force

    # Output
    print(f"Normal force: {normal_force:.2f} N")
    print(f"Average Friction Force: {avg_friction:.2f} N → μ_avg = {mu_avg:.4f}")
    print(f"Max Friction Force: {max_friction:.2f} N → μ_max = {mu_max:.4f}")
    print(f"Static Friction (first): {static_friction:.2f} N → μ_static = {mu_static:.4f}")

mass=10
g = 9.81
texture="EFoam"
file_to_write="C:/Users/dexte/Documents/GitHub/3D-textures/Friction/data/recordings_"+str(texture)+"_"+str(mass)+".csv"

#run the trials
data1,times1=run_trial()
data2,times2=run_trial()
data3,times3=run_trial()

#save the trials
with open(file_to_write, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Trial 1 Timestamp', 'Trial 1 Force','Trial 2 Timestamp', 'Trial 2 Force','Trial 3 Timestamp', 'Trial 3 Force'])  # 
    rows=zip(times1,data1,times2,data2,times3,data3)
    writer.writerows(rows)