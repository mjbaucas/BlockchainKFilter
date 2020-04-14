from .blescan import hci_le_set_scan_parameters, hci_enable_le_scan, parse_events
import sys
import bluetooth._bluetooth as bluez

# Obtain the RSSI and TX values of each packet
def getRSSIandTX(iterations):
    # Value containers
    values = {}

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
            print(details)