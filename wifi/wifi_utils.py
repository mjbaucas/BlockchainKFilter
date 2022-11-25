import rssi


def get_RSSI(iteration):
	interface = 'wlan0'
	rssi_scanner = rssi.RSSI_Scan(interface)

	ssids = ['Baucas_Deco']

	rssi_val = 0
	rssi_list = []

	for x in range(0, iteration):
		info = rssi_scanner.getAPinfo(networks=ssids, sudo=True)
		if info != False and len(info) > 0:
			for network in info:
				rssi_list.append(int(network['signal']))

	if len(rssi_list) > 0:
		rssi_val = max(set(rssi_list), key=rssi_list.count)

	return rssi_val
