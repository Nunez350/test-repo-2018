from matplotlib import pyplot as plt
import numpy as np
import minmaxradiuscircle
import functions

# This demo presents the minimum radius enclosing ball using the specified percent of data and the minimum radius
# enclosing ball of 100% data.
# Input: the starting coordinate and the percent of data points that user wants to include
# Output: One minimum radius enclosing ball that includes all data (red) and one minimum radius enclosing ball that
#         includes specified percent of data (blue)

def onclick(event):
    print(event.xdata, event.ydata)


class MinradCirclebuilder:
    def __init__(self, point):
        self.point = point
        self.xs = list(point.get_xdata())
        self.ys = list(point.get_ydata())
        self.cid = point.figure.canvas.mpl_connect('button_press_event', self)
        #print(self.xs)


    def __call__(self, event):
        #print('click', event)
        if event.inaxes!=self.point.axes: return
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        self.point.set_data(self.xs, self.ys)


        xCoord = np.asarray(self.xs)
        yCoord = np.asarray(self.ys)

        prevXcoord = xCoord[0: len(xCoord) - 1]
        prevYcoord = yCoord[0: len(yCoord) - 1]

        #Find the average points
        #xMean = np.mean(presentPts[:, 0])
        #yMean = np.mean(presentPts[:, 1])
        #xMean = np.mean(xCoord)
        #yMean = np.mean(yCoord)


        #print(type(event.xdata))
        #print(event.ydata)
        #print(type(self.xs))
        #print(self.xs, self.ys)
        #print(self.xs)
        #print(firstPts)


        #coord of present circle
        presentCircle = minmaxradiuscircle.make_circle2(xCoord, yCoord, len(xCoord))

        # coord of previouse circle
        prevCircle = minmaxradiuscircle.make_circle2(prevXcoord, prevYcoord, len(prevXcoord))


        #coord of percent circle
        percentPresentCircle = minmaxradiuscircle.percent_make_circle(xCoord, yCoord, len(xCoord), percent,event.xdata, event.ydata)




        circle1 = plt.Circle((presentCircle[0], presentCircle[1]), presentCircle[2], color='r', linestyle='--', fill=False)
        percentCircle1 = plt.Circle((percentPresentCircle[0], percentPresentCircle[1]), percentPresentCircle[2], color='b', linestyle='--', fill=False)

        centerOfCircle1 = plt.Circle((presentCircle[0], presentCircle[1]), 1, color='r', fill=True)
        centerOfPercentCircle1 = plt.Circle((percentPresentCircle[0], percentPresentCircle[1]), 1, color='b', fill=True)
        #avgPoint = plt.Circle((xMean, yMean), 0.1, color='k', fill=True)


        distPointToCen = functions.distCordwise(event.xdata, event.ydata, presentCircle[0], presentCircle[1])
        percentDistPointToCen = functions.distCordwise(event.xdata, event.ydata, percentPresentCircle[0], percentPresentCircle[1])

        #print(prevCircle[2])
        #print(presentCircle[2])
        #print(distPointToCen)

        if distPointToCen <= prevCircle[2]:
            print("new point ({}, {}) entered, keep minimum radius disk.".format(round(event.xdata,4),round(event.ydata,4)))
        else:
            print("new point ({}, {}) entered, update minimum radius disk.".format(round(event.xdata,4),round(event.ydata,4)))

        '''
        if c2 == 1:
            print("new point entered, update {}% disk.".format(percent))
        else:
            print("new point entered, keep {}% disk.".format(percent))
        '''


        #circle2 = plt.plot([actual[0]], [actual[1]], marker='o', markersize=3, color="red")
        ax.add_artist(circle1)
        ax.add_artist(centerOfCircle1)
        ax.add_artist(percentCircle1)
        ax.add_artist(centerOfPercentCircle1)
        #ax.add_artist(avgPoint)
        self.point.figure.canvas.draw()
        circle1.remove()
        centerOfCircle1.remove()
        percentCircle1.remove()
        centerOfPercentCircle1.remove()
        #avgPoint.remove()
        #canvas.update()


fig = plt.figure(figsize=(7,8))
ax = fig.add_subplot(111)
ax.set_xlim([-100, 100])
ax.set_ylim([-100, 100])
ax.set_title('Click a point to build an Minimum radius enclosing circles')

xflag = 1
yflag = 1
percflag = 1

while xflag == 1:
    try:
        x = float(input("Enter x coordinate between -50 and 50, x: "))
        xflag = 0
    except ValueError:
        print("Please enter a float number.")

while yflag == 1:
    try:
        y = float(input("Enter y coordinate between -50 and 50, y: "))
        yflag = 0
    except ValueError:
        print("Please enter a float number.")

while percflag == 1:
    try:
        percent = float(input("Enter the percentage of data you want to include between 0 and 100: "))
        percflag = 0
    except ValueError:
        print("Please enter a float number.")

point, = ax.plot([x], [y], marker="o", linestyle="")  # first point

minradcirclebuilder = MinradCirclebuilder(point)

plt.show()