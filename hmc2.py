#(1,1) model, HMC(2)

import sys
import math
import random
import hm
import numpy as np

def a_constr(p, delta):
    a = [[[0 for _ in range(4)] for _ in range(4)]for _ in range(4)]
    qdel = [1-delta, delta]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                    x1 = i & 1
                    y1 = j & 1
                    q = qstate[k]
                    a[i][j][k] = p[x1][y1][q[0]]*pow(qdel[q[1]],q[1])*pow(qdel[q[0]], 1-q[1])
    return a

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

def get_ps(p):
    n = len(p)
    ps = [0 for _ in range(n+1)]
    for i in range(n):
        ps[i+1] = ps[i]+p[i]
    return ps

def gen_bi_mc(p, n):
    random.seed()
    ps = [[0 for _ in range(2)] for _ in range(2)]
    for i in range(2):
        for j in range(2):
            ps[i][j] = get_ps(p[i][j])
    x = [0 for _ in range(n)]
    #modeling x
    x[0] = discr_distr([0,0.5,1])
    x[1] = discr_distr([0,0.5,1])
    for i in range(2,n):
        xpr1 = x[i-2]
        xpr2 = x[i-1]
        x[i] = discr_distr(ps[xpr1][xpr2])
    return x

def bi_law(alpha):
    x = random.random()
    if (x<=alpha):
        result = 1
    else:
        result = 0
    return result


def get_gamma_11(delta, n):
    gamma = [0 for _ in range(n)]
    k = 0
    for i in range(n):
        zeta = bi_law(delta)
        gamma[i] = zeta
        k += zeta
    return (gamma, k)

def get_message(k):
    m = [0 for _ in range(k)]
    for i in range(k):
        m[i] =  bi_law(0.5)
    return m

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


def forward(y, a, b):
    n = len(y)
    ll = 0
    qdel = [1-delta, delta]
    alpha = [[[0.0 for _ in range(4)] for _ in range(4)] for _ in range(n)]
    ct = [0 for _ in range(n)]
    for s in range(4):
        q = qstate[s]
        alpha[0][0][s] = 0.5*qdel[q[1]]*b[s][y[0]]
        pi=0
        for s0 in range(4):
            q0 = qstate[s0]
            pi += 0.25 * pow( delta, q0[0]+q[0])* pow(1-delta, 2-q0[0]-q[0])
            alpha[1][s][s0] = alpha[0][0][s]*b[s][y[1]]*0.25 * pow( delta, q0[0]+q[0])* pow(1-delta, 2-q0[0]-q[0])/pi
        ct[0] += alpha[0][0][s]
        ct[1] += alpha[0][1][s]
    ll += math.log(ct[0], 2)
    ll += math.log(ct[0], 2)

    for s in range(4):
        alpha[0][0][s] /= ct[0]
        alpha[0][1][s] /= ct[1]
    #print alpha[0]

    for t in range(1,n):
        ct[t] = 0
        for s in range(4):
            for s0 in range(4):
                for j in range(4):
                    alpha[t][s][s0] += alpha[t-1][s][j]*a[j][s][s0]
                alpha[t][s][s0] *= b[s][y[t]]
                ct[t] += alpha[t][s][s0]

        for s in range(4):
            for s0 in range(4):
                alpha[t][s][s0] /= ct[t]
        ll += math.log(ct[t], 2)
    print 'f', ll
    return (alpha, ct, ll)

def backward(y, a, b, ct):
    n = len(y)
    beta = [[[0.0 for _ in range(4)] for _ in range(4)] for _ in range(n)]
    for s in range(4):
        for s0 in range(4):
            beta[n-1][s][s0] = 1.0#/ct[n-1]
    for t in range(1,n):
        for s in range(4):
            for s0 in range(4):
                for j in range(4):
                    beta[n-1-t][s][s0] += a[s][s0][j]*beta[n-t][s0][j]*b[j][y[n-t]]
                #beta[n-1-t][s][s0] /= ct[n-1-t]
    ll = 0
    qdel = [1-delta, delta]
    for s in range(4):
        q = qstate[s]
        for s0 in range(4):
            q0 = qstate[s0]
            ll += 0.5*qdel[q[1]]*beta[0][s][s0]*b[s][y[0]]
    print 'b', math.log(ll, 2)
    return beta


if __name__=='__main__':
    qstate = [[0, 0],
              [1, 0],
              [0, 1],
              [1, 1]
              ]
#    n = pow(2, 16)
    n = pow(2, 4)
    delta = 0.30
    p = [[[0.71, 0.29], [0.29, 0.71]],
         [[0.71, 0.29], [0.29, 0.71]]]

    b = [[1, 0],
         [0, 1],
         [0.5, 0.5],
         [0.5, 0.5]
         ]

    a = a_constr(p, delta)
    for i in range(4):
        for j in range(4):
            print a[i][j]


    p_hat = [[0,0] for _ in range(2)]
    x = gen_bi_mc(p, n)
    print x

    gamma, k = get_gamma_11(delta,n)
    print (0.0+k)/n
    mes = get_message(k)

    y = [0 for _ in range(n)]
    y = embed_message(x, mes, gamma)

    print gamma
    print y

    (alpha, ct, __logp) = forward(y, a, b)

    print alpha
    print 'logp', __logp

    beta = backward(y, a, b, ct)

    print beta


