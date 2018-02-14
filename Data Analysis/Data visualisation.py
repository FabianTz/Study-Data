import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

if __name__ == "__main__":
    # file open dialog to select the file to plot
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    # echo back the data source
    print("Getting data from: ", file_path, "\n")
    # pull the data from CSV using genfromtext
    data = np.genfromtxt(file_path, delimiter=',', names=True, dtype=None)
    # print(data.dtype.names)
    # print(data['Frame'].dtype)
    # first, strip the dodgy values
    # create array variables to hold my coordinate data
    # tool sensor 1
    Tx = []
    Ty = []
    Tz = []
    Theta = []
    Phi = []

    # tool sensor 2
    Tx_1 = []
    Ty_1 = []
    Tz_1 = []
    Theta_1 = []
    Phi_1 = []

    # reference sensor
    Tx_2 = []
    Ty_2 = []
    Tz_2 = []

    Frames = []

    for i, n in np.ndenumerate(data['State']):

        # only include tool sensor data and frame numbers if both sensor readings are OK
        if data['State'][i] == b'OK' and data['State_1'][i] == b'OK':
            Tx.append(data['Tx'][i])
            Ty.append(data['Ty'][i])
            Tz.append(data['Tz'][i])
            Theta.append(data['Latitude'][i])
            Phi.append(data['Longitude'][i])

            Tx_1.append(data['Tx_1'][i])
            Ty_1.append(data['Ty_1'][i])
            Tz_1.append(data['Tz_1'][i])
            Theta_1.append(data['Latitude_1'][i])
            Phi_1.append(data['Longitude_1'][i])

            Frames.append(data['Frame'][i])

        # sensor 3 is independent, so it doesn't really matter if the array is the same length
        if data['State_2'][i] == b'OK':

            Tx_2.append(data['Tx_2'][i])
            Ty_2.append(data['Ty_2'][i])
            Tz_2.append(data['Tz_2'][i])

    # create arrays to hold my vector components
    u = []
    v = []
    w = []

    u_1 = []
    v_1 = []
    w_1 = []

    r = 1

    # convert my elevation and azimuth angles to radians
    ThetaRadians = np.deg2rad(Theta)
    PhiRadians = np.deg2rad(Phi)
    Theta_1Radians = np.deg2rad(Theta_1)
    Phi_1Radians = np.deg2rad(Phi_1)

    # now use them to derive the x, y and z components of my vectors
    for index, n in np.ndenumerate(Tx):
        uComponent = math.cos(PhiRadians[index]) * math.sin(ThetaRadians[index]) * r
        vComponent = math.sin(PhiRadians[index]) * math.sin(ThetaRadians[index]) * r
        wComponent = math.cos(ThetaRadians[index]) * r

        u.append(uComponent)
        v.append(vComponent)
        w.append(wComponent)

        uComponent = math.cos(Phi_1Radians[index]) * math.sin(Theta_1Radians[index]) * r
        vComponent = math.sin(Phi_1Radians[index]) * math.sin(Theta_1Radians[index]) * r
        wComponent = math.cos(Theta_1Radians[index]) * r

        u_1.append(uComponent)
        v_1.append(vComponent)
        w_1.append(wComponent)



    # create variable to hold the velocity array
    Velocities = []

    # for graphing purposes, grab the time signature of each point
    Times = np.divide(np.subtract(Frames,Frames[0]),40)

    # work out the position between the sensors, on the tool axis
    CenterLineX = np.divide(np.add(Tx, Tx_1), 2)
    CenterLineY = np.divide(np.add(Ty, Ty_1), 2)
    CenterLineZ = np.divide(np.add(Tz, Tz_1), 2)

    DeltaT = 0
    # calculate velocities
    for i, n in np.ndenumerate(CenterLineX):

        # prevent off-by one index out of range exceptions
        if (i[0] + 1) < len(Tx):

            if Frames[i[0]] > 0:
                DeltaT = (Frames[i[0] + 1] - Frames[i[0]])/40

            else:
                DeltaT = 1/40

            DeltaXSquared = (CenterLineX[i[0] + 1] - CenterLineX[i[0]]) ** 2
            DeltaYSquared = (CenterLineY[i[0] + 1] - CenterLineY[i[0]]) ** 2
            DeltaZSquared = (CenterLineZ[i[0] + 1] - CenterLineZ[i[0]]) ** 2

            Sum = DeltaXSquared + DeltaYSquared + DeltaZSquared

            DeltaPosition = math.sqrt(Sum)

            Velocities.append(DeltaPosition / DeltaT)

    # create a plot
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # set plot labels
    ax.set_title('Toolpath visualisation')
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Z (mm)')

    ax.plot(CenterLineX,CenterLineY,CenterLineZ,linewidth = 0.5, label = 'Tool Axis', color = 'b')
    ax.plot(Tx,Ty,Tz,linewidth = 0.1, label = 'Tool Sensor 1', color = 'r')
    ax.plot(Tx_1,Ty_1,Tz_1,linewidth = 0.1, label = 'Tool Sensor 2', color = 'r')
    ax.plot(Tx_2,Ty_2,Tz_2,linewidth=0.1, label='Reference Sensor', color='g')

    plt.xlim((-200, 200))
    plt.ylim((-200, 300))
    ax.set_zlim(-600, -100)
    ax.invert_zaxis()

    plt.show()

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.quiver(Tx, Ty, Tz, u, v, w, length=8, normalize=True, color='r', linewidth=0.1)
    ax.quiver(Tx_1, Ty_1, Tz_1, u_1, v_1, w_1, length=8, normalize=True, color='r', linewidth=0.1)
    plt.xlim((-200, 200))
    plt.ylim((-200, 300))
    ax.set_zlim(-600, -100)
    ax.invert_zaxis()
    plt.show()

    fig = mpl.pyplot.figure(1)
    fig.suptitle = "Raw Sensor Movement Data"

    plt.subplot(221)
    plt.title("Sensor velocity")
    plt.xlabel('Time (S)')
    plt.ylabel('Velocity (mm/s)')
    plt.plot(Times[0:-1],Velocities)
    plt.show()


