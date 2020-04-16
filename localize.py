from localization.tri_utils import pick_anchors, get_distance, get_point_distance, trilateration, plot_on_grid
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
	
	temp_dist = []
	for line in dist_flist[i].readlines():
		line = line.strip('\n')
		line = line.split(' ')
		temp_dist.append(float(line[1]))
	
	cases = min([len(temp_rssi),len(temp_dist)]) 
	cases = 10
	for j in range(40,50):
		if anchor_nomenclature[i] in anchors:
			anchors[anchor_nomenclature[i]].append([temp_rssi[j], temp_dist[j]]) 
		else:
			anchors[anchor_nomenclature[i]] = [[temp_rssi[j], temp_dist[j]]]

# Trilaterate
x_plt = []
y_plt = []
pt_dist = []
w = 3.0
l = 4.0
poi_x = 2
poi_y = 1.5
for i in range(cases):
	temp_anchors = {}
	for j in range(len(anchor_nomenclature)):
		temp_anchors[anchor_nomenclature[j]] = anchors[anchor_nomenclature[j]][i]
	selected = pick_anchors(temp_anchors)

	d = [0, 0, 0]
	for i in range(3):
		d[i] = selected[list(selected)[i]]

	x,y = trilateration(d[0], d[1], d[2], w, l, 0.0)
	new_x, new_y = plot_on_grid(x,y,l,w,list(selected)[0])
	new_d = get_point_distance(poi_x, poi_y, new_x, new_y)
	print('{}, {}, {}'.format(new_x, new_y, new_d))

	x_plt.append(new_x)
	y_plt.append(new_y)
	pt_dist.append(new_d)

print(sum(pt_dist)/len(pt_dist))
plt.figure(0)
plt.xlim(0, 4)
plt.ylim(0, 3)
plt.xlabel("x-axis (m)")
plt.ylabel("y-axis (m)")
plt.scatter(x_plt, y_plt)
plt.scatter(poi_x,poi_y, color='r')
plt.savefig("localize_plot.png")
	
