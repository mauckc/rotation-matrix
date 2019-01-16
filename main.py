# This program loads a binary file containing 3D point cloud data formated
# as a list of 3-tuples (floats) corresponding to the (x,y,z) coordinates of a
# collection of points i.e. (point cloud)

import numpy as np
import array
import math

# set rotation axis to be the z-axis
axis = [0., 0., 1.]
# set rotation degree in radians
theta = 1.2

def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the user specified axis by theta radians.
    """
    # convert the input to an array
    axis = np.asarray(axis)
    # Get unit vector of our axis
    axis = axis/math.sqrt(np.dot(axis, axis))
    # take the cosine of out rotation degree in radians
    a = math.cos(theta/2.0)
    # get the rest rotation matrix components
    b, c, d = -axis*math.sin(theta/2.0)
    # create squared terms
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    # create cross terms
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    # return our rotation matrix

    return np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)],
                     [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)],
                     [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]])
# TO DO: make num_lon read from first 32-bit integer of binary file tc1.bin
num_lon = 50
num_lat = 3
tmpfile = "tc1.bin"

fileobj = open(tmpfile, mode='rb')
binvalues = array.array('f')
binvalues.read(fileobj, num_lon * num_lat)

# create data numpy array of floats
data = np.array(binvalues, dtype=float)
# reshape array to data dimensions (3,50)
data = np.reshape(data, (num_lon, num_lat))

#dt = np.dtype({'col1': ('int', 0), 'col2': (np.float32, 8),    'col3': (np.float32, 12),'col4': (np.float32, 16)})
#dt = np.dtype({'names': ['index','x','y','z'],'formats': [np.int8, np.float32, np.float32, np.float32]})
#dt = np.dtype("i4,f8,f8,f8")
# format initial point data set
#indata = np.zeros(shape=(num_lon+1, num_lat+1),dtype=dt)
#outdata = np.zeros(shape=(num_lon+1, num_lat+1),dtype=dt)
indata = np.zeros(shape=(num_lon+1, num_lat+1),dtype=np.float)
outdata = np.zeros(shape=(num_lon+1, num_lat+1),dtype=np.float)

infile = np.zeros(shape=(num_lon, num_lat),dtype=np.float)
outfile = np.zeros(shape=(num_lon, num_lat),dtype=np.float)

# index for iterating through array points
index = 0

# set header to the count number of 3D points and three zeros in first rows
indata[0]=[num_lon,0.,0.,0.]
outdata[0]=[num_lon,0.,0.,0.]
#index +=1
# run through length of data array to process all points
while index < num_lon:

    # print indexed array before rotation
    #print(index,data[index][0],data[index][1],data[index][2])
    # format original input 3D point cloud points
    indata[index+1]=[index+1., np.float16(data[index][0]), data[index][1], data[index][2]]

    # store current array as temporary vector to rotate
    v = [data[index][0],data[index][1],data[index][2]]

    # rotate the vector by performing a dot product with the rotation matrix
    outdata[index+1]=[index+1., np.dot(rotation_matrix(axis,theta), v)[0], np.dot(rotation_matrix(axis,theta), v)[1], np.dot(rotation_matrix(axis,theta), v)[2]]

    # populate our in and out files with only the x y z coords of our points
    infile[index] = [indata[index][1],indata[index][2],indata[index][3]]
    outfile[index] = [outdata[index][1],outdata[index][2],outdata[index][3]]

    # iterate the index
    index += 1

# print data arrays to the screen
#print(data)
print(indata)
print(outdata)


# PLOT DATA
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import random

fig = plt.figure()


ax = fig.add_subplot(111, projection='3d')

Xin = infile[:, [0]]
Yin = infile[:, [1]]
Zin = infile[:, [2]]

Xout = outfile[:, [0]]
Yout = outfile[:, [1]]
Zout = outfile[:, [2]]

#ax.plot_wireframe(Xin, Yin, Zin)
# Plot in and out data before and after rotation with colors and markers
ax.scatter(Xin, Yin, Zin, c='b', marker = 'o')
ax.scatter(Xout, Yout, Zout,c='r', marker= '^')

#ax.plot(Xin[1],Yin[1],Zin[1],Xout[1],Yout[1],Zout[1])

# Label the axes with our three space
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()


# todo: Could add specify data format(.dat instead or dtype option)
# save data arrays as files
#np.savetxt('indata.csv', indata, delimiter=',')
#np.savetxt('outdata.csv', outdata, delimiter=',')
#np.savetxt('convertedbinary.csv', data, delimiter=',')
#np.savetxt('infile.csv', infile, delimiter=',')
#np.savetxt('outfile.csv', outfile, delimiter=',')

fileobj.close()
