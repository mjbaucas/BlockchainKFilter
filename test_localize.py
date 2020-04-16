from localization.tri_utils import pick_anchors, get_distance, trilateration, plot_on_grid
import matplotlib.pyplot as plt

# Process Data Files
anchor_nomenclature = ["A", "B", "C", "D"]
rssi_flist = [None, None, None,None]
dist_flist = [None, None, None,None]

for i in range(len(anchor_nomenclature)):
	rssi_flist[i] = open("rssi{}.txt".format(anchor_nomenclature[i], "r"))
	dist_flist[i] = open("dist{}.txt".format(anchor_nomenclature[i], "r"))

anchors = {}
cases = 0
for i in range(len(anchor_nomenclature)):
	temp_rssi = []
	for line in rssi_flist[i].readlines():
		line = line.strip('\n')
		line = line.split(' ')
		temp_rssi.append(float(line[1]))
	#print(temp_rssi)
	
	temp_dist = []
	for line in dist_flist[i].readlines():
		line = line.strip('\n')
		line = line.split(' ')
		temp_dist.append(float(line[1]))
	#print(temp_dist)
	
	cases = min([len(temp_rssi),len(temp_dist)]) 
	for j in range(cases):
		if anchor_nomenclature[i] in anchors:
			anchors[anchor_nomenclature[i]].append([temp_rssi[j], temp_dist[j]]) 
		else:
			anchors[anchor_nomenclature[i]] = [[temp_rssi[j], temp_dist[j]]]
	
#print(anchors)
x_plt = []
y_plt = []
for i in range(cases):
	temp_anchors = {}
	for j in range(len(anchor_nomenclature)):
		temp_anchors[anchor_nomenclature[j]] = anchors[anchor_nomenclature[j]][i]
	
	#print(temp_anchors)
	selected = pick_anchors(temp_anchors)
	#print(selected)

	w = 3.0
	l = 4.0

	d = [0, 0, 0]
	for i in range(3):
		d[i] = selected[list(selected)[i]]
		
	#print(d)	
	x,y = trilateration(d[0], d[1], d[2], w, l, 0.0)
	#print('{}, {}'.format(x,y))
	new_x, new_y = plot_on_grid(x,y,l,w,list(selected)[0])
	x_plt.append(new_x)
	y_plt.append(new_y)
	
plt.figure(0)
plt.xlim(0, 4)
plt.ylim(0, 3)
plt.scatter(x_plt, y_plt)
plt.savefig("localize_plot.png")
	
