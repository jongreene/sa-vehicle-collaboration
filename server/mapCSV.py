import sys, os
import numpy as np 

def mapCSV(csv_file):
    # make sure the file exists and is correct
    if not os.path.isfile(csv_file) or '.csv' not in str(csv_file):
        print('Error: File either does not exist or is not a csv')
        sys.exit()
    
    # generate a numpy array from the csv with type float
    m1 = np.genfromtxt(csv_file, dtype=float, delimiter=',')

    # TODO: search and correct for missing csv values 

    #return the gradient of the map
    g1 = np.gradient(m1)
    print(g1)