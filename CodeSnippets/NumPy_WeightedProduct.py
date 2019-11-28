
__version__ = '0.1'
__date__ = '28-11-2019'
__author__ = 'Shervin Azadi & Pirouz Nourian'

import numpy as np
node = hou.pwd()

#function to put the attributes of the houdini geometry into a numpy array
def attrib_to_nparray(input_index, attributeList):
    
    #loading the geometry of the corresponding input
    geo = node.inputGeometry(input_index)

    #read the name of the attributes
    attribs = attributeList
    #counting the number of the elements of the attributes (vectors have more than one for eg)
    numElementAttrib = 0
    for attrib in attribs:
        #retrieve the attribute value
        val = geo.iterPoints()[0].attribValue(attrib)
        if isinstance(val, tuple):
            numElementAttrib += len(val)
        else:
            numElementAttrib += 1
    #getting the number of the points
    numpt = len(geo.iterPoints())
    # initialize the numpy array
    DataSet = np.zeros((numpt,numElementAttrib), dtype=float)

    # iterate over points
    for i in range(numpt):
        
        #iterate over attribs
        j = 0
        for attrib in attribs:

            #retrieve the attribute value
            val = geo.iterPoints()[i].attribValue(attrib)
            
            #check if it is a vector
            if isinstance(val, tuple):
                #iterate over the vector elements and store all of them
                for k in range(len(val)):
                    DataSet[i][j] = val[k]
                    j += 1
            else:
                DataSet[i][j] = val
                j += 1
    return (DataSet)

#function to write the data of a numpy array onto the houdini geometry
def nparray_to_attrib(DataSet, name):
    #load the main geometry
    geo = node.geometry()
    #iterate over columns of DataSet (attributes)
    for j in range(DataSet.shape[1]):
        #create the name of the attribute
        attribName = name + str(j)
        #initialize the attribute in the geometry
        geo.addAttrib(hou.attribType.Point, attribName, 0.0)
        #iterate over the rows of DataSet (points)
        for i in range(DataSet.shape[0]):
            # read the value that corresponds to each point from DataSet and write it to the attribute
            geo.iterPoints()[i].setAttribValue(attribName, DataSet[i][j])

#read the attribute list for voxels
attribs_0 = hou.evalParm("attribs_0").split(',')
#put the VoxelData in a numpy array
VoxelData = attrib_to_nparray(0, attribs_0)

#read the attribute list for functions
attribs_1 = hou.evalParm("attribs_0").split(',')
#put the FunctionData in a numpy array
FunctionData = attrib_to_nparray(1, attribs_1)

#initialize the WP matrix with the number of points as the numberof rows AND number of functions as number of attributes
WeightedProduct = np.zeros((VoxelData.shape[0],FunctionData.shape[0]), dtype=float)

#iterate of the functions 
for i in range(FunctionData.shape[0]):
    #raising each voxel value to the power of the function criteria
    powers = np.float_power(VoxelData, FunctionData[i])
    #multiplying all the value powers together for each voxel
    product = np.prod(powers, axis=1)
    #placing the result in the corresponding column of the wweighted product matrix
    WeightedProduct[:,i] = product

#place the calculated WP as attribute 'func' on the voxels
nparray_to_attrib(WeightedProduct, "func")