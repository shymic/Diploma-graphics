__author__ = 'Andrey'


import matplotlib.pyplot as plt
x=[1000,5000,10000,20000,50000,100000]
y1=[0.949786845,0.95168044,0.947407436,0.948834443,0.948043287,0.947876472]
y2=[0.94712651106442526,0.94712651106442526,0.94712651106442526,0.94712651106442526,0.94712651106442526,0.94712651106442526]
y3=[0.9739070661719972,0.9739070661719972,0.9739070661719972,0.9739070661719972,0.9739070661719972,0.9739070661719972]

h2= plt.plot(x,y1,'o', label=r'$ H_3(\delta) $', color='black')
h3= plt.plot(x,y2,'-', label=r'$ H_3^0(\delta) $', color='black')
h4= plt.plot(x,y3,'-^', label=r'$ H_3^{as}(\delta) $', color='black')
plt.ylim(ymax = 1.0, ymin = 0.9)
#plt.scatter(x, y, label = u'graphic', color='r')
plt.grid(True)
plt.text(0.5, -0.5, r'$ \delta $', fontsize='16')
plt.ylabel(r'$H_3(\delta)$')
plt.xlabel(r'$T$')
plt.title(r'$  \epsilon=0.3,  \delta=0.1 $')
plt.legend()
plt.show()