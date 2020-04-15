from .blescan import hci_le_set_scan_parameters, hci_enable_le_scan, parse_events
import sys
import bluetooth._bluetooth as bluez

# Obtain the RSSI and TX values of each packet
def get_RSSI_and_TX(iterations, authorized):
    # Value containers
    rssi_list = []
    tx_power_list = []
    rssi = 0
    tx_power = 0

    # Open BLE socket
    try:
        sock = bluez.hci_open_dev(0)
        print("Start BLE communication")

    except:
        print("error accessing bluetooth device...")
        sys.exit(1)

    hci_le_set_scan_parameters(sock)
    hci_enable_le_scan(sock)

    # Loop to scan the beacons
    for x in range(iterations):
        returnedList = parse_events(sock, 10)
        for beacon in returnedList:
            details = beacon.split(',')
            #print(details)
            if details[0] in authorized:
                rssi_list.append(details[5])
                tx_power_list.append(details[4])
    
    if len(rssi_list) > 0 or len(tx_power_list) > 0:
        rssi = max(set(rssi_list), key=rssi_list.count)
        tx_power = max(set(tx_power_list), key=tx_power_list.count)
        
    return int(rssi), int(tx_power)        
    
                
    
