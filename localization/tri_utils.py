from math import sqrt

def get_distance(rssi, C=-67, N=2.0):
	return 10.0 ** ((C - rssi)/(10.0 * N))

def pick_anchors(anchors):
	points = sorted(anchors, key=lambda dict_key: abs(anchors[dict_key][0]))
	points = points[:3]
	
	selected_anchors = {}
	for i in range(3):
		selected_anchors[points[i]] = float(anchors[points[i]][1])
	
	sorted_anchors = {}
	if 'A' not in selected_anchors.keys():
		sorted_anchors['C'] = selected_anchors['C']
		sorted_anchors['B'] = selected_anchors['B']
		sorted_anchors['D'] = selected_anchors['D']
	elif 'B' not in selected_anchors.keys():
		sorted_anchors['D'] = selected_anchors['D']
		sorted_anchors['A'] = selected_anchors['A']
		sorted_anchors['C'] = selected_anchors['C']
	elif 'C' not in selected_anchors.keys():
		sorted_anchors['A'] = selected_anchors['A']
		sorted_anchors['B'] = selected_anchors['B']
		sorted_anchors['D'] = selected_anchors['D']
	else:
		sorted_anchors['B'] = selected_anchors['B']
		sorted_anchors['C'] = selected_anchors['C']
		sorted_anchors['A'] = selected_anchors['A']
	
	return sorted_anchors
	
def trilateration(d1, d2, d3, r, s, t):
	x = (d1**2 - d2**2 + r**2)/(2.0*r)
	y = sqrt(abs(d3**2 - (x-s)**2)) + t
	return x, y
	
def plot_on_grid(x, y, l, w, ref):
	if ref == 'A':
		return x,y
	elif ref == 'B':
		return y,w-x 
	elif ref == 'C':
		return l-x,w-y
	else:
		return l-y,x

def get_point_distance(x1,y1,x2,y2):
	return sqrt((x2-x1)**2 + (y2-y1)**2)
