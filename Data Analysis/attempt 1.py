import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib as mpl
import matplotlib.cm as cmx
import matplotlib.colors as colors
from mpl_toolkits.mplot3d import Axes3D
import Functions as fn

import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

if __name__ == "__main__":

    # file open dialog to select the file to plot
    raw_data = fn.grabdata()

    # how many sensors are we tracking?
    n_sensors = raw_data['Tools'][0]

    # tell the user
    print("Dataset contains tracking data from ", n_sensors, " sensors:")

    # find the sensor name columns
    sensor_name_cols = np.linspace(1,((13*(n_sensors-1))+1),num=n_sensors)

    # for each sensor
    for i,n in np.ndenumerate(sensor_name_cols):
        # print the column name
        print("Sensor ",i[0],":",raw_data.dtype.names[int(n)])

    times = np.divide(np.subtract(raw_data['Frame'],raw_data['Frame'][0]),40)

    Tx = []
    Ty = []
    Tz = []
    Theta = []
    Phi = []

    Tx_1 = []
    Ty_1 = []
    Tz_1 = []
    Theta_1 = []
    Phi_1 = []

    Tx_2 = []
    Ty_2 = []
    Tz_2 = []
    Theta_2 = []
    Phi_2 = []

    OK_times = []

    discarded_frames = []

    clean_data = []

    for i, n in np.ndenumerate(raw_data['State']):

        if raw_data['State'][i[0]] == 'OK' and raw_data['State_1'][i[0]] == 'OK' and raw_data['State_2'][i[0]] == 'OK':

            Tx.append(raw_data['Tx'][i[0]])
            Ty.append(raw_data['Ty'][i[0]])
            Tz.append(raw_data['Tz'][i[0]])
            Theta.append(raw_data['Latitude'][i[0]])
            Phi.append(raw_data['Longitude'][i[0]])

            Tx_1.append(raw_data['Tx_1'][i[0]])
            Ty_1.append(raw_data['Ty_1'][i[0]])
            Tz_1.append(raw_data['Tz_1'][i[0]])
            Theta_1.append(raw_data['Latitude_1'][i[0]])
            Phi_1.append(raw_data['Longitude_1'][i[0]])

            Tx_2.append(raw_data['Tx_2'][i[0]])
            Ty_2.append(raw_data['Ty_2'][i[0]])
            Tz_2.append(raw_data['Tz_2'][i[0]])
            Theta_2.append(raw_data['Latitude_2'][i[0]])
            Phi_2.append(raw_data['Longitude_2'][i[0]])

            OK_times.append(times[i[0]])

        else:
            discarded_frames.append(i[0])

    discard_percentage = len(discarded_frames) / len(raw_data['Frame'])*100
    discard_percentage = round(discard_percentage,2)

    print("\n")
    print(len(discarded_frames), "of", len(raw_data['Frame']), "frames discarded due to bad values (",discard_percentage,"%)")

    Sensor_0 = np.column_stack((Tx, Ty, np.multiply(Tz,-1), Theta, Phi))
    Sensor_1 = np.column_stack((Tx_1, Ty_1, np.multiply(Tz_1, -1), Theta_1, Phi_1))
    Sensor_2 = np.column_stack((Tx_2, Ty_2, np.multiply(Tz_2, -1), Theta_2, Phi_2))

    Time_delta = np.diff(OK_times)

    #Sensor_0_delta_pos = np.column_stack((np.diff(Sensor_0[:, 0], n=1),
    #                                      np.diff(Sensor_0[:, 1], n=1),
    #                                      np.diff(Sensor_0[:, 2], n=1),
    #                                      np.diff(Sensor_0[:, 3], n=1),
    #                                      np.diff(Sensor_0[:, 4], n=1),
    #                                      Time_delta))

    #Sensor_0_distance = np.sqrt(np.add(np.add(np.square(Sensor_0_delta_pos[:,0]),np.square(Sensor_0_delta_pos[:,1])),np.square(Sensor_0_delta_pos[:,2])))
    #Sensor_0_velocities = np.divide(Sensor_0_distance,Sensor_0_delta_pos[:,5])

    #elapsed_time = np.cumsum(Sensor_0_delta_pos[:,5])





    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ax.set_title('Toolpath visualisation')
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Z (mm)')
    #ax.invert_zaxis()

    ax.plot(Sensor_0[:,0],Sensor_0[:,1],Sensor_0[:,2])
    ax.plot(Sensor_1[:, 0], Sensor_1[:, 1], Sensor_1[:, 2])
    ax.plot(Sensor_2[:, 0], Sensor_2[:, 1], Sensor_2[:, 2])
    plt.show()
