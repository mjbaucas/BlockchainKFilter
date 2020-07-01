import matplotlib.pyplot as plt 
import numpy as np

wifi_rssi = [0.7, 1.3, 1.78]
xbee_rssi = [0.2, 1.92, 2.34]
ble_rssi = [3.16, 3.57, 4.46]

distance_tick = np.arange(3)
distance_label = [0.25, 0.5, 1.0]

plt.figure(0)
plt.plot(distance_tick, wifi_rssi, label="WiFi")
plt.plot(distance_tick, xbee_rssi, label="XBee")
plt.plot(distance_tick, ble_rssi, label="BLE")
plt.legend()
plt.xticks(distance_tick, distance_label)
plt.ylabel("RSSI (dB)")
plt.xlabel("Distance (m)")
plt.savefig('rmseplotrssi.png')