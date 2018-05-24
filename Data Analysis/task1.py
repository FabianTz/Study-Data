import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib as mpl
import Functions as fn

if __name__ == "__main__":
    data = fn.grabdata()

    #print(data.dtype.names)

    # Task time, error count, dominant hand error count, nondominant hand error count, overall time
    # pull the task start time
    task_start = fn.pulldatawhere(data['Event'],data['Timestamp'],b'TASK_START')

    # pull the timestamp if pattern 3 and Pattern_finish
    break_start = fn.pulldataif(data['Pattern'],data['Event'],data['Timestamp'],3,b'PATTERN_FINISH')

    # pull the break end time
    break_finish = fn.pulldataif(data['Pattern'], data['Event'], data['Timestamp'], 4, b'PATTERN_START')

    # pull the task end time
    task_finish = fn.pulldatawhere(data['Event'],data['Timestamp'],b'TASK_FINISH')

    if len(task_start) > 1:
        print("More than one task start marker found. Please manually repair the data. \n")
        print("Program will now exit.")
        exit()

    print(task_start)