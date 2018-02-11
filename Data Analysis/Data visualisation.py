import datetime
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from mpl_toolkits.mplot3d import Axes3D


if __name__ == "__main__":
	#file open dialog to select the file to plot
	root=tk.Tk()
	root.withdraw()
	file_path = filedialog.askopenfilename()
	#echo back the data source
	print("Getting data from: ", file_path, "\n")
	#pull the data from CSV using genfromtext
	data = np.genfromtxt(file_path, delimiter=',', names=True, dtype=None)

	#print(data.dtype.names)
	
	#tool sensor 1
	Tx = data['Tx']
	Ty = data['Ty']
	Tz = data['Tz']
	print(Tx)

	#tool sensor 2
	Tx_1 = data['Tx_1']
	Ty_1 = data['Ty_1']
	Tz_1 = data['Tz_1']

	#reference sensor
	Tx_2 = data['Tx_2']
	Ty_2 = data['Ty_2']
	Tz_2 = data['Tz_2']

	#create a plot
	fig = plt.figure()
	ax = fig.gca(projection='3d')

	#set plot labels
	ax.set_title('Toolpath visualisation')
	ax.set_xlabel('X (mm)')
	ax.set_ylabel('Y (mm)')
	ax.set_zlabel('Z (mm)')


	ax.scatter(Tx,Ty,Tz,linewidth = 0.1, label = 'Tool Sensor 1', color = 'b')
	ax.scatter(Tx_1,Ty_1,Tz_1,linewidth = 0.1, label = 'Tool Sensor 2', color = 'r')
	ax.scatter(Tx_2,Ty_2,Tz_2,linewidth = 0.1, label = 'Reference Sensor', color = 'g')
	
	plt.xlim((-300,300))
	plt.ylim((-300,300))
	ax.set_zlim(-600,100)
	ax.invert_zaxis()
	
	plt.show()