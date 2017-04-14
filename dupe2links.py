# -*- coding: utf-8 -*-
"""
dupe2links project

@author: %(username)s
"""
# In[]:
#from _NEMOpy.importCalculator import *

# In[]:
import numpy as np
from numpy import *
#%%
import ctypes
import os
import platform
import sys

#%%%
import os
import ntfsutils
from ntfsutils import hardlink
from ntfsutils import junction
#%%%
import hashlib


#%%
def isRunFromIDE(): return 'spyder.'in str(sys.modules)
#%%

def processArgs(verose=False): 
    import argparse     
    aparser = argparse.ArgumentParser(description='search duped files and turn it to NTFS-links')
    aparser.add_argument("-m","--IgnoreSzLess",dest="IgnoreSzLess", type=int, default=1024, help='ignore files with size less ... (def 1024)') 
    aparser.add_argument("-i","--OnlyInfo",dest="onlyInfo", action='store_true', default=False, help='do not create links- just report') 
    aparser.add_argument("-s","--noWaitEnter",dest="noWaitEnter", action='store_true', default=False, help='do not wait Enter after finish') 
    
    aparser.add_argument('dir',             help='dir0 to start recursive search')

    try:
        args = aparser.parse_args()
    except:
        print "_"*80
        if not '-h' in str(sys.argv[1:]):aparser.print_help()
        return
            
    if verose: print args
    
    return args


#%%%

#%%%

#%%%

import subprocess

def makesymlinkViaCmd(origf,newf):
    try:
#        cmdprocess = subprocess.Popen("cmd",
#                                          stdin  = subprocess.PIPE,
#                                          stdout = subprocess.PIPE,
#                                          stderr = subprocess.PIPE)
#        
#        if not os.path.exists(linkname):
#            fullcmd = "mklink " + '"'+newf+'"' + " " + '"'+origf+'"' + "\r\n"
#            print fullcmd
#            cmdprocess.stdin.write(fullcmd)        
#        cmdprocess.terminate()
        print "cmd /C mklink "+ '"'+os.path.abspath(newf)+'"' + " " + '"'+os.path.abspath(origf)+'"'
        cmdprocess = subprocess.Popen("cmd /C mklink "+ '"'+os.path.abspath(newf)+'"' + " " + '"'+os.path.abspath(origf)+'"')
    except:
        print "error on create symlink"
#%%%

def recodeAllStrParam(args):
    def isRunFromIDE(): return 'spyder.'in str(sys.modules)
    def isIterable(x): return hasattr(var,'__iter__')
    def recodeInParam(x): return x if isRunFromIDE() else x.decode('cp1251','ignore') # recode only for work mode! in debug no need to recode!

    for k in vars(args):        
        if isIterable(vars(args)[k]):
            if len(vars(args)[k])>0:
                if type(vars(args)[k][0])==str:
                    vars(args)[k]=map(recodeInParam,vars(args)[k]) 
        else:
            if type(vars(args)[k])==str:
                vars(args)[k]=recodeInParam(vars(args)[k])
    return args

            



#%%%


#%%
#from a import md5ofFile
#import a
def md5ofFile(fname): #http://stackoverflow.com/a/3431838/4278938   http://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

#%%%



def get_free_space(dirname):  ## based on http://stackoverflow.com/questions/51658/cross-platform-space-remaining-on-volume-using-python
    """Return folder/drive free space ."""
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dirname), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value
    else:
        st = os.statvfs(dirname)
        return st.f_bavail * st.f_frsize 

#%%%
#%%%

#%%

def arrayGroupBy(arr,grByCol,srtd=False,asint=False,fltGE=0):
    """"group by col 
    return list of arrays where col value is same
    fltGE used if fltGE>0 and if asint==True
    """
    def useRevSorted(lst,srtd=False):
        return sorted(lst,reverse=True) if srtd else lst
    
    szi=np.int64(arr[:,grByCol]) if asint else arr[:,grByCol] #col to work with
    #print szi
    #print len(szi)
    #print useRevSorted(np.unique(szi),srtd)
    acc=[]
    for y in useRevSorted(np.unique(szi),srtd): #for y in set(szi):
        if asint and(fltGE>0): 
            if y<fltGE: 
                continue #print "fltd" 
        sameSzInd=np.argwhere(szi==y)[:,0]
        #print y
        #print sameSzInd
        if len(sameSzInd)>1: 
            afssi=arr[sameSzInd]
            #print afssi
            acc+=[afssi]#.tolist()]
    return acc

#%%

#%%
def md5sForPFSarr(PFarr):
    "return md5-s vector for array where 1st 2 col is Path and Filename"
    #return array([md5ofFile(p+os.sep+n) for p,n,s in tarr])
    return np.array([md5ofFile(x[0]+os.sep+x[1]) for x  in PFarr])

#%%
import shutil
shutil.copyfile
#%%
#%%
#%%

#%%
#%%
def filterAlreadyLinked(arrayOfSomePF,onlyInfo=False):
    acc1=array(arrayOfSomePF)
#    forig=os.sep.join(acc1[0,:2])
#    print "\norig:\t",forig
#    for x in acc1[1:]:
#        fsame=os.sep.join(x[:2])        
#        print fsame,
#        if hardlink.samefile(forig,fsame):
#            print "already hardlink"
#            continue
        
#%%
#%%

def dupe2link4PFarrayOfSame(arrayOfSomePF,onlyInfo=False):
    acc1=array(arrayOfSomePF)
    forig=os.sep.join(acc1[0,:2])
    print "\norig:\t",forig
    for x in acc1[1:]:
        fsame=os.sep.join(x[:2])        
        print fsame,
        if hardlink.samefile(forig,fsame):
            print "already hardlink"
            continue
        else: print
        if not onlyInfo:
            os.remove(fsame)
            try:
                hardlink.create(forig,fsame)
            except:
                try:
                    print "can't create hardlink. try create symlink"
                    makesymlinkViaCmd(forig,fsame)
                except:
                    print "can't create symlink. sorry. try just copy"
                    try:
                        shutil.copyfile(forig,fsame)
                    except:
                        print "can't copy. please do something manualy!"
                        raw_input()
                    
            
            print "created hardlink"
        else:
            print "need to created hardlink"
                

#dupe2link4PFarrayOfSame(PFarGrpdBymd5s[0],onlyInfo=True)


#%%
#%%
def filterAlreadyLinked(arr):
    trueind=np.where(array([True]+[ not hardlink.samefile(os.sep.join(arr[0,:2]),os.sep.join(x[:2]))  for x in arr[1:] ] ) )
    return arr[trueind]
#filterAlreadyLinked(tarr)    

#%%
#### mainLoop


def dedup2links4arrayOfFiles(afiles,onlyInfo=False):
    aflsGrSzs=arrayGroupBy(afiles,2,True,True,IgnoreSzLess)
    aflsGrSzs
    for tarr in aflsGrSzs:
        tarr=filterAlreadyLinked(tarr)
        if len(tarr)<=1: 
            print os.sep.join(tarr[0,:2])+" already linked group"
            continue
        md5s=md5sForPFSarr(tarr)
        tarrwmd5=np.hstack((tarr,md5s.reshape(-1,1)))
        PFarGrpdBymd5s=arrayGroupBy(tarrwmd5,3)
        #print PFarGrpdBymd5s
        for m in PFarGrpdBymd5s:
            dupe2link4PFarrayOfSame(m,onlyInfo)

#%%

    
#%%


#%%
if __name__=='__main__':
    args=processArgs()
    if args==None: 
        print "error in params"
        exit(1)
    #%%

    
    args = recodeAllStrParam(args)
    
    dir0=args.dir
    if ((not os.path.exists(dir0)) or (not os.path.isdir(dir0))): 
        print "dir param must be existed directory"
        exit(1)
    
    
    IgnoreSzLess=args.IgnoreSzLess
    
    afiles=array([ list((p,x,os.path.getsize(p+os.sep+x))) for (p,d,f) in os.walk(dir0) for x in f ])
    #%%
    #%%
    #%%
    #%%
    
    do=get_free_space(dir0)    
    #print 'do',do 
    
    dedup2links4arrayOfFiles(afiles,onlyInfo=args.onlyInfo)
        
    posle=get_free_space(dir0)    
    print '______'
    print 'options:'
    print 'dir\t=\t',dir0
    print 'onlyInfo\t=\t',args.onlyInfo
    print 'IgnoreSzLess\t=\t',IgnoreSzLess
    print ''
    print ''
    print '___ free space: ___'
    print ''
    print 'before\t',do 
    print 'after \t',posle
    print 'saved \t',posle-do," ~= %.2f MB" % ( ((posle-do)/1024./1024.) )              

    if not args.noWaitEnter:
        print "~~~"
        print "done. press enter..."
        raw_input()



#%%

