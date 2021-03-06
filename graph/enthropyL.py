__author__ = 'Andrey'
import matplotlib.pyplot as plt
x=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
y1=[0.999987275,0.979385248,0.972449277,0.968971834,0.966880408,0.965472702,0.964446932,0.963619436,0.96286262,0.962080009,0.961077731,0.959640237,0.957192957,0.95274668,0.94448247]
y2=[0.999994741,0.966813365,0.955740125,0.950198876,0.946865911,0.944629872,0.942995271,0.941707956,0.940600899,0.939541294,0.938328206,0.936709116,0.934073006,0.929495381,0.921739561]
y3=[0.999992334,0.998226563,0.997608238,0.997296741,0.997101607,0.996950874,0.996810436,0.996653444,0.996410113,0.996029436,0.99539662,0.994241021,0.992060738,0.987816226,0.979226438]
y4=[0.999995982,0.99253716,0.989958891,0.988662413,0.987878759,0.987329672,0.986906995,0.986529913,0.986116241,0.985585646,0.984799441,0.983497663,0.981210035,0.976909975,0.968324859]
x2=[2,3,4]
y21=[0.966813365,0.955740125,0.950198876];
y22=[0.979385248,0.972449277,0.968971834];
y23=[0.99253716,0.989958891,0.988662413];
y24=[0.998226563,0.997608238,0.997296741];
h4= plt.plot(x,y3,'-', label=r'$ H_l(0) $', color='black')
h= plt.plot(x,y4,'--', label=r'$ H_l(0.1) $', color='black' , marker='o' , mew=0.5, mfc='1',  c='k')
h2= plt.plot(x,y1,'--o', label=r'$ H_l(0.3) $', color='black')
h3= plt.plot(x,y2,'--^', label=r'$ H_l(0.5) $', color='black')
h20= plt.plot(x2,y21,'o', label=r'$ H_l^o(0.5) $', color='black',marker='v' , mew=0.5, mfc='1',  c='k')
h30= plt.plot(x2,y22,'o', label=r'$ H_l^o(0.3) $', color='black',marker='D' , mew=0.5, mfc='1',  c='k')
h40= plt.plot(x2,y23,'o', label=r'$ H_l^o(0.1) $', color='black',marker='x' , mew=0.5, mfc='1',  c='k')
h00= plt.plot(x2,y24,'o', label=r'$ H_l^o(0) $', color='black',marker='X' , mew=0.5, mfc='1',  c='k')

#plt.ylim(ymax = 0.99, ymin = 0.97)
#plt.scatter(x, y, label = u'graphic', color='r')
plt.grid(True)
plt.text(0.5, -0.5, r'$ \delta $', fontsize='16')
plt.ylabel(r'$H_l(\delta)$')
plt.xlabel(r'$l$')
plt.title(r'$  \epsilon=0.35 $')
plt.legend()
plt.show()