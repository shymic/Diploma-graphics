__author__ = 'Andrey'
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import math


def h3_delta(delta,eps):
    p111 = (eps*(eps+2)*pow(delta,2)-2*eps*(eps+2)*delta+pow(1+eps,2))/8
    p110 = (-pow(eps,2)*pow(delta,2)+2*pow(eps,2)*delta+1-pow(eps,2))/8
    p101 = (eps*(eps-2)*pow(delta,2)-2*eps*(eps-2)*delta+pow(1-eps,2))/8
    res = -2*p111*math.log(p111,2)-4*p110*math.log(p110,2)-2*p101*math.log(p101,2)
    return res


if __name__=='__main__':
    params = {'axes.linewidth': 0.5,
              'xtick.labelsize': 8,
              'ytick.labelsize': 8,
              'font.family': 'serif',
              'xtick.major.size': 3,
              'ytick.major.size': 3,
              'legend.fontsize': 8,
              'savefig.dpi': 72,
              'savefig.facecolor': 'white',
              'savefig.edgecolor': 'white'}
    mpl.rcParams.update(params)

    my_ms = 4.5
    w120 = 5.50
    w80 = 3.55
    hw120 = 2.55
    hw80 = 2.2

    k = 50
    h3 = [0 for _ in range(k)]
    eps = 0.12
    p1 = 0.5*(1+eps)
    h3_0 = 2*(-p1*math.log(p1,2)-(1-p1)*math.log(1-p1,2))+math.log(2,2)
    x = [0 for _ in range(k)]
    delta = 0
    delta_h = 0.002
    for i in range(k):
        x[i] = delta
        tmp1 = h3_0+2*eps*delta*math.log((1+eps)/(1-eps),2)
        tmp2 = h3_delta(delta,eps)
        h3[i] = (tmp1-tmp2)/tmp2
        delta += delta_h
    print (h3[:5])
    x=[0.01,0.03,0.05,0.07,0.09,0.11,0.13,0.15,0.17,0.19,0.21,0.23,0.25,0.27,0.29,0.31,0.33,0.35,0.37,0.39,0.41]
    y1=[-6.26E-06,-5.56E-05,-1.52E-04,-2.94E-04,-4.80E-04,-7.07E-04,-9.74E-04,-0.001279244,-0.001620475,-0.001996241,-0.002404881,-0.00284478,-0.00331436,-0.00381209,-0.004336478,-0.004886076,-0.005459476,-0.006055312,-0.006672259,-0.007309034,-0.007964393]
    y2=[-1.26E-05,-1.12E-04,-3.06E-04,-5.91E-04,-9.63E-04,-0.001418628,-0.001953655,-0.002564593,-0.003247914,-0.004000191,-0.004818088,-0.005698363,-0.006637862,-0.007633524,-0.008682373,-0.009781519,-0.01092816,-0.012119574,-0.013353127,-0.014626265,-0.015936516]
    y3=[3.65E-04,9.85E-04,0.001462479,0.00180299,0.002012816,0.002097736,0.002063365,0.001915159,0.001658424,0.001298314,8.40E-04,2.88E-04,-3.53E-04,-0.001077795,-0.001882427,-0.002762445,-0.003713648,-0.004731963,-0.005813443,-0.006954265,-0.008150727]

    f = plt.gcf()
    plt.plot(x, y3, '-', linewidth=0.5, marker='o', mew=0.5, mfc='1', ms=my_ms, c='k')
    f.set_size_inches(w80,hw80)
    plt.show()
   #plt.savefig('h4.eps', transparent=False, bbox_inches='tight', pad_inches=0.1)
    plt.clf()

    plt.close()
