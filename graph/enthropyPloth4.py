import matplotlib.pyplot as plt
x=[1000,5000,10000,20000,50000,100000]
y1=[0.974967133,0.979715457,0.977754276,0.978062762,0.978098969,0.978341117]
y2=[0.97880738247996453,0.97880738247996453,0.97880738247996453,0.97880738247996453,0.97880738247996453,0.97880738247996453]
y3=[0.9806926533994359,0.9806926533994359,0.9806926533994359,0.9806926533994359,0.9806926533994359,0.9806926533994359]

h2= plt.plot(x,y1,'o', label=r'$ H_4(\delta) $', color='black')
h3= plt.plot(x,y2,'-', label=r'$ H_4^0(\delta) $', color='black')
h4= plt.plot(x,y3,'-^', label=r'$ H_4^{as}(\delta) $', color='black')
plt.ylim(ymax = 0.99, ymin = 0.97)
#plt.scatter(x, y, label = u'graphic', color='r')
plt.grid(True)
plt.text(0.5, -0.5, r'$ \delta $', fontsize='16')
plt.ylabel(r'$H_4(\delta)$')
plt.xlabel(r'$T$')
plt.title(r'$  \epsilon=0.3,  \delta=0.3 $')
plt.legend()
plt.show()