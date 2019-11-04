import math
import numpy as np
from pylab import *
from matplotlib import pyplot as plt

# start to calculate area of contour, use green theory
def area(vs):
    a = 0
    x0,y0 = vs[0]
    for [x1,y1] in vs[1:]:
        dx = x1-x0
        dy = y1-y0
        a += 0.5*(y0*dx - x0*dy)
        x0 = x1
        y0 = y1
    return a

#start to use green theory to get centroid of contour
def centroid_for_polygon(polygon,contourarea):
    imax = len(polygon)-1
    cx = 0
    cy = 0
    for i in range(0,imax):
        cx += (polygon[i][0] + polygon[i+1][0]) * ((polygon[i][0] * polygon[i+1][1]) - (polygon[i+1][0] * polygon[i][1]))
        cy += (polygon[i][1] + polygon[i+1][1]) * ((polygon[i][0] * polygon[i+1][1]) - (polygon[i+1][0] * polygon[i][1]))
    cx += (polygon[imax][0] + polygon[0][0]) * ((polygon[imax][0] * polygon[0][1]) - (polygon[0][0] * polygon[imax][1]))
    cy += (polygon[imax][1] + polygon[0][1]) * ((polygon[imax][0] * polygon[0][1]) - (polygon[0][0] * polygon[imax][1]))
    cx /= (contourarea * 6.0)
    cy /= (contourarea * 6.0)
    Coorcentroid = (cx,cy)
    return Coorcentroid

# find perimeter of contour
def find_perimeter(v):
    imax = len(v) - 1
    perimeter = 0
    for i in range(0, imax):
        perimeter += ((v[i][0] - v[i + 1][0]) ** 2 + (v[i][1] - v[i + 1][1]) ** 2) ** 0.5
    return perimeter

# find radial length of sample points
def find_radial_length(sample, center):
    radlen = list()
    smax = len(sample)
    for i in range(0, smax):
        samplen = ((sample[i][0] - center[0]) ** 2 + (sample[i][1] - center[1]) ** 2) ** 0.5
        radlen.append(samplen)
    minradial = min(radlen)
    maxradial = max(radlen)
    return radlen, minradial, maxradial

# find radius of whole points
def find_radius(v, center):
    imax = len(v)
    radiussum = 0
    radius_list = list()
    for i in range(0, imax):
        radius = ((v[i][0] - center[0]) ** 2 + (v[i][1] - center[1]) ** 2) ** 0.5
        radius_list.append(radius)
        radiussum += radius
    radius = float(radiussum) / float(imax)
    maxradius = max(radius_list)
    normalized_radius = float(radius) / float(maxradius)
    return normalized_radius, maxradius

# find curvature
def get_curvature(x, y):
    curvlist = list()
    dx = np.array(np.gradient(x))
    dy = np.array(np.gradient(y))

    d2x_dt2 = np.gradient(dx)
    d2y_dt2 = np.gradient(dy)

    for i in range(len(dx)):
        divi = (dx[i] * dx[i] + dy[i] * dy[i]) ** 1.5
        if divi != 0:
            curvature = np.abs(d2x_dt2[i] * dy[i] - dx[i] * d2y_dt2[i]) / divi
            curvature = curvature**2
            curvlist.append(curvature)
        else:
            curvature = np.abs(d2x_dt2[i] * dy[i] - dx[i] * d2y_dt2[i])
            curvature = curvature**2
            curvlist.append(curvature)
    return curvlist

# find bending energy
def BendingEnergy(sample,samplex,sampley):

    imax = len(sample)
    curvature = get_curvature(samplex,sampley)
    sumcurv = sum(curvature)
    be = float(sumcurv)/float(imax)
    return curvature,be


# random generate angle with 0.01 interval
delta = 0.01
x = np.arange(0, 2*pi, delta)
y = np.arange(0, 2*pi, delta)

# get radius of circle
r = 200

# get centroid axis of circle
xc = 100
yc = 100


# get circle points
for i in range(len(x)):
    x[i] = xc + r*cos(x[i])
    y[i] = yc + r*sin(y[i])


# construct circle points by combining two random x and y lists
v = np.column_stack((x,y))

figure()
plt.plot(x,y)

samplestep = 1
sample = list()
samplex = list()
sampley = list()

# select sample by interval of samplestep
randIndex = np.arange(0,len(v),samplestep)
for i in randIndex:
    samplex.append(v[i-1][0])
    sampley.append(v[i-1][1])
    sample.append(v[i-1])



contourarea = np.abs(area(v))
realarea = pi*(r**2)
print 'right area:', realarea
print 'area:',contourarea,'\n'

Coorcentroid = centroid_for_polygon(v,contourarea)
realcentroid = (xc,yc)
print 'right centroid:',realcentroid
print 'centroid of contour:', Coorcentroid,'\n'


perimeter = find_perimeter(v)
realperimeter = 2*pi*r
print 'right perimeter:',realperimeter
print 'perimeter:', perimeter,'\n'

# find compactness
Compactness = float(perimeter**2)/float(contourarea)
realcompact = float(realperimeter**2)/float(realarea)
print 'right compactness', realcompact
print 'compactness:',Compactness, '\n'

radlen,minradial,maxradial = find_radial_length(sample,Coorcentroid)
print 'radial length list:',radlen
print 'minimum of radial length:',minradial
print 'maximum of radial length:',maxradial,'\n'

normradius,maxradius = find_radius(v,Coorcentroid)
print 'normalized radius:',normradius
print 'maximum radius:',maxradius,'\n'

# find difference between radial and radius
diff_rad = list()
numcom = 0
for i in range(0,len(sample)):
    normal_radial = float(radlen[i])/float(maxradial)
    compartworad = abs(normal_radial-normradius)
    diff_rad.append(compartworad)

    if compartworad <= 0.01:
        numcom +=1

#print 'difference between radial length and normalized radius:', diff_rad
print 'number of difference between radial length and normalized radius below 0.01:',numcom,'\n'

# find entropy of lesion contour
p = float(numcom)/float(len(sample))
#print p
if p >=1:
    Entropy = -(p*math.log(p))
elif p<=0:
    Entropy = -((1-p)*math.log(1-p))
else:
    Entropy = -(p*math.log(p)+(1-p)*math.log(1-p))
print 'entropy:',Entropy

# find ratio of minimum to maximum radial length
radialratio = float(minradial)/float(maxradial)
realradialratio = 1
print 'real radial ratio:',realradialratio
print 'ratio of minimum to maximum radial length:',radialratio, '\n'

curvature,bendingenergy = BendingEnergy(sample,samplex,sampley)
print 'curvature:',curvature
print 'bending energy:', bendingenergy


numsample = len(sample)
numv = len(v)
print 'number of samples:',numsample
print 'number of vertices:',numv
#show()