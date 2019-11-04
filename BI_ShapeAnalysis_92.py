from pylab import *
import SimpleITK
from matplotlib import pyplot as plt
import numpy as np
import csv
import os
import fnmatch

filename = '/Users/yanzhexu/Google Drive/Marley Grant Data/Marley Grant Data'

outcsv = '/Users/yanzhexu/Desktop/Research/ShapeDescriptors_92cases.csv'

#title = ['dicom file','compactness','entropy', 'bending energy','ratio(min/max)','perimeter','area','normalized_radius','min of radial length','max of radial length']
title = ['patient ID','phase','compactness','entropy','bending energy','ratio(min/max)']

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

# find radial length
def find_radial_length(sample, center):
    radlen = list()
    smax = len(sample)
    for i in range(0, smax):
        samplen = ((sample[i][0] - center[0]) ** 2 + (sample[i][1] - center[1]) ** 2) ** 0.5
        radlen.append(samplen)
    minradial = min(radlen)
    maxradial = max(radlen)
    return radlen, minradial, maxradial

# find radius
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
            curvature  = curvature**2
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

with open(outcsv, 'wb') as CSVFile:
    descriptorWriter = csv.writer(CSVFile, dialect='excel')
    descriptorWriter.writerow(title)

    for casefile in os.listdir(filename):
        if casefile.startswith('.'):
            continue
        if casefile.startswith('..'):
            continue
        if fnmatch.fnmatch(casefile, '*Icon*'):
            continue
        print casefile

        filename2 = os.path.join(filename, casefile)
        #print os.listdir(filename)
        for casefile2 in os.listdir(filename2):
            if casefile2.startswith('.'):
                continue
            if casefile2.startswith('..'):
                continue
            if fnmatch.fnmatch(casefile2, '*Icon*'):
                continue
            if fnmatch.fnmatch(casefile2, '*roi*'):
                continue

            #print casefile2

            filename3 = os.path.join(filename2,casefile2)

            for phasefolder in os.listdir(filename3):

                filename4 = os.path.join(filename3,phasefolder)
                if phasefolder.startswith('.'):
                    continue
                if phasefolder.startswith('..'):
                    continue
                if phasefolder.startswith('*Icon*'):
                    continue
                if os.path.isfile(filename4):
                    continue

                #print phasefolder


                for dcmfile in os.listdir(filename4):
                    if not fnmatch.fnmatch(dcmfile, '*dcm'):
                        continue

                    #print dcmfile

                    dcmname = casefile.split('-')[0] + phasefolder.split('-')[0]
                    print dcmname

                    patientID = casefile.split('-')[0]
                    phasename = phasefolder.split('-')[0]

                    filename5 = os.path.join(filename4, dcmfile)
                    rawImage = SimpleITK.ReadImage(filename5)
                    imgArray = SimpleITK.GetArrayFromImage(rawImage)

                    if len(imgArray.shape) == 3:
                        imgArray = imgArray[0, :, :]

                    # create a new figure
                    # figure()

                    # show contours with origin upper left corner
                    c = plt.contour(imgArray, levels=[245], colors='black', origin='image')

                    # path means number of contours, 0 usually means largest contour
                    arealist = list()
                    numver = list()
                    pathnum = list()
                    # path means number of contours, 0 usually means largest contour
                    for i in range(len(c.collections[0].get_paths())):
                        vi = c.collections[0].get_paths()[i].vertices

                        contourarea = np.abs(area(vi))

                        if contourarea < 100:
                            continue
                        num = len(vi)
                        arealist.append(contourarea)
                        numver.append(num)
                        pathnum.append(i)

                    print 'area list', arealist
                    print 'number of vertices', numver
                    # max_value = max(pathlist)
                    max_value = max(numver)
                    # max_index = pathlist.index(max_value)
                    contouindex = numver.index(max_value)
                    pathindex = pathnum[contouindex]

                    v = c.collections[0].get_paths()[pathindex].vertices

                    print 'vertices of path:', v

                    contourarea = arealist[contouindex]
                    print 'area:', contourarea

                    # print 'vertices of path:',v
                    # show()
                    # get sample
                    # samplesize = 800
                    samplestep = 1
                    sample = list()
                    samplex = list()
                    sampley = list()

                    # random select samples
                    # randIndex = np.random.choice(len(v),samplesize)

                    # select sample by interval of samplestep
                    randIndex = np.arange(0, len(v), samplestep)
                    for i in randIndex:
                        samplex.append(v[i - 1][0])
                        sampley.append(v[i - 1][1])
                        sample.append(v[i - 1])
                    # print sample

                    Coorcentroid = centroid_for_polygon(v, contourarea)
                    # print 'centroid of contour:', Coorcentroid

                    perimeter = find_perimeter(v)
                    # print 'perimeter:', perimeter

                    # find compactness
                    Compactness = float(perimeter ** 2) / float(contourarea)
                    # print 'compactness:',Compactness

                    radlen, minradial, maxradial = find_radial_length(sample, Coorcentroid)
                    # print 'radial length list:',radlen
                    # print 'minimum of radial length:',minradial
                    # print 'maximum of radial length:',maxradial

                    normradius, maxradius = find_radius(v, Coorcentroid)
                    # print 'normalized radius:',normradius
                    # print 'maximum radius:',maxradius

                    # find difference between radial and radius
                    diff_rad = list()
                    numcom = 0
                    for i in range(0, len(sample)):
                        normal_radial = float(radlen[i]) / float(maxradial)
                        compartworad = abs(normal_radial - normradius)
                        diff_rad.append(compartworad)

                        if compartworad <= 0.01:
                            numcom += 1

                    # print 'difference between radial length and normalized radius:', diff_rad
                    # print 'number of difference between radial length and normalized radius below 0.01:',numcom

                    # find entropy of lesion contour
                    p = float(numcom) / float(len(sample))
                    # print p
                    if p >= 1:
                        Entropy = -(p * math.log(p))
                    elif p <= 0:
                        Entropy = -((1 - p) * math.log(1 - p))
                    else:
                        Entropy = -(p * math.log(p) + (1 - p) * math.log(1 - p))
                    # print 'entropy:',Entropy

                    # find ratio of minimum to maximum radial length
                    radialratio = float(minradial) / float(maxradial)
                    # print 'ratio of minimum to maximum radial length:',radialratio

                    curvature, bendingenergy = BendingEnergy(sample, samplex, sampley)
                    # print 'curvature:',curvature
                    # print 'bending energy:', bendingenergy
                    numsample = len(sample)

                    shapedescriptors = [patientID,phasename, Compactness, Entropy, bendingenergy, radialratio]

                    descriptorWriter.writerow(shapedescriptors)




