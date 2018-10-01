import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma
import math
import matplotlib as mpl
import Functions as fn

if __name__ == "__main__":

    # file open dialog to select the file to plot
    raw_data = fn.grabdata()
    print(np.shape(raw_data))
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

    # create an array of indices to mask in the raw_data array
    bad_indices = []

    for i, n in np.ndenumerate(sensor_state_cols):

        for index, value in np.ndenumerate(raw_data[raw_data.dtype.names[n]]):

            if value != 'OK':
                bad_indices.append(index[0])

    # remove duplicate bad indices
    bad_indices=list(set(bad_indices))
    print("Data contains ", len(bad_indices), " bad values. Discarding...")

    # create a mask with True in all rows marked by bad_indices
    empty_mask = np.zeros_like(raw_data, dtype=int)
    row_mask = np.ones(len(raw_data[0]), dtype=int)
    print(row_mask)
    for index in enumerate(bad_indices):
        empty_mask[index[1]] = row_mask

    print(empty_mask)
    # print(len(raw_data))
    # print(len(masked_data))