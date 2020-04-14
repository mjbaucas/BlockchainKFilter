from numpy import array, eye, diag, zeros, arange, ndarray, dot, empty, append, nan_to_num
from numpy.linalg import norm
from numpy.random import multivariate_normal, randn

from math import sqrt
import matplotlib.pyplot as plt

from filters.kalman import KalmanFilter1D
from ble.ble_utils import getRSSIandTX

if __name__ == "__main__":
    T = 1e-3
    t = list(arange(0, 1, T))
    A = 1
    B = 0
    C = 1
    Q = 1e-3
    R = 1e-2

    X = [0]*len(t)
    Z = randn(len(t))
    for i in range(len(Z)):
        if i >= len(t)/8:
            Z[i]+=67
        if i >= (len(t)/8)*2:
            Z[i]-=67
        if i >= len(t)/2:
            Z[i]+=120
        if i >= (len(t)/4)*3:
            Z[i]-=100

    U = randn(len(t))
    P_KF = [0]*len(t)
    X_KF = [0]*len(t)

    X[0] = None
    P_KF[0] = Q
    A_KF = 1

    kf = KalmanFilter1D()
    
    for k in range(10):
        getRSSIandTX(10)

    #for k in range(1, len(t)-1):
        #if X[k] == None:
        #    X_KF[k+1] = Z[k]*(1/C)
        #else:
        #    X_KF[k+1], P_KF[k+1] = kf.filter(X_KF[k], Z[k], U[k], P_KF[k], A_KF, B, C, Q, R)

    plt.plot(t, Z[:])
    plt.plot(t, X_KF[:])
    plt.savefig('test4.png')
