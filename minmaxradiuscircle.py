import math
import random
import numpy as np
import functions
from operator import itemgetter

# Data conventions: A point is a pair of floats (x, y). A circle is a triple of floats (center x, center y, radius).

# Returns the smallest circle that encloses all the given points. Runs in expected O(n) time, randomized.
# Input: Two arrays representing x coordinates and y coordinates.
# Output: A triple of floats representing a circle.
# Note: If 0 points are given, None is returned. If 1 point is given, a circle of radius 0 is returned.
#
# Initially: No boundary points known

def make_circle(points):
    # Convert to float and randomize order
    shuffled = [(float(x), float(y)) for (x, y) in points]
    random.shuffle(shuffled)

    # Progressively add points to circle or recompute circle
    c = None

    for (i, p) in enumerate(shuffled):
        if c is None or not point_in_circle(c, p):
            c = _make_circle_one_point(shuffled[0 : i + 1], p)

    return c

def make_circle2(xCoord, yCoord, numData):
    points = np.zeros((numData,2))

    for a in range(numData):
        for b in range(2):
            if b == 0:
                points[a][b] = xCoord[a]
            else:
                points[a][b] = yCoord[a]

    # Convert to float and randomize order
    shuffled = [(float(x), float(y)) for (x, y) in points]
    random.shuffle(shuffled)

    # Progressively add points to circle or recompute circle
    c = None

    for (i, p) in enumerate(shuffled):
        if c is None or not point_in_circle(c, p):
            c = _make_circle_one_point(shuffled[0 : i + 1], p)

    return c

def percent_make_circle(xCoord, yCoord, tempNumData, percent, newX, newY):
    tempPoints = np.zeros((tempNumData,3))

    if round(tempNumData * (percent / 100.0)) > 0:
        numData = round(tempNumData * (percent / 100.0))
    else:
        numData = math.ceil(tempNumData * (percent / 100.0))

    newDist = functions.sqrt_sum_dist(newX, newY, xCoord, yCoord)
    for a in range(tempNumData):
        tempPoints[a][0] = xCoord[a]
        tempPoints[a][1] = yCoord[a]
        tempPoints[a][2] = functions.sqrt_sum_dist(tempPoints[a][0], tempPoints[a][1], xCoord, yCoord)

    listTempPoints = tempPoints.tolist()

    sortedlistTempPoints = sorted(listTempPoints, key=itemgetter(2))

    points = np.asarray(sortedlistTempPoints)

    #print(points.shape)


    #present one
    c1 = make_circle2(points[0:numData, 0], points[0:numData, 1], numData)
    #print(numData)
    #print(len(points[0:numData, 0]))
    #c2 = 0


    return c1

# One boundary point known
def _make_circle_one_point(points, p):
    c = (p[0], p[1], 0.0)
    for (i, q) in enumerate(points):
        if not point_in_circle(c, q):
            #no circle is specified yet
            if c[2] == 0.0:
                c = diameter_circle(p, q)
            #we have two points that are on the boundary of the circle
            else:
                c = make_circle_two_points(points[0 : i + 1], p, q)
    return c


# Two boundary points known
def _make_circle_two_points(points, p, q):
    baseCircle = diameter_circle(p, q)
    leftIncludingCircle = None
    rightIncludingCircle = None
    px, py = p
    qx, qy = q

    # For each point not in the two-point circle
    for r in points:
        if point_in_circle(baseCircle, r):
            continue

        # Form a circumcircle and classify it on left or right side
        # Form a diameter circle and classify it on left or right side

        cross = cross_product(p, q, r)

        c = circum_circle(p, q, r)
        if c is None:
            continue
        elif cross > 0.0:
                    if leftIncludingCircle is None or cross_product(p, q , c) > cross_product(p, q, leftIncludingCircle):
                        leftIncludingCircle = c
        elif cross < 0.0:
                    if rightIncludingCircle is None or cross_product(p, q, c) < cross_product(p, q, rightIncludingCircle):
                        rightIncludingCircle = c


    # Select which circle to return
    # When neither left nor right circle exists
    if leftIncludingCircle is None and rightIncludingCircle is None:
        return baseCircle
    # When there exists only the right circle
    elif leftIncludingCircle is None:
        return rightIncludingCircle
    # When there exists only the left circle
    elif rightIncludingCircle is None:
        return leftIncludingCircle
    # When there exists both the left and right circle
    else:
        return leftIncludingCircle if (leftIncludingCircle[2] <= rightIncludingCircle[2]) else rightIncludingCircle


