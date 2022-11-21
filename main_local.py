from numpy.random import randn
from sklearn.metrics import mean_squared_error
from math import sqrt
import matplotlib.pyplot as plt

from filters.kalman import KalmanFilter1D
from localization.tri_utils import get_distance
from wifi.wifi_utils import get_RSSI
import hashlib
from blockchain.private_blockchain import Chain

import sys

local_number = sys.argv[1]

# Initialize Private Blockchain
authorized = sys.argv[2] # Change this to hash or read from encrypted file
ledger = Chain()
ledger.gen_next_block(hashlib.sha256("AddressBlock0".encode()).digest(), authorized)

# Initialize Kalman Filter
kf = KalmanFilter1D()

if __name__ == "__main__":
    # Write to files
    rssi_file = open("rssiLocal" + local_number + ".txt", "a")
    dist_file = open("distLocal" + local_number + ".txt", "a")

    # Filter Parameters
    A = 1
    B = 0
    C = 1
    Q = 1e-3
    R = 1e-2

    Beta = 0.5

    X = [None]
    t = 100
    Z = []
    P_KF = [Q]
    X_KF = []
    
    # Apply Filter
    k = 0
    D = []
    D_KF = []
    while k < t:
        rssi = get_RSSI(5)
        if rssi != 0:
            Z.append(rssi)
            D.append(get_distance(rssi, C=-45, N=2))   
            if k == 0:
                X_KF.append(Z[k]*(1/C))
            else:
                new_X_KF, new_P_KF = kf.filter(X_KF[k-1], Z[k], 0, P_KF[k-1], A, B, C, Q, R)
                # Send to Global Filter
                # Recieve Values
                Q = Q/Beta
                new_P_KF = new_P_KF/Beta
                X_KF.append(new_X_KF)
                P_KF.append(new_P_KF)
            D_KF.append(get_distance(X_KF[k], C=-45, N=2))  
            
            # Debugging prints
            print(D[k])
            print(D_KF[k])
            
            rssi_file.write("{} {}\n".format(Z[k], X_KF[k]))
            dist_file.write("{} {}\n".format(D[k], D_KF[k]))
            k+=1

    # RMSE     
    rms = sqrt(mean_squared_error(Z, X_KF))
    rms_d = sqrt(mean_squared_error(D, D_KF))
    print(rms)
    print(rms_d)
    
    # Plot RSSI
    plt.figure(0)
    plt.plot(Z[:], label="True")
    plt.plot(X_KF[:], label="KF")
    plt.legend()
    plt.ylabel("RSSI (dB)")
    plt.xlabel("Samples")
    plt.savefig("rssiplotLocal" + local_number + ".png")
    
    # Plot Distance
    plt.figure(1)
    plt.plot(D, label="True")
    plt.plot(D_KF, label="KF")
    plt.legend()
    plt.ylabel("Distance (m)")
    plt.xlabel("Samples")
    plt.savefig("rssiplotLocal" + local_number + ".png")
    
    # Clean up
    rssi_file.close()
    dist_file.close()
