# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 09:57:06 2020

@author: Carl
"""

import numpy as np
import scipy
import scipy.integrate
from matplotlib import pyplot as plt
import PIDiabetes as pd


#Problem 6
def rho(G):
    return 1/2*(G-108)**2 + 1000000/2*np.max([70-G, 0])**2
    
def phi(x0, u0, d0, parm):
    #Do first five minutes with meal intake and bolus size
    u1 = u0/5
    d1 = d0/5
    #the first ten steps are individually half a minute long
    xs1 = scipy.integrate.odeint(pd.MVPModel, x0, np.linspace(0,5,10), args=(parm, u1, d1))
    #print(xs1[-1,:])
    #Then do rest without
    #One minute per step.
    ts = np.linspace(5,1000,1000-5) #Every minute, excluding the first five.
    xs = scipy.integrate.odeint(pd.MVPModel, xs1[-1,:], ts, args=(parm, 25.04, 0))
    
    phi = 0;
    for G in xs1[:,3]:
        phi += 1/2*rho(G)
        if(G < 70):
            print(rho(G))
    for G in xs[:,3]:
        phi += rho(G)
    #DEBUG PLOTS
    totalTs = np.concatenate((np.array(np.linspace(0,5,10)),np.array(ts)))
    totalXs = np.concatenate((xs1[:,3], xs[:,3]))
    plt.plot(totalTs,totalXs)
    return phi

#Problem 7
def findOptimalU(x0, d0, parm):
    phis = []
    
    
    #Do u estimates
    precision = 5000
    minU = 10000
    
    for loop in range(0,15):
        phis = []
        Us = [(i)*precision+minU for i in range(-1,2)]
        for U in Us:
            phis += [phi(x0,U,d0,parm)]
        
        #plt.ylabel("phi")
        #plt.xlabel("bolus [mU]")
        #plt.plot(Us,phis)
        #plt.show()
    
        #Then, do finer estimate of minimum
        minU = Us[np.argmin(phis)]
        
        precision /= 2
    
    #Then, this is the best U
    optimalU = minU
        
    plt.ylabel("Blood glucose")
    plt.xlabel("Time [min]")
    plt.title("Bolus guesses, d0=" + str(d0) + "g carbs")
    plt.savefig("bolusguess"+str(d0)+".svg", format="svg")
    plt.show()
    plt.ylabel("phi")
    plt.xlabel("bolus [mU]")
    plt.title("Bolus size vs carbs in meal")
    plt.plot(Us,phis)
    plt.show()
    
    return optimalU

#Problem 8
#Returns d0s, optimalUs which is an array of carbohydrate meal sizes and insulin infusions
def Problem8(stepSize):
    
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
    x0 = [1.2458,1.2458,0.0101,108.2115,0,0]
    
    d0s = np.arange(70,200,stepSize)
    optimalUs = []
    for d0 in d0s:
        optimalUs += [findOptimalU(x0, d0, parm)]
    
    plt.plot(d0s,optimalUs, 'o')
    plt.xlabel("Meal size [g carbs]")
    plt.ylabel("Bolus [mU]")
    plt.show()
    return (d0s,optimalUs)

def Problem9():
    d0s, optimalUs = Problem8(5)
    c = np.polyfit(d0s, optimalUs, 2)
    
    
    ds = np.linspace(60,200,300);
    p = np.poly1d(c)
    fitPoly = p(ds)
    
    plt.plot(ds,fitPoly)
    plt.plot(d0s,optimalUs, 'o')
    plt.ylabel("Bolus [mU]")
    plt.xlabel("Carbs in meal [g]")
    plt.savefig("bolusplot.svg", format="svg")
    plt.show()
    