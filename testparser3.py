import os
import fnmatch

filename = '/Users/yanzhexu/Google Drive/Marley Grant Data/Marley Grant Data'

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

                print dcmfile
                filename5 = os.path.join(filename4,dcmfile)

                dcmname = casefile.split('-')[0] + phasefolder.split('-')[0]
                print dcmname
