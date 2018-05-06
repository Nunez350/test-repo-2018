# Author: Jingwen Qian ID:108660470 ----------PHY546-Final Assignment

'''The following work is related to a project in collaboration with professor
Robert Harrison and a PHD student, Hongchen Wu. The function readmat() is a
collaborated work from us, here I used it as a reference to introduce
the function GetInteractionMap() which is coded by myself'''

import numpy as np
import matplotlib.pyplot as plt

def readmat(filename):
    f = open(filename,'r')
    f.readline()

    line = f.readline()
    natom = int(line)

    f.readline()
    
    nneigh = [0]*natom
    for iatom in range(natom):
        line = f.readline()
        fields = line.split()
        atomnum = int(fields[0])
        numneigh = int(fields[1])
        norb = int(fields[2])
        if norb != 4:
            raise ValueError("assuming norb=4")
        nneigh[iatom] = numneigh

    nrows = ncols = 4 * natom
    M = np.zeros((nrows,ncols))
    
    for iatom in range(natom):
        for neigh in range(nneigh[iatom]):
            f.readline()
            line = f.readline()
            fields = line.split()
            iatom1 = int(fields[0])
            ineigh = int(fields[1])
            iatom2 = int(fields[2])
            if iatom1 != iatom+1:
                raise ValueError("iatom1 != iatom+1")
            if neigh != ineigh:
                raise ValueError("neigh != ineigh")
       
            f.readline()
        
            ilo = (iatom1-1)*4
            jlo = (iatom2-1)*4

            i = ilo
            for linenum in range(4): 
                line = f.readline()
                fields = line.split()
                j = jlo
                for value in fields: 
                    value = float(value)
                    M[i,j] = value
                    M[j,i] = M[i,j]
                    j = j+1
                i = i+1
    return M

# readmat() returns the matrix that we want to work on

'''Starting from here is solely my code. The general idea is to check if atom i and
atom j are neighbors with each other. If they are neighbors, then we assign
the cell value to 1, the corresponding index is [i-1,j-1]; 0, otherwise.'''

def getInteractionMap():
    # We have multiple files that are in the same format
    # First, ask the user for the file that he/she wants to work on
    file_name = input("To plot an interaction map, please enter the file name: ")
    
    # To get the total number of atoms 
    file = open(file_name,'r')
    file.readline()
    line = file.readline()
    num_atom = int(line)

    file.readline()

    # To get the total number of neighbors
    t_neighbor = 0
    for num in range (num_atom):
        line = file.readline()
        l = line.split()
        num_neighbor = int(l[1])
        t_neighbor = t_neighbor + num_neighbor

    # Create a matrix that stores the values which are used to make the map
    m = np.zeros((num_atom,num_atom))

    # Loop through every atom 
    for number in range(t_neighbor):
        file.readline()
        line = file.readline()
        l = line.split()   
        atom1_index = int(l[0])
        atom2_index = int(l[2])
        m[atom1_index-1,atom2_index-1] = 1
        m[atom2_index-1,atom1_index-1] = 1
        for i in range(5):
            file.readline()
        dim = m.shape
        
    print("This is what the first 10 by 10 matrix looks like:")
    print(m[0:10,0:10])
    
    # Generating the map
    plt.imshow(m,cmap='Purples')
    plt.title("Atom Interaction Map",loc='center',fontsize=12,fontweight='bold')
    ax = plt.gca()
    ax.invert_yaxis()
    plt.show()

    return "Map is generated."+"\n"+"The dimension is: "+str(dim)

# For example, the file "hamreal1-C.dat" is what we want to work on
# Enter file name "hamreal1-C.dat" when the input message pops out
print(getInteractionMap())

# The output shows that the resulted matrix is 961 by 961
M = readmat("hamreal1-C.dat")

# Do a simple check to make sure that the matrix we got is the right one
# Here we can do mutiple simple tests, for example:
print("The two partial matrices associated with the first two interaction info:")
print(M[0:4,0:4])
print(M[556:560,0:4])

print("The dimension of M is: ", M.shape)

# Since M is composed with many 4 by 4 matrices, so the dimentions match.
# By further observation, we are sure we got the right interaction matrix.









    








