import socket  
import sys

from utils import send_msg, recv_msg
from blockchain.private_blockchain import Chain as PrivateBlockchain
from filters.kalman import KalmanFilter1D
 
host_ip = sys.argv[1]  
port = int(sys.argv[2])

print('host ip: ', host_ip)# Should be displayed as: 127.0.1.1  

# Initialize Blockchain
trusted_list = [
    "local1c", "local2c", "local3c", "local4c"
]

pchain = PrivateBlockchain()
pchain.gen_next_block("0", trusted_list)

# Initialize Data Queue 
data_queue = {
}

for filter_number in trusted_list:
    data_queue[filter_number] = {"X":None, "P":None, "sent": False}


# Initialize Kalman Filter
kf = KalmanFilter1D()

# Filter Parameters
A = 1
B = 0
C = 1
Q = 1e-3
R = 1e-2

X = [None]
t = 100
Z = []
P_M = [Q]
X_M = [0]

k = 1
D = []
D_KF = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
s.bind((host_ip, port))  
s.listen(10)  

trustee_index = 0
while True:  
    data = "none"
    conn, addr = s.accept()  
    print('Connected by', addr)  
    data = recv_msg(conn)
    if not data: 
        break
    message = data.decode().split("_")
    if message[0] in pchain.output_ledger() and trusted_list[trustee_index] == message[0]:
        new_X_M, new_P_M = kf._predict(X_M[k-1], 0, P_M[k-1], A, B, Q)
        inv_new_P_M = 1/new_P_M
        inv_P_K = 1/float(message[1])

        if data_queue[message[0]]["sent"] == False:
            if data_queue[message[0]]["P"] == None:
                data_queue[message[0]]["P"] = inv_P_K
            
            if data_queue[message[0]]["X"] == None:
                data_queue[message[0]]["X"] = float(message[2])

        trust_counter = 0
        for trustee in trusted_list:
            if data_queue[trustee]["X"] != None and data_queue[trustee]["P"] != None:
                trust_counter+=1
        
        # Calculate the final P and X
        sum_inv_P_K = 0
        sum_inv_P_X = 0
        if trust_counter == len(trusted_list):
            for trustee in trusted_list:
                sum_inv_P_K += data_queue[trustee]["P"]
                sum_inv_P_X += data_queue[trustee]["P"] * data_queue[trustee]["X"]
                
            inv_P_F_K = sum_inv_P_K + inv_new_P_M
            P_F_K = 1/inv_P_F_K
            X_F_K = P_F_K*(inv_new_P_M*new_X_M + sum_inv_P_X)

            P_M.append(P_F_K)
            X_M.append(X_F_K)
            k+=1

            data = str(P_F_K) + "_" + str(X_F_K) 
            data_queue[message[0]]["sent"] = True
        else:
            data = "none"

        # Check if valeu has been sent to local filter
        sent_counter = 0
        for trustee in trusted_list:
            if data_queue[trustee]["sent"] == True:
                sent_counter+=1
        if sent_counter == len(trusted_list):
            for trustee in trusted_list:
                data_queue[trustee]["P"] = None
                data_queue[trustee]["X"] = None
                data_queue[trustee]["sent"] = False

        trustee_index+=1
        if trustee_index > len(trusted_list) - 1:
            trustee_index = 0
    else:
        data = "none"
    
    
    send_msg(conn, str.encode(data))# Send back the received data intact
    print('Received', repr(data))  
    conn.close()