import os, sys, inspect, glob

from PIL import Image   #I am using Pillow! pip install pillow
import sizesort
import check
import pixelcheck
from os.path import basename
import bar



def dupemain(path,dupesim,samplesize):
    #print(path)
    samplesize=float(samplesize)
    dupesim = int(dupesim)
    dupemap={}


    data = open("gensimilarity.txt", "w")

    #data.write('working with'+ str(dupesim))
    #data.write('similarity \n')
    similar = [] #similarpictures
    matchfound1=[]
    matchfound2=[]
    simresult=0

    fixes=["*.jpg","*.png","*.jpeg","*.JPEG","*.PNG","*.JPEG"]


    for fixmain in fixes:
        #print('fixmain: '+fixmain)
        for name1 in glob.glob(path+fixmain):
            #print ("comping:"+ name1)
            pic1 = Image.open(name1)
            #match vorhanden dann nicht, wenn nicht dann checken
            z=True
            for index in matchfound2:
                if index == name1 :
                    #print('DUPE')
                    pic1.close()
                    z=False

            if z :
                z=True
                #jeder fix mit jedem fix
                for fixmini in fixes:
                    #print('fixmini: '+fixmini)
                    for name2 in glob.glob(path+fixmini):
                        #print("mit: "+ name2)
                        pic2 = Image.open(name2)
                        p=True
                        bar.incprog() # ----
                        for index in matchfound1:
                            if index == name2:
                                #print('taken')
                                pic2.close()
                                p=False



                        if p:
                            p=True
                            if name1 != name2 and check.checkformat(pic1,pic2) :

                                simresult = pixelcheck.pixelmain(pic1,pic2,samplesize,dupesim)

                                if simresult >=dupesim :
                                    similar.append(name1)
                                    similar.append(name2)  #noted for further inspection!

                                    bar.incstep() #---

                                    matchfound2.append(str(name2))

                                    dupemap[basename(name2)]=basename(name1)

                                    data.write(basename(name1))
                                    data.write(";")
                                    data.write(basename(name2))
                                    data.write(";")
                                    data.write(str(float(simresult)))
                                    data.write(";\n")




                                #WRITE RESULTS IN A FILE [NAME and NAME , SIMILARITY = simresult ]
                                matchfound1.append(str(name1))


                            pic2.close()
                        else:
                            p=True
            else:
                z=True


            pic1.close()
    data.close()

    print('\ntotal: '+str(check.piccounter(path))+ '  Dupes: ' + str(len(matchfound2))+ '  Unique: '+ str(  (check.piccounter(path))-(len(matchfound2))   ))


    #return DICTIONARY MAP!


    return dupemap


def twocomp(dir1,dir2):
    try :
        pic1=Image.open(dir1)
    except FileNotFoundError:
        print('wrong file path on path1'+path1)
        return None
        #NOT FileNotFoundError

    try:
        pic2=Image.open(dir2)
    except FileNotFoundError:
        print('wrong file path on path2'+path2)
        return None


    simresult = pixelcheck.pixelmain(pic1,pic2,-1,0)

    pic1.close()
    pic2.close()
    return simresult
