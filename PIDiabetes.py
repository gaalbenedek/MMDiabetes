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

def PIDControl(i, r, y, y_prev, us, Kp, Ti, Td, Ts):
    e = y-r
    P = Kp*e
    I = i+(Kp*Ts*e)/Ti
    D = (Kp*Td/Ts)*(y-y_prev)
    return (us+P+I+D, I)


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