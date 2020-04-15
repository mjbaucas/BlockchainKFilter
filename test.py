from localization.tri_utils import pick_anchors, get_distance, trilateration, plot_on_grid

anchors = {
	'A':-67,
	'B':-81,
	'C':-42,
	'D':67	
}


selected = pick_anchors(anchors)
print(selected)

w = 3.0
l = 4.0

d = [0, 0, 0]
for i in range(3):
	d[i] = get_distance(selected[list(selected)[i]])
	
print(d)	
x,y = trilateration(d[0], d[1], d[2], w, l, 0.0)
print('{}, {}'.format(x,y))
print(plot_on_grid(x,y,l,w,list(selected)[0]))
