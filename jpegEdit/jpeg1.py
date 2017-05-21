from PIL import Image
from numpy import*

def simple():
    temp=asarray(Image.open('d:\\e.jpg'))
    x=temp.shape[0]
    y=temp.shape[1]*temp.shape[2]
    temp.resize((x,y)) # a 2D array
    return temp



def s1():
    temp=Image.open('d:\\e.jpg')
    temp=temp.convert('1')      # Convert to black&white
    A = array(temp)             # Creates an array, white pixels==True and black pixels==False
    new_A=empty((A.shape[0],A.shape[1]),None)    #New array with same size as A

    for i in range(len(A)):
        for j in range(len(A[i])):
            if A[i][j]==True:
                new_A[i][j]=0
            else:
                new_A[i][j]=1
    print(new_A)


arr= simple()
print(arr)