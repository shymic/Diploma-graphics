#(1,1) model, HMC(1)

import sys
import math
import random
import hm
import numpy as np


def get_ps(p):
    n = len(p)
    ps = [0 for _ in range(n+1)]
    for i in range(n):
        ps[i+1] = ps[i]+p[i]
    return ps

def discr_distr(p):
    n = len(p)
    x = random.random()
    res = 0
    i = 0
    while x > p[i]:
        i += 1
    if i!=0:
        res = i-1
    else:
        res = 0
    return res

def bi_law(alpha):
    x = random.random()
    if (x<=alpha):
        result = 1
    else:
        result = 0
    return result

def gen_bi_mc(p, n):
    random.seed()
    ps = [0 for _ in range(2)]
    for i in range(2):
        ps[i] = get_ps(p[i])
    x = [0 for _ in range(n)]
    #modeling x
    x[0] = discr_distr([0,0.5,1])
    for i in range(1,n):
        xpr = x[i-1]
        x[i] = discr_distr(ps[xpr])
    return x

def get_gamma_11(delta, n):
    gamma = [0 for _ in range(n)]
    k = 0
    for i in range(n):
        zeta = bi_law(delta)
        gamma[i] = zeta
        k += zeta
    return (gamma, k)

def embed_message(x, m, gamma):
    y = [0 for _ in range(len(x))]
    j = 0
    for i in range(len(x)):
        if gamma[i] == 1:
            y[i] = m[j]
            j += 1
        else:
            y[i] = x[i]
    return y

def get_message(k):
    m = [0 for _ in range(k)]
    for i in range(k):
        m[i] =  bi_law(0.5)
    return m

def forward(y, a, b):
    n = len(y)
    ll = 0
    qdel = [1-delta, delta]
    alpha = [[0.0 for _ in range(4)] for _ in range(n)]
    ct = [0 for _ in range(n)]
    for s in range(4):
        q = qstate[s]
        alpha[0][s] = 0.5*qdel[q[1]]*b[s][y[0]]
        ct[0] += alpha[0][s]
    ll += math.log(ct[0], 2)
    for s in range(4):
        alpha[0][s] /= ct[0]
    print alpha[0]
    for t in range(1,n):
        ct[t] = 0
        for s in range(4):
            for j in range(4):
                alpha[t][s] += alpha[t-1][j]*a[j][s]
            alpha[t][s] *= b[s][y[t]]
            ct[t] += alpha[t][s]
        for s in range(4):
            alpha[t][s] /= ct[t]
        ll += math.log(ct[t], 2)
    print 'f', ll
    return (alpha, ct, ll)

def backward(y, a, b, ct):
    n = len(y)
    beta = [[0.0 for _ in range(4)] for _ in range(n)]
    for s in range(4):
        beta[n-1][s] = 1.0/ct[n-1]
    for t in range(1,n):
        for s in range(4):
            for j in range(4):
                beta[n-1-t][s] += a[s][j]*beta[n-t][j]*b[j][y[n-t]]
            beta[n-1-t][s] /= ct[n-1-t]
    ll = 0
    qdel = [1-delta, delta]
    for s in range(4):
        q = qstate[s]
        ll += 0.5*qdel[q[1]]*beta[0][s]*b[s][y[0]]
    #print 'b', math.log(ll, 2)
    return beta

def force(y, p, delta, a, b):
    n = len(y)
    n_ =int(math.pow(2,n))
    qdel = [1-delta, delta]
    x = [0 for _ in range(n)]
    g = [0 for _ in range(n)]
    ll = 0
    for x_ in range(n_):
        for i in range(n):
            x[i] = (x_ & (1 << i)) >> i
        for g_ in range(n_):
            for i in range(n):
                g[i] = (g_ & (1 << i)) >> i
            q = x[0]+2*g[0]
            tmp = 0.5*qdel[g[0]]*b[q][y[0]]
            for i in range(1,n):
                q = x[i]+2*g[i]
                q_pr = x[i-1]+2*g[i-1]
                tmp *= b[q][y[i]]*a[q_pr][q]
            ll += tmp
    print 'force', math.log(ll,2)

def a_constr(p, delta):
    a = [[0 for _ in range(4)] for _ in range(4)]
    qdel = [1-delta, delta]
    for i in range(4):
        for j in range(4):
            x1 = i & 1
            q = qstate[j]
            a[i][j] = p[x1][q[0]]*qdel[q[1]]
    return a

def bw_step(y, a, alpha, beta):
    n = len(y)
    xi = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(n-1)]
    for t in range(n-1):
        tmp = 0
        for s1 in range(4):
            for s2 in range(4):
                xi[t][s1][s2] = alpha[t][s1]*a[s1][s2]*b[s2][y[t+1]]*beta[t+1][s2]
                tmp += xi[t][s1][s2]
        for s1 in range(4):
            for s2 in range(4):
                xi[t][s1][s2] /= tmp
        #print 'tmp', tmp
    p_new = [[0, 0],
             [0, 0]
             ]
    delta_new = 0
    xi1 = [[0 for _ in range(4)] for _ in range(n-1)]
    for t in range(n-1):
        for s1 in range(4):
            for s2 in range(4):
                xi1[t][s1] += xi[t][s1][s2]
    xi1_23 = [0 for _ in range(n)]
    for t in range(n-1):
        delta_new += xi1[t][2]+ xi1[t][3]
        xi1_23[t] = 1-xi[t][0][0]
    delta_new /= (n-1)
    tmp1 = 0
    tmp2 = 0
    tmp_eps = 0
    for t in range(n-1):
        tmp1 += xi[t][0][0]+xi[t][0][2]+xi[t][2][0]+xi[t][2][2]
        tmp2 += xi1[t][0]+xi1[t][2]
        tmp_eps += xi[t][0][0]+xi[t][0][2]+xi[t][2][0]+xi[t][2][2]+xi[t][1][1]+xi[t][1][3]+xi[t][3][1]+xi[t][3][3]
        tmp_eps -= xi[t][0][1]+xi[t][0][3]+xi[t][3][0]+xi[t][1][0]+xi[t][1][2]+xi[t][2][3]+xi[t][3][2]+xi[t][2][1]
    p_new[0][0] = tmp1/tmp2
    p_new[0][0] = 0.5+0.5*tmp_eps/(n-1) #
    p_new[0][1] = 1- p_new[0][0]
    tmp1 = 0
    tmp2 = 0
    for t in range(n-1):
        tmp1 += xi[t][1][0]+xi[t][1][2]+xi[t][3][0]+xi[t][3][2]
        tmp2 += xi1[t][1]+xi1[t][3]
    p_new[1][0] = tmp1/tmp2
    p_new[1][1] = 1-p_new[1][0]
    p_new[1][1] = p_new[0][0] #
    p_new[1][0] = 1-p_new[1][1] #
    return (p_new, delta_new, xi1_23)
                
    

if __name__=='__main__':
    qstate = [[0, 0],
              [1, 0],
              [0, 1],
              [1, 1]
              ]
    #b2_k  = pow(2,16)
    b2_k  = pow(2,4)
    print b2_k
    delta = 0.30
    p = [[0.71, 0.29],
         [0.29, 0.71]]
    b = [[1, 0],
         [0, 1],
         [0.5, 0.5],
         [0.5, 0.5]
         ]
    a = a_constr(p, delta)


    for i in range(4):
        print a[i]
                     
    p_hat = [[0,0] for _ in range(2)]
    x = gen_bi_mc(p, b2_k)
    print x

    for i in range(b2_k-1):
        p_hat[x[i]][x[i+1]] += 1
    for i in range(2):
        k = p_hat[i][0]+p_hat[i][1]+0.0
        for j in range(2):
            p_hat[i][j] = p_hat[i][j]/k
    print p_hat

    gamma, k = get_gamma_11(delta,b2_k)
    print (0.0+k)/b2_k
    mes = get_message(k)

    #x = [0,1,0]
    #mes = [1,0]
    #gamma = [1,1,0]

    y = [0 for _ in range(b2_k)]
    y = embed_message(x, mes, gamma)

    #print 'x',x
    #print 'gamma, mes', gamma, mes
    #print 'y', y


    (alpha, ct, __logp) = forward(y, a, b)

    print alpha
    print 'logp', __logp
    #force(y, p, delta, a, b)
    beta = backward(y, a, b, ct)

    #force(y, p, delta, a, b)

    delta_1_s = [0.001, 0.05, 0.10, 0.15, 0.20, 0.25, 0.3, 0.4, 0.5, 0.7, 0.9]
    delta_1_s = [0.27, 0.30, 0.33]
    logp = __logp

    logp_max = -sys.maxint-1
    x1_23_argmax = [0 for _ in range(b2_k)]
    for delta_1 in delta_1_s:
        p_1 = [[0.5, 0.5],
               [0.5, 0.5]
               ]
        s = '%4.2f %4.2f %4.2f %7d %4.2f' % (delta, p[0][0], p[1][0], b2_k, delta_1)
        fou = file('_bw_'+s+'.txt', 'w')
        s1 = s+'%12.3f' % __logp
        fou.write(s1+'\n')
        fou.close()
        for i in range(300):
            fou = file('_bw_'+s+'.txt', 'a')
            a = a_constr(p_1, delta_1)
            logp1 = logp
            (alpha, ct, logp) = forward(y, a, b)
            beta = backward(y, a, b, ct)
            print 'bw', i+1
            print p_1[0]
            print p_1[1]
            print delta_1, '__'
            s1 = '%4d %7.4f %7.4f %7.4f %10.3f \n' % (i+1, delta_1, p_1[0][0], p_1[1][0], logp)
            (p_1, delta_1, x1_23) = bw_step(y, a, alpha, beta)
            fou.write(s1)
            fou.close()
            if abs(logp1-logp) < 0.05:
                if logp_max < logp:
                    print 'log_max < logp'
                    logp_max = logp
                    for j in range(b2_k):
                        x1_23_argmax[j] = x1_23[j]
                break

    fou = file('__key3.txt', 'w')
    for i in range(b2_k):
        s = '%2d  %5.3f \n' % (gamma[i], x1_23_argmax[i])
        fou.write(s)
    fou.close()

            
        

    

