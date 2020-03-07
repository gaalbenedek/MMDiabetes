

import numpy as np
import scipy
import scipy.integrate
from matplotlib import pyplot as plt
import PIDiabetes as pd


#Problem 1 
#x[0] = Isc
#x[1] = Ip
#x[2] = Ieff
#x[3] = G
#x[4] = D1
#x[5] = D2



def Problem2():
    parm = {
        "tau1":49,
        "tau2":47,
        "C1":20.1,
        "p2":0.0106,
        "SI":0.0081,
        "GEZI":0.0022,
        "EGP0":1.33,
        "VG":253,
        "taum":47
    }
    u = 25.04
    d = 0
    xs = scipy.integrate.odeint(pd.MVPModel, [0,0,0,0,0,0], t=np.linspace(0,5000,50000), args=(parm, u, d))
    
    plt.plot(np.linspace(0,5000,50000),xs[:,3])



def Problem4():
    parm = {
        "tau1":49,
        "tau2":47,
        "C1":20.1,
        "p2":0.0106,
        "SI":0.0081,
        "GEZI":0.0022,
        "EGP0":1.33,
        "VG":253,
        "taum":47
    }
    x0 = np.array([1.2458,1.2458,0.0101,200,0,0])

    Kp = 0.2
    Ti=800
    Td=15
    Ts=5
    us=25.04
    ts,xs = pd.runPIDControl(parm, x0, Kp, Ti, Td, Ts, us)
    plt.plot(ts,xs[:,3])
    plt.title('Min: {}'.format(np.amin(xs[:,3])))
    
def Problem5():
    parm = {
        "tau1":49,
        "tau2":47,
        "C1":20.1,
        "p2":0.0106,
        "SI":0.0081,
        "GEZI":0.0022,
        "EGP0":1.33,
        "VG":253,
        "taum":47
    }
    x0 = np.array([1.2458,1.2458,0.0101,200,0,0])
    
    N=1000
    d=np.zeros(N)
    #Sugar intake tests
    d[200]=10
    d[250]=15
    
    noiseSD = 2
    
    Kp=0.1
    Ti=800
    Td=20
    Ts=5
    us=25.04
    
    ts,xs = pd.runPIDControl(parm, x0, Kp, Ti, Td, Ts, us, N, d, noiseSD)
    
    plt.plot(ts,xs[:,3],label='d(200) = {}, Min: {} \nd(250) = {}'.format(d[200],round(np.amin(xs[:,3]),2),d[250]))
    plt.title('Blood glucose level under PID control')
    plt.xlabel('Time [s]')
    plt.ylabel('Blood glucose [mg/dL]')
    plt.legend()

Problem5()
    