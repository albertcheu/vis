import matplotlib.pyplot as plt
import numpy as np
from splom import splom as splom
splom([[1,10,100,50],[2,20,200,60],[3,30,300,70],[4,40,400,80]],('w','x','y','z'),plt,np)
plt.show()
