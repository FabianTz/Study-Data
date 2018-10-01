import tkinter as tk
from tkinter import filedialog
import numpy as np
import math
import pandas as pd


def grab_data():
    # file open dialog to select the file to work on
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    # by default expect a csv
    delim = ","

    # if a tsv is found, switch delimiter to a tab character
    if file_path[-4:] == ".tsv":
        delim = "\t"
        # warn the user that this is a tab sep file
        print("\n.tsv file detected, switching delimiter \n")

    # pull the data from the file
    data = pd.read_csv(file_path, delimiter=delim, header=0, index_col=False)
    # print(type(data))
    # print the file name & location to the console
    print("Getting data from: ", file_path, "\n")

    # return the data array
    return data


def segment_length(x1, y1, z1, x2, y2, z2):

    delta_x_squared = (x2 - x1)**2
    delta_y_squared = (y2 - y1)**2
    delta_z_squared = (z2 - z1)**2

    l = math.sqrt((delta_x_squared + delta_y_squared + delta_z_squared))

    return l
