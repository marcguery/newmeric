import matplotlib.pyplot as plt
import numpy as np
import time
import math
import easygui

class Numer(object):
	"""
	Matplotlib heatmap in which a number can be drawn.
	"""
	def __init__(self, x=100, y=100, size=3):
		"""
		Initialize the object with number of x cells, y cells and size of the line.
		"""
		try:
			assert size in range(1, 6)
			assert x in range(10, 501)
			assert y in range(10, 501)
		except AssertionError:
			print("x and y must be between 10 and 500. Input is x : %s, y : %s." % (x, y))
			print("Size must be between 1 and 5. Input is %s." % (size))
			raise
		self.ranx=x
		self.rany=y
		self.size=size
		self.coords=np.zeros((self.ranx, self.rany))
		self.nice_trick_bro()
		self.fig, self.ax = plt.subplots()
		self.heatmap = plt.imshow(self.coords, cmap='gray')
		self.fig.tight_layout()
		plt.axis('off')
	
	def nice_trick_bro(self):
		self.coords[0][0]=1.1
		self.coords[0][self.rany-1]=1.1
		self.coords[self.ranx-1][0]=1.1
		self.coords[self.ranx-1][self.rany-1]=1.1
	
	def reset_coords(self):
		self.coords=np.zeros((self.ranx, self.rany))
		self.nice_trick_bro()

	def save_draw(self, file="draws.csv", foot="#"):
		with open(file, "a") as fdraw:
			np.savetxt(fdraw, self.coords, delimiter=",", footer=foot)
		fdraw.close
	
	def update_data(self, event):
		xmou = int(event.ydata)
		ymou = int(event.xdata)
		if self.coords[xmou][ymou]>0.8:
			return
		interx=max(int(self.ranx // (1/self.size*100) + 1), 2)
		intery=max(int(self.rany // (1/self.size*100) + 1), 2)
		maxx=min(xmou+interx-1, self.ranx)
		minx=max(xmou-interx+1, 0)
		maxy=min(ymou+intery-1, self.rany)
		miny=max(ymou-intery+1, 0)
		for xare in range(minx, maxx+1):
			normx = (maxx-xmou) - math.fabs(xare-xmou)
			valx = normx/(maxx-xmou)
			for yare in range(miny, maxy+1):
				normy = (maxy-ymou) - math.fabs(yare-ymou)
				valy = normy/(maxy-ymou)
				self.coords[xare][yare]=min(self.coords[xare][yare]+(valx+valy)/3, 1)

	def hover(self, event):
		if event.inaxes == self.ax:
			cont = self.heatmap.contains(event)
			if cont:
				self.update_data(event)
				self.heatmap.set_data(self.coords)
				self.fig.canvas.draw_idle()

	def key(self, event):
		cid = self.fig.canvas.mpl_connect("motion_notify_event", self.hover)
		if event.key!='control':
			self.fig.canvas.mpl_disconnect(cid)

	def button(self, event):
		cid = self.fig.canvas.mpl_connect("motion_notify_event", self.hover)
		self.fig.canvas.mpl_disconnect(cid)
		if easygui.ccbox("Do you want to save your draw ?", title="Newmeric is waiting for you..."):
			num=easygui.integerbox(msg='Which number did you draw ?', title='Newmeric is waiting for you...', 
			default=0, lowerbound=0, upperbound=9)
			filename="draws"+str(num)+".csv"
			self.save_draw(filename)
			print("Your draw has been saved in %s !" % filename)
		else:
			print("nonencor")
		self.reset_coords()
		self.heatmap.set_data(self.coords)
		self.fig.canvas.draw_idle()
	
	def draw(self):
		"""
		Activate the drawing process
		"""
		self.fig.canvas.mpl_connect("key_press_event", self.key)
		self.fig.canvas.mpl_connect('button_press_event', self.button)
		plt.show()
