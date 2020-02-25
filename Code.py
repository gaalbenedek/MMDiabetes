# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 09:31:34 2020

@author: carl
"""
import numpy as np
import scipy
import scipy.integrate
from matplotlib import pyplot as plt

#Problem 1 
#x[0] = Isc
#x[1] = Ip
#x[2] = Ieff
#x[3] = G
#x[4] = D1
#x[5] = D2
def MVPModel(x,t,parm,u,d):
    xp = [
            u/(parm["tau1"]*parm["C1"]) - x[0]/parm["tau1"], #I sc prime
            (x[0]-x[1])/parm["tau2"], #I p prime
            -parm["p2"]*x[2] +parm["p2"]*parm["SI"]*x[1], #I eff prime, TODO: FIND OUT WHAT SI IS
            -(parm["GEZI"] + x[2])*x[3] + parm["EGP0"] + 1000*x[5]/(parm["VG"]*parm["taum"]), #G prime
            d-x[4]/parm["taum"],
            (x[4]-x[5])/parm["taum"]
        ];
    return xp

#Problem 2
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
    xs = scipy.integrate.odeint(MVPModel, [0,0,0,0,0,0], t=np.linspace(0,5000,50000), args=(parm, u, d))
    
    plt.plot(np.linspace(0,5000,50000),xs[:,3])

#Problem 3

def PIDControl(i, r, y, y_prev, us, Kp, Ti, Td, Ts):
    e = y-r
    P = Kp*e
    I = i+(Kp*Ts*e)/Ti
    D = (Kp*Td/Ts)*(y-y_prev)
    return (us+P+I+D, I)

#Problem 4
def runPIDControl(parm,x0,Kp,Ti,Td,Ts,us):
    I=0
    t=0
    ts = []
    ts += [t]
    x=x0
    xs = []+[x]
    y_prev=x[3]
    r = 108
    us = 108 #What is insulin steady state?
    d=0
    for loop in range(0,500):
        u, I = PIDControl(I,r,x[3],y_prev, us, Kp,Ti,Td,Ts)
        y_prev = x[3]
        if u<0:
            u=0
        xnext = scipy.integrate.odeint(MVPModel,x, t=np.linspace(0,Ts,10),args=(parm,u,d))
        t = t+Ts
        x = xnext[-1,:]
        xs += [x]
        ts += [t]
    return (np.array(ts),np.array(xs))

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
    Kp = 0.3
    Ti=300
    Td=15
    Ts=5
    us=108
    ts,xs = runPIDControl(parm, x0, Kp, Ti, Td, Ts, us)
    plt.plot(ts,xs[:,3])