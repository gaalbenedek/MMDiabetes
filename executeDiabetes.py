

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
    Kp = 1.4
    Ti=120
    Td=20
    Ts=5
    us=108
    ts,xs = pd.runPIDControl(parm, x0, Kp, Ti, Td, Ts, us)
    plt.plot(ts,xs[:,3])
    
def Problem5(Ku,Tu):
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
    Kp=Ku*0.2
    Ti=Tu*0.5
    Td=Tu*0.2
    Ts=5
    us=108
    N=2000
    ts,xs = pd.runPIDControl(parm, x0, Kp, Ti, Td, Ts, us, N)
    
    plt.plot(ts,xs[:,3])
    plt.title((Kp, Ti, Td))
    
#seq = np.arange(2.3,2.34,0.005)
#for i in seq:
    #plt.figure(np.where(seq==i)[0])
    #Problem5(i)
Problem5(2.32,376)
    