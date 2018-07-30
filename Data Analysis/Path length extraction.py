import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib as mpl
import Functions as fn

if __name__ == "__main__":

    # file open dialog to select the file to plot
    raw_data = fn.grabdata()

    # how many sensors are we tracking?
    n_sensors = raw_data['Tools'][0]

    # tell the user
    print("Dataset contains tracking data from ", n_sensors, " sensors:")

    # find the sensor name columns
    sensor_name_cols = np.linspace(1, ((13 * (n_sensors - 1)) + 1), num=n_sensors, dtype=int)

    # find the sensor state columns
    sensor_state_cols = np.linspace(4, ((13 * (n_sensors - 1)) + 4), num=n_sensors, dtype=int)

    # for each sensor
    for i, n in np.ndenumerate(sensor_name_cols):

        # print the column name
        print("Sensor ", i[0], ":", raw_data.dtype.names[int(n)])

    for i, n in np.ndenumerate(sensor_state_cols):

        for index, value in np.ndenumerate(raw_data[raw_data.dtype.names[n]]):

            print(value)