def make_circle_two_points(points, p, q):
    baseCircle = diameter_circle(p, q)
    leftIncludingCircle = None
    rightIncludingCircle = None
    px, py = p
    qx, qy = q

    # For each point not in the two-point circle
    for r in points:
        if not point_in_circle(baseCircle, r):


        # Form a circumcircle and classify it on left or right side
        # Form a diameter circle and classify it on left or right side


            cross = cross_product(p, q, r)

            c = circum_circle(p, q, r)

            if c is not None:
                if cross > 0.0:
                        if leftIncludingCircle is None or cross_product(p, q , c) > cross_product(p, q, leftIncludingCircle):
                             leftIncludingCircle = c
                elif cross < 0.0:
                        if rightIncludingCircle is None or cross_product(p, q, c) < cross_product(p, q, rightIncludingCircle):
                            rightIncludingCircle = c


    # Select which circle to return
    # When neither left nor right circle exists
    if leftIncludingCircle is None and rightIncludingCircle is None:
        return baseCircle
    # When there exists only the right circle
    elif leftIncludingCircle is None:
        return rightIncludingCircle
    # When there exists only the left circle
    elif rightIncludingCircle is None:
        return leftIncludingCircle
    # When there exists both the left and right circle
    else:
        return leftIncludingCircle if (leftIncludingCircle[2] <= rightIncludingCircle[2]) else rightIncludingCircle


# compute the circumscribed cirecle using three given points
def circum_circle(p, q, r):
    c = moved_circum_circle(q[0]-p[0], q[1]-p[1], r[0] - p[0], r[1] - p[1])
    #rp = math.sqrt(math.pow(c[0]- p[0], 2) + math.pow(c[1] - p[1], 2))
    #rq = math.sqrt(math.pow(c[0]- q[0], 2) + math.pow(c[1] - q[1], 2))
    #rr = math.sqrt(math.pow(c[0]- r[0], 2) + math.pow(c[1] - r[1], 2))
    r = math.sqrt(math.pow(c[0], 2) + math.pow(c[1] , 2))
    return (c[0] + p[0], c[1] + p[1], r)

# compute the circumscribed cirecle using two given points and the origin
def moved_circum_circle(ax, ay, bx, by):
    A = math.pow(ax,2) + math.pow(ay,2)
    B = math.pow(bx,2) + math.pow(by,2)
    C = ax*by - ay*bx
    return ((by*A-ay*B)/(2*C), (ax*B-bx*A)/(2*C))



def make_diameter(p0, p1):
    cx = (p0[0] + p1[0]) / 2.0
    cy = (p0[1] + p1[1]) / 2.0
    r0 = math.hypot(cx - p0[0], cy - p0[1])
    r1 = math.hypot(cx - p1[0], cy - p1[1])
    return (cx, cy, max(r0, r1))

def diameter_circle(p, q):
    x = (p[0] + q[0]) / 2.0
    y = (p[1] + q[1]) / 2.0
    r1 = math.sqrt(math.pow(x - p[0], 2) + math.pow(y - p[1], 2))
    r2 = math.sqrt(math.pow(x - q[0], 2) + math.pow(y - q[1], 2))
    r = max(r1, r2)
    return (x, y, r)


_MULTIPLICATIVE_EPSILON = 1 + 1e-14

def point_in_circle(c, p):
    if c is not None:
        if math.sqrt(math.pow(p[0] - c[0],2)+ math.pow(p[1] - c[1],2)) <= (c[2] * _MULTIPLICATIVE_EPSILON):
            return True
    else:
        return False

    #return c is not None and math.hypot(p[0] - c[0], p[1] - c[1]) <= c[2] * _MULTIPLICATIVE_EPSILON


# Returns twice the signed area of the triangle defined by (x0, y0), (x1, y1), (x2, y2).
def cross_product(x, y, z):
    return (y[0]-x[0])*(z[1]-x[1]) - (z[0]-x[0])*(y[1]-x[1])

def center_of_circle(xData, yData, numData):
    c = make_circle2(xData, yData, numData)
    return c[2]