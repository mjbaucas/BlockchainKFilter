from xbee import ZigBee
import serial
from time import sleep

def get_RSSI(iteration):
    comm = serial.Serial('/dev/ttyUSB0', 9600)
    xbee_conn = ZigBee(comm)
    
    rssi = 0
    
    rssi_list = []
    counter = 0
    while counter < iteration:
        try:
            packet = xbee_conn.wait_read_frame()
            xbee_conn.at(command=b'DB')
            if 'parameter' in packet:
                rssi_list.append(packet['parameter'][0])
                counter += 1
            sleep(0.1)
        except KeyboardInterrupt:
            break
    comm.close()
    
    if len(rssi_list) > 0:
        rssi = max(set(rssi_list), key=rssi_list.count)
    
    print(rssi)
    return int(rssi)
