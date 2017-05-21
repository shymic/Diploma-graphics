import time
import random

def get_time(f, tprev):
    res = ''
    tcurr = time.clock()
    dtime = tcurr-tprev
    if f=='s':
        res = '%.2f sec.' % round(dtime,2)
        return res
    res = '%d min. %d sec.' % (dtime/60, round(dtime % 60))
    return res

def bi_law(alpha):
    x = random.random()
    if (x<=alpha):
        result = 1
    else:
        result = 0
    return result

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

def gen_binary_markov_chain(eps, n):
    random.seed()
    ps = [0 for _ in range(2)]
    p = [[0.5*(1+eps),0.5*(1-eps)],[0.5*(1-eps),0.5*(1+eps)]]
    for i in range(2):
        ps[i] = get_ps(p[i])
    x = [0 for _ in range(n)]
    #modeling x
    x[0] = discr_distr([0,0.5,1])
    for i in range(1,n):
        xpr = x[i-1]
        x[i] = discr_distr(ps[xpr])
    return x

def get_message(k):
    m = [0 for _ in range(k)]
    for i in range(k):
        m[i] =  bi_law(0.5)
    return m

def get_gamma_21(delta, n):
    gamma = [0 for _ in range(n)]
    k = 0
    for i in range(n/2):
        zeta = bi_law(delta)
        if zeta == 0:
            gamma[2*i+1] = 0
            gamma[2*i] = 0
        else:
            xi = bi_law(0.5)
            gamma[2*i+1] = xi
            gamma[2*i] = 1-xi
            k += 1
    return (gamma, k)

def get_gamma_11(delta, n):
    gamma = [0 for _ in range(n)]
    k = 0
    for i in range(n):
        zeta = bi_law(delta)
        gamma[i] = zeta
        k += zeta
    return (gamma, k)

def embed_message(x, m, gamma):
    j = 0
    for i in range(len(x)):
        if gamma[i] == 1:
            x[i] = m[j]
            j += 1
    return x

