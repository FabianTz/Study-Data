import tkinter as tk
from tkinter import filedialog
import numpy as np
import math


def grabdata():

    # file open dialog to select the file to plot
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    # be smart about selecting the correct delimiter, be it a comma or tab sep
    delim = b','
    if file_path[-4:] == ".tsv":
        delim = b'\t'
        print("\n.tsv file detected, switching delimiter \n")

    data = np.genfromtxt(file_path, delimiter=delim, names=True, dtype=None, encoding=None)
    print("Getting data from: ", file_path, "\n")
    # print("Raw data: \n")
    # print(data.dtype.names)
    return data


def pullsamelengthdatawhere(statearray, statearray_1, dataarray, criterion='OK'):
    outputarray = []
    # for every row in the table
    for i, n in np.ndenumerate(statearray):

        # only include data where the sensor tracked OK
        if statearray[i] == criterion and statearray_1[i] == criterion:
            outputarray.append(dataarray[i])

    return outputarray


def pulldatawhere(statearray, dataarray, criterion):
    outputarray = []
    # for every row in the table
    for i, n in np.ndenumerate(statearray):

        # only include data where the sensor tracked OK
        if statearray[i] == criterion:
            outputarray.append(dataarray[i])

    return outputarray

def pulldataif(statearray, statearray_1, dataarray, criterion, criterion_1):
    outputarray = []
    # for every row in the table
    for i, n in np.ndenumerate(statearray):

        # only include data where the sensor tracked OK
        if statearray[i] == criterion and statearray_1[i] == criterion_1:
            outputarray.append(dataarray[i])

    return outputarray


def getvectorcomponents(theta, phi, r=1):

    u = []
    v = []
    w = []

    thetaradians = np.deg2rad(theta)
    phiradians = np.deg2rad(phi)

    for i, n in np.ndenumerate(thetaradians):
        ucomponent = math.cos(phiradians[i]) * math.sin(thetaradians[i]) * r
        vcomponent = math.sin(phiradians[i]) * math.sin(thetaradians[i]) * r
        wcomponent = math.cos(thetaradians[i]) * r

        u.append(ucomponent)
        v.append(vcomponent)
        w.append(wcomponent)

    return u, v, w


def getdotproduct(x1, y1, z1, x2, y2, z2):

    dots = []

    for i,n in np.ndenumerate(x1):
        inner = np.inner([x1[i[0]], y1[i[0]], z1[i[0]]], [x2[i[0]],y2[i[0]], z2[i[0]]])
        dots.append(inner)
    return dots


def badfits(Tx0, Ty0, Tz0, Theta0, Phi0, index0, Txn, Tyn, Tzn, Thetan, Phin, indexn):

    # how many consecutive bad frames?
    n = indexn - index0

    # that is, I need to divide by n+1
    # div = n + 1

    # get the deltas
    DeltaTx = Txn - Tx0
    DeltaTy = Tyn - Ty0
    DeltaTz = Tzn - Tz0
    DeltaTheta = Thetan - Theta0
    DeltaPhi = Phin - Phi0

    # divide deltas by div to get the delta for each segment

    SegmentDeltaTx = DeltaTx / n # div
    SegmentDeltaTy = DeltaTy / n # div
    SegmentDeltaTz = DeltaTz / n # div
    SegmentDeltaTheta = DeltaTheta / n # div
    SegmentDeltaPhi = DeltaPhi / n # div

    # create arrays to store the interpolated values and interpolate

    Tx_interpolated = np.linspace(Tx0, Txn, n, endpoint=False)
    Ty_interpolated = np.linspace(Ty0, Tyn, n, endpoint=False)
    Tz_interpolated = np.linspace(Tz0, Tzn, n, endpoint=False)
    Theta_interpolated = np.linspace(Theta0, Thetan, n, endpoint=False)
    Phi_interpolated = np.linspace(Phi0, Phin, n, endpoint=False)

    # return an ndarray for the values
    ret = np.array([Tx_interpolated,Ty_interpolated,Tz_interpolated,Theta_interpolated,Phi_interpolated])
    ret = np.transpose(ret)
    return ret

