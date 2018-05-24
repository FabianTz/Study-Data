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
    delim = ","
    if file_path[-4:] == ".tsv":
        delim = "\t"
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


def getvectorcomponents(theta,phi,r=1):

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


def getdotproduct(x1,y1,z1,x2,y2,z2):

    dots = []

    for i,n in np.ndenumerate(x1):
        inner = np.inner([x1[i[0]], y1[i[0]], z1[i[0]]], [x2[i[0]],y2[i[0]], z2[i[0]]])
        dots.append(inner)
    return dots



