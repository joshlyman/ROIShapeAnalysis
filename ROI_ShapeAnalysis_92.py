from pylab import *
import SimpleITK
from matplotlib import pyplot as plt
import numpy as np
import csv
import os
import fnmatch

filename = '/Users/yanzhexu/Google Drive/Marley Grant Data/Marley Grant Data'

outcsv = '/Users/yanzhexu/Desktop/Research/ROI_ShapeDescriptors_92.csv'

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

num = 0
casenum = 0
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

        # print casefile

        filename2 = os.path.join(filename, casefile)

        for phasefolder in os.listdir(filename2):
            if phasefolder.startswith('.'):
                continue
            if phasefolder.startswith('..'):
                continue
            if fnmatch.fnmatch(phasefolder, '*Icon*'):
                continue
            if fnmatch.fnmatch(phasefolder, '*roi*'):
                continue

            filename3 = os.path.join(filename2, phasefolder)

            for coorfile in os.listdir(filename3):
                if coorfile.startswith('.'):
                    continue
                if coorfile.startswith('..'):
                    continue
                if fnmatch.fnmatch(coorfile, '*Icon*'):
                    continue
                if fnmatch.fnmatch(coorfile, '*largest_rec*csv'):
                    continue
                if fnmatch.fnmatch(coorfile, '*texture*'):
                    continue
                if not fnmatch.fnmatch(coorfile, '*CC*csv'):
                    if not fnmatch.fnmatch(coorfile, '*MLO*csv'):
                        if not fnmatch.fnmatch(coorfile, '*LM*csv'):
                            continue

                filename4 = os.path.join(filename3, coorfile)
                if coorfile is None:
                    print'Lost coordinate CSV file'
                # print coorfile

                # dont have too much number of points so only use all vertice points
                v = list()
                vx = list()
                vy = list()
                num += 1

                with open(filename4, 'r') as contourfile:
                    contourlist = csv.reader(contourfile)
                    row1 = next(contourlist)
                    row2 = next(contourlist)

                    numv = int(row2[14])

                    for i in range(numv):
                        columnx = 18 + 5 * i  # column 19
                        columny = 19 + 5 * i  # column 20
                        v.append([float(row2[columnx]), float(row2[columny])])
                        vx.append(float(row2[columnx]))
                        vy.append(float(row2[columny]))

                patientID = casefile.split('-')[0]

                if fnmatch.fnmatch(coorfile, '*CC*') is True:
                    phasename = 'CC'
                elif fnmatch.fnmatch(coorfile, '*MLO*') is True:
                    phasename = 'MLO'
                elif fnmatch.fnmatch(coorfile, '*LM*') is True:
                    phasename = 'LM'
                else:
                    phasename = coorfile.split('.')[0]
                    # print sample

                contourarea = np.abs(area(v))
                print patientID
                print v
                print len(vx)
                print 'area:', contourarea

                Coorcentroid = centroid_for_polygon(v, contourarea)
                # print 'centroid of contour:', Coorcentroid

                perimeter = find_perimeter(v)
                # print 'perimeter:', perimeter

                # find compactness
                Compactness = float(perimeter ** 2) / float(contourarea)
                # print 'compactness:',Compactness

                radlen, minradial, maxradial = find_radial_length(v, Coorcentroid)
                # print 'radial length list:',radlen
                # print 'minimum of radial length:',minradial
                # print 'maximum of radial length:',maxradial

                normradius, maxradius = find_radius(v, Coorcentroid)
                # print 'normalized radius:',normradius
                # print 'maximum radius:',maxradius

                # find difference between radial and radius
                diff_rad = list()
                numcom = 0
                for i in range(0, len(v)):
                    normal_radial = float(radlen[i]) / float(maxradial)
                    compartworad = abs(normal_radial - normradius)
                    diff_rad.append(compartworad)

                    if compartworad <= 0.01:
                        numcom += 1

                # find entropy of lesion contour
                p = float(numcom) / float(len(v))
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

                curvature, bendingenergy = BendingEnergy(v, vx, vy)
                # print 'curvature:',curvature
                # print 'bending energy:', bendingenergy
                numsample = len(v)

                shapedescriptors = [patientID,phasename, Compactness, Entropy, bendingenergy, radialratio]

                descriptorWriter.writerow(shapedescriptors)




