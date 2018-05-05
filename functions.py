import numpy as np
import math
import matplotlib.pyplot as plt
import minmaxradiuscircle
from operator import itemgetter

def generate_one_traj(length, delMux, delSigx, xStartPoint, xEndPoint,  delMuy, delSigy,yStartPoint, yEndPoint):
    #xStartPoint = 0
    #xStartPoint = 30
    #yStartPoint = 0
    #yEndPoint = 0.2

    delx = np.random.normal(delMux, delSigx, length);
    tempx = np.linspace(xStartPoint, xEndPoint, length);
    x = tempx + delx;


    dely = np.random.normal(delMuy, delSigy, length);
    #dely = np.random.uniform(delMuy, delSigy, length);
    tempy = np.linspace(yStartPoint, yEndPoint, length);
    y = tempy + dely;

    return x, y

def multiple_traj(numData, xTraj, yTraj, delSigx, delSigy):
    #delSigx = 0.3
    #delSigy = 0.3
    length = len(xTraj)

    tData = np.linspace(0, 1000, length)
    xData = np.zeros((numData, length))
    yData = np.zeros((numData, length))

    for a in range(numData):
        for b in range(length):
            if a == 0:
                xData[0][b] = xTraj[b]
                yData[0][b] = yTraj[b]
            else:
                xData[a][b] = xData[0][b] + np.random.normal(0, delSigx)
                yData[a][b] = yData[0][b] + np.random.normal(0, delSigy)

    return xData, yData, tData

def average_traj(xData, yData):

    numData = xData.shape[0]
    length = xData.shape[1]

    xAverTraj = np.zeros(length)
    yAverTraj = np.zeros(length)

    for a in range(length):
        xAverTraj[a] = np.mean(xData[:, a])
        yAverTraj[a] = np.mean(yData[:, a])
    return xAverTraj, yAverTraj


def minmax_Traj(xData, yData):
    
    numData = xData.shape[0]
    length = xData.shape[1]

    xMinmaxTraj = np.zeros(length)
    yMinmaxTraj = np.zeros(length)

    for a in range(length):
        c = minmaxradiuscircle.make_circle2(xData[:, a], yData[:, a], numData)
        xMinmaxTraj[a] = c[0]
        yMinmaxTraj[a] = c[1]

    return xMinmaxTraj, yMinmaxTraj

def mean_squre_error(orgDatax, orgDatay, estDatax, estDatay):
    length = len(orgDatax)
    squareDst = np.zeros(length)
    for a in range(length):
        squareDst[a] =  math.sqrt(math.pow(orgDatax[a] - estDatax[a], 2) + math.pow(orgDatay[a] - estDatay[a], 2))

    return np.mean(squareDst)

def max_dist_error(orgDatax, orgDatay, estDatax, estDatay):
    length = len(orgDatax)
    squareDst = np.zeros(length)
    for a in range(length):
        squareDst[a] = math.sqrt(math.pow(orgDatax[a] - estDatax[a], 2) + math.pow(orgDatay[a] - estDatay[a], 2))

    return np.max(squareDst)

def dist(x,y):
    return math.sqrt(math.pow(x[0] - y[0], 2) + math.pow(x[1] - y[1], 2))

def distCordwise(x0, x1, y0, y1):
    return math.sqrt(math.pow(x0 - y0, 2) + math.pow(x1 - y1, 2))

#Compute square-root sum distance of one point to all points
def sqrt_sum_dist(x, y, xCoord, yCoord):
    sum = 0
    for a in range(len(xCoord)):
        sum += distCordwise(x,y, xCoord[a], yCoord[a])

    return sum

def percent_minmax_Traj(xData, yData, percent):
    numData = xData.shape[0]
    length = xData.shape[1]

    validNumData = round(numData * (percent / 100.0))

    xPercMinmaxTraj = np.zeros(length)
    yPercMinmaxTraj = np.zeros(length)

    for a in range(length):
        fixedTimeData = np.zeros((numData, 3))

        for b in range(numData):
            fixedTimeData[b][0] = xData[b][a]
            fixedTimeData[b][1] = yData[b][a]
            fixedTimeData[b][2] = sqrt_sum_dist(fixedTimeData[b][0], fixedTimeData[b][1], xData[:, a], yData[:,a])

        listFixedTimeData = fixedTimeData.tolist()
        sortedlistFixedTimeData = sorted(listFixedTimeData, key=itemgetter(2))
        newfixedTimeData = np.asarray(sortedlistFixedTimeData)

        c = minmaxradiuscircle.make_circle2(newfixedTimeData[0:validNumData, 0], newfixedTimeData[0:validNumData, 1], validNumData)
        xPercMinmaxTraj[a] = c[0]
        yPercMinmaxTraj[a] = c[1]

    return xPercMinmaxTraj, yPercMinmaxTraj, validNumData