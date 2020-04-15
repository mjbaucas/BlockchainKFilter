from numpy.random import randn
from sklearn.metrics import mean_squared_error

from math import sqrt
import matplotlib.pyplot as plt

from filters.kalman import KalmanFilter1D
from ble.ble_utils import get_RSSI_and_TX
from localization.tri_utils import get_distance

authorized = ['b8:27:eb:ca:80:6c']

kf = KalmanFilter1D()

if __name__ == "__main__":
    A = 1
    B = 0
    C = 1
    Q = 1e-3
    R = 1e-1

    X = [None]
    t = 10
    Z = []
    P_KF = [Q]
    X_KF = []
        
    k = 0
    d = []
    while k < t:
        rssi, tx_power = get_RSSI_and_TX(1, authorized)
        if rssi != 0:
            Z.append(rssi)
            if k == 0:
                X_KF.append(Z[k]*(1/C))
            else:
                new_X_KF, new_P_KF = kf.filter(X_KF[k-1], Z[k], 0, P_KF[k-1], A, B, C, Q, R)
                X_KF.append(new_X_KF)
                P_KF.append(new_P_KF)
            k+=1
            d.append(get_distance(rssi, C=tx_power))    
            
    rms = sqrt(mean_squared_error(Z, X_KF))
    print(rms)
    
    plt.figure(0)
    plt.plot(Z[:], label="True")
    plt.plot(X_KF[:], label="KF")
    plt.legend()
    plt.ylabel("RSSI (dBm)")
    plt.xlabel("Samples")
    plt.savefig('rssiplot.png')
    
    plt.figure(1)
    plt.plot(d)
    plt.ylabel("Distance (m)")
    plt.xlabel("Samples")
    plt.savefig('dplot.png')
    
    
