


import matplotlib.pyplot as plt
x=[1000,10000,20000,30000,40000,50000,60000,70000,80000,90000,100000]
y1=[0.994472147,0.992240725,0.991372012,0.991999901,0.993466905,0.99220474,0.991979664,0.992120725,0.991568017,0.992455848,0.99245316]
y2=[0.9923391496082595,0.9923391496082595,0.9923391496082595,0.9923391496082595,0.9923391496082595,0.9923391496082595,0.9923391496082595,0.9923391496082595,0.9923391496082595,0.9923391496082595,0.9923391496082595]
y3=[1.0655850785879326,1.0655850785879326,1.0655850785879326,1.0655850785879326,1.0655850785879326,1.0655850785879326,1.0655850785879326,1.0655850785879326,1.0655850785879326,1.0655850785879326,1.0655850785879326]

h2= plt.plot(x,y1,'o', label=r'$ H_2(\delta) $', color='black')
h3= plt.plot(x,y2,'-', label=r'$ H_2^0(\delta) $', color='black')
h4= plt.plot(x,y3,'-^', label=r'$ H_2^{as}(\delta) $', color='black')
plt.ylim(ymax = 1.1, ymin = 0.95)
#plt.scatter(x, y, label = u'graphic', color='r')
plt.grid(True)
plt.text(0.5, -0.5, r'$ \delta $', fontsize='16')
plt.ylabel(r'$H_2(\delta)$')
plt.xlabel(r'$T$')
plt.title(r'$  \epsilon=0.35,  \delta=0.3 $')
plt.legend()
plt.show()