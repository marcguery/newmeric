#!/usr/bin/python3
import matplotlib.pyplot as plt
import numpy as np
import time
import math

ranx = int(100)
rany = int(100)
a = np.zeros((ranx,rany))
a[0][0]=1
fig,ax = plt.subplots()
heat = plt.imshow(a, cmap='gray')

def update_data(event, mat):
	xmou = int(event.xdata)
	ymou = int(event.ydata)
	if mat[ymou][xmou]>0.8:
		return mat
	interx=int(ranx/25)
	intery=int(rany/25)
	maxx=min(xmou+interx, ranx)
	minx=max(xmou-interx, 0)
	maxy=min(ymou+intery, rany)
	miny=max(ymou-intery, 0)
	for yare in range(miny, maxy):
		normy = (maxy-ymou) - math.fabs(yare-ymou)
		valy = normy/(maxy-ymou)
		for xare in range(minx, maxx):
			normx = (maxx-xmou) - math.fabs(xare-xmou)
			valx = normx/(maxx-xmou)
			mat[yare][xare]=min(mat[yare][xare]+(valx+valy)/2, 1)
	return mat
def hover(event):
	mat = a
	if event.inaxes == ax:
		cont = heat.contains(event)
		if cont:
			newmat = update_data(event, mat)
			heat.set_data(newmat)
			fig.canvas.draw_idle()

def key(event):
	cid = fig.canvas.mpl_connect("motion_notify_event", hover)
	if event.key!='control':
		fig.canvas.mpl_disconnect(cid)

def button(event):
	global a #pas bien
	a = np.zeros((ranx,rany))
	a[0][0]=1
	heat.set_data(a)
	fig.canvas.draw_idle()

fig.canvas.mpl_connect("key_press_event", key)
fig.canvas.mpl_connect('button_press_event', button)


plt.show()