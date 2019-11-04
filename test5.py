from pylab import *
import SimpleITK
from matplotlib import pyplot as plt
import numpy as np
import csv
import os
import fnmatch


filename = '/Users/yanzhexu/Google Drive/Marley Grant Data/Marley Grant Data'

num =0
for casefile in os.listdir(filename):
    if casefile.startswith('.'):
        continue
    if casefile.startswith('..'):
        continue
    if fnmatch.fnmatch(casefile, '*Icon*'):
        continue

    #print casefile


    filename2 = os.path.join(filename, casefile)

    for phasefolder in os.listdir(filename2):
        if phasefolder.startswith('.'):
            continue
        if phasefolder.startswith('..'):
            continue
        if fnmatch.fnmatch(phasefolder,'*Icon*'):
            continue
        if fnmatch.fnmatch(phasefolder,'*roi*'):
            continue

        filename3 = os.path.join(filename2,phasefolder)

        for coorfile in os.listdir(filename3):
            if coorfile.startswith('.'):
                continue
            if coorfile.startswith('..'):
                continue
            if fnmatch.fnmatch(coorfile, '*Icon*'):
                continue
            if fnmatch.fnmatch(coorfile,'*largest_rec*csv'):
                continue
            if fnmatch.fnmatch(coorfile,'*texture*'):
                continue
            if not fnmatch.fnmatch(coorfile, '*CC*csv'):
                if not fnmatch.fnmatch(coorfile, '*MLO*csv'):
                    if not fnmatch.fnmatch(coorfile,'*LM*csv'):
                        continue

            filename4 = os.path.join(filename3,coorfile)
            if coorfile is None:
                print'Lost coordinate CSV file'
            #print coorfile

            v = list()
            vx = list()
            vy = list()
            num +=1

            with open(filename4,'r') as contourfile:
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
            elif fnmatch.fnmatch(coorfile,'*LM*') is True:
                phasename = 'LM'
            else:
                phasename = coorfile.split('.')[0]

            print patientID
            print phasename
print num

            # numvx = len(vx)
            # numvy = len(vy)

