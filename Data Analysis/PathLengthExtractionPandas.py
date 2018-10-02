import os
import datetime
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog
import math
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import FunctionsPandas as fn
import pandas as pd



if __name__ == "__main__":
    # file open dialog to select the file to work on
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    # create a file in the same directory to log the output of this code
    output_path = os.path.dirname(os.path.abspath(file_path))
    output_path = output_path+"\\Output.txt"
    datestring = "\n\n\nFile created: {} \n".format(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))

    text_file = open(output_path, "a")
    text_file.write(datestring)
    text_file.close()

    getdatastring = "Getting data from: {} \n".format(file_path)

    text_file = open(output_path, "a")
    text_file.write(getdatastring)
    text_file.close()

    # by default expect a csv
    delim = ","

    # if a tsv is found, switch delimiter to a tab character
    if file_path[-4:] == ".tsv":
        delim = "\t"
        # warn the user that this is a tab sep file
        print("\n.tsv file detected, switching delimiter \n")

        text_file = open(output_path, "a")
        text_file.write("\n.tsv file detected, switching delimiter \n")
        text_file.close()

    # pull the data from the file
    raw_data = pd.read_csv(file_path, delimiter=delim, header=0, index_col=False)
    # print(type(data))
    # print the file name & location to the console
    print("Getting data from: ", file_path, "\n")


    # print data shape for reference
    shapestring = "Data shape: {:d} rows by {:d} columns\n \n".format(raw_data.shape[0],raw_data.shape[1])
    print(shapestring)
    colnamestring = "Column names: \n {} \n\n".format(raw_data.columns.values)
    print(colnamestring)

    #write it to file
    text_file = open(output_path, "a")
    text_file.write(shapestring)
    text_file.write(colnamestring)
    text_file.close()

    # how many sensors are we tracking?
    n_sensors = raw_data['Tools'][0]
    n_sensors = int(n_sensors)

    # tell the user
    sensorstring = "Dataset contains tracking data from {:d} sensors:\n".format(n_sensors)
    print(sensorstring)

    #print to file
    text_file = open(output_path, "a")
    text_file.write(sensorstring)
    text_file.close()

    # find the sensor name columns
    sensor_name_cols = np.linspace(1, ((13 * (n_sensors - 1)) + 1), num=n_sensors, dtype=int)

    # find the sensor state columns
    sensor_state_cols = np.linspace(4, ((13 * (n_sensors - 1)) + 4), num=n_sensors, dtype=int)

    # for each sensor
    for i, n in np.ndenumerate(sensor_name_cols):
        # print the column name
        sensornamestring = "Sensor {}: {}\n".format(i[0],raw_data.columns.values[int(n)])
        print(sensornamestring)
        text_file = open(output_path, "a")
        text_file.write(sensornamestring)
        text_file.close()



        # create an array of indices to mask in the raw_data array
        bad_indices = []

    # for each sensor state column
    for i, n in np.ndenumerate(sensor_state_cols):
        # for each row in each column
        for index, value in np.ndenumerate(raw_data[raw_data.columns.values[n]]):
            # if the value isn't OK, add it to the bad indices array
            if value != 'OK':
                bad_indices.append(index[0])

    # remove duplicate bad indices
    bad_indices = list(set(bad_indices))
    percentage_badness = (len(bad_indices) / raw_data.shape[0]) * 100
    badnessstring = "\nData contains {} bad values ({:.2f}%). Discarding...".format(len(bad_indices), percentage_badness)
    print(badnessstring)

    #print to file
    text_file = open(output_path, "a")
    text_file.write(badnessstring)
    text_file.close()


    # drop the bad data
    clean_data = raw_data.drop(bad_indices, axis=0)

    # relative locations of data columns
    # Theta (Latitude) is state col + 1,
    # Phi (Longitude) is state col + 2,
    # Tx is state col + 5,
    # Ty is state col + 6,
    # Tz is state col + 7

    # create an array to hold the path lengths
    Path_lengths = []

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_title('Sensor Path')
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Z (mm)')


    # for each sensor:
    for i, n in np.ndenumerate(sensor_state_cols):
        Tx = clean_data.iloc[:, n + 5]
        Ty = clean_data.iloc[:, n + 6]
        Tz = clean_data.iloc[:, n + 7]

        DeltaTx = Tx.diff()
        DeltaTx = DeltaTx.fillna(0)
        DeltaTxSquared = np.square(DeltaTx)


        DeltaTy = Ty.diff()
        DeltaTy = DeltaTx.fillna(0)
        DeltaTySquared = np.square(DeltaTy)

        DeltaTz = Ty.diff()
        DeltaTz = DeltaTx.fillna(0)
        DeltaTzSquared = np.square(DeltaTz)

        DeltaSum = DeltaTxSquared + DeltaTySquared + DeltaTzSquared
        Path_lengths.append(np.divide(np.sum(np.sqrt(DeltaSum)), 1000))

        if(not clean_data.empty):
            ax.plot(Tx, Ty, Tz, linewidth=1, label=clean_data.iloc[0, n-3])

    sensorpathstring = "Sensor path lengths:\n"
    text_file = open(output_path, "a")
    text_file.write(sensorpathstring)
    text_file.close()

    print(sensorpathstring)

    for i, n in np.ndenumerate(sensor_name_cols):

        pathlengthstring = "Sensor {}: {:05.3f} meters\n".format(i[0], Path_lengths[i[0]])
        print(pathlengthstring)
        text_file = open(output_path, "a")
        text_file.write(pathlengthstring)
        text_file.close()

    if not clean_data.empty:
        plt.xlim((-200, 200))
        plt.ylim((-200, 300))
        ax.set_zlim(-600, -100)
        ax.invert_zaxis()
        plt.legend()
        plt.show()

