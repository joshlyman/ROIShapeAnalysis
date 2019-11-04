from pylab import *
import SimpleITK
from matplotlib import pyplot as plt
import numpy as np
import csv
import os
import fnmatch

#filename = '/Users/yanzhexu/Google Drive/Marley Grant Data/CEDM pilot data-selected/malignant'

# for casefile in os.listdir(filename):
#     if casefile.startswith('.'):
#         continue
#     if casefile.startswith('..'):
#         continue
#     if fnmatch.fnmatch(casefile, '*Icon*'):
#         continue
#
#     print casefile
#
#     filename2 = os.path.join(filename, casefile)
#     for dicomfile in os.listdir(filename2):
#         if dicomfile.startswith('.'):
#             continue
#         if dicomfile.startswith('..'):
#             continue
#         if fnmatch.fnmatch(dicomfile, '*Icon*'):
#             continue
#         if not fnmatch.fnmatch(dicomfile, '*coor.txt'):
#             continue
#         # if dicomfile == 'Pt1 - LE - CC.dcm':
#         #     continue
#
#
#         # read image to array
#         print dicomfile

filename = '/Users/yanzhexu/Google Drive/Marley Grant Data/CEDM pilot data-selected/benign'

num =0
casenum = 0
for casefile in os.listdir(filename):
    if casefile.startswith('.'):
        continue
    if casefile.startswith('..'):
        continue
    if fnmatch.fnmatch(casefile, '*Icon*'):
        continue

    casenum+=1
    casefile = 'Pt1'

    filename2 = os.path.join(filename, casefile)
    for coorfile in os.listdir(filename2):
        if coorfile.startswith('.'):
            continue
        if coorfile.startswith('..'):
            continue
        if fnmatch.fnmatch(coorfile, '*Icon*'):
            continue
        if fnmatch.fnmatch(coorfile,'*largest_rec*csv'):
            continue
        if fnmatch.fnmatch(coorfile, '*texture*'):
            continue
        if not fnmatch.fnmatch(coorfile, '*CC*csv'):
            if not fnmatch.fnmatch(coorfile, '*MLO*csv'): # pt25 only have CC1.csv/MLO.csv
                continue

        filename3 = os.path.join(filename2,coorfile)
        if coorfile is None:
            print'Lost coordinate CSV file'
        #print coorfile

        v = list()
        vx = list()
        vy = list()
        num += 1

        with open(filename3,'r') as contourfile:
            contourlist = csv.reader(contourfile)
            row1 = next(contourlist)
            row2 = next(contourlist)

            numv = int(row2[14])

            for i in range(numv):
                columnx = 18 + 5*i # column 19
                columny = 19 + 5*i # column 20
                v.append([float(row2[columnx]), float(row2[columny])])
                vx.append(float(row2[columnx]))
                vy.append(float(row2[columny]))

        patientID = casefile

        if fnmatch.fnmatch(coorfile,'*CC*') is True:
            phasename = 'CC'

        elif fnmatch.fnmatch(coorfile,'*MLO*') is True:
            phasename = 'MLO'

        else:
            phasename = coorfile.split('.')[0]

        print patientID
        print phasename





print num
print casenum



    # print row1
    # print row2
    # print numv
    # print numvx
    # print numvy
    # print v[0],v[1]
    # print vx[0]
    # print vy[0]

#phasename = filename2.split('.')[0].split('_')[0].split('-')[1]+filename2.split('.')[0].split('_')[0].split('-')[2]

#print phasename
# v = list()
# vx = list()
# vy = list()
#
# with open(filename2, 'r') as roifile:
#     roiCoordsList = csv.reader(roifile, delimiter=';')
#     for row in roiCoordsList:
#         # v.append([row[0],row[1]])
#         # vx.append(row[0])
#         # vy.append(row[1])
#         v.append([int(row[0]), int(row[1])])
#         vx.append(int(row[0]))
#         vy.append(int(row[1]))
#
# #
# # for vi in v:
# #     vi[0] = int(vi[0])
# #     vi[1] = int(vi[1])
#
# x,y = v[0]
#
# print x
# print y
# print v[0],v[1]
# print vx[0]
# print vy[0]


