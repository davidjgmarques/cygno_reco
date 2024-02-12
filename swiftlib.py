#!/usr/bin/env python
import uproot
import midas.file_reader
import h5py
import cygno as cy
import os

def swift_root_file(tag, run):
    sel = rootlocation(tag,run)    
    BASE_URL = "https://s3.cloud.infn.it/v1/AUTH_2ebf769785574195bde2ff418deac08a/"
    if 'MC' in tag:
        bucket = 'cygnus' if tag=='MC-old' else 'cygno-sim'
    elif tag=='Data':
        bucket = 'cygnus' if run<4505 else 'cygno-data'
    elif tag=='DataMango':
        bucket = 'cygnus' if run<3242 else 'cygno-data'
    BASE_URL = BASE_URL + bucket + '/'
    file_root = (sel+'/histograms_Run%05d.root' % run)
    return BASE_URL+file_root

    
def reporthook(blocknum, blocksize, totalsize):
    import sys
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*d / %d" % (
            percent, len(str(totalsize)), readsofar, totalsize)
        sys.stderr.write(s)
        if readsofar >= totalsize: # near the end
            sys.stderr.write("\n")
    else: # total size is unknown
        sys.stderr.write("read %d\n" % (readsofar,))

def swift_download_root_file(url,run,tmp=None,justName=False):
    import ROOT
    from urllib.request import urlretrieve
    try:
        USER = os.environ['USER']
    except:
        USER = "" # os.environ['JUPYTERHUB_USER']
    tmpdir = tmp if tmp else '/tmp/'
    if tmpdir == '/tmp/':
         os.system('mkdir -p {tmpdir}/{user}'.format(tmpdir=tmpdir,user=USER))
         tmpname = ("%s/%s/histograms_Run%05d.root" % (tmpdir,USER,run))
    else:
         tmpname = ("%s/histograms_Run%05d.root" % (tmpdir,run))
    if not justName:
        urlretrieve(url, tmpname, reporthook)
    return tmpname 

def rootlocation(tag,run):
    
    if tag == 'Data':
        if (run>=936) and (run<=1601):
            sel = 'Data/LTD/Data_Camera/ROOT'
        elif (run>=1632) and (run<4505):
            sel = 'Data/LAB'
        elif (run>=4470) and (run<10000):
            sel = 'LAB'
        else:
           print("WARNING: Data taken with another DAQ or not yet uploaded to the cloud")
           exit()
    elif tag == 'DataMango':
            sel= 'Data/MAN' if run<3242 else 'MAN' 
    elif tag == 'MC':
        sel = 'Simulation'
        print("WARNING: automatic download for Simulated data not implemented yet")
        exit()
        
    return sel

def swift_read_root_file(tmpname):
    f  = uproot.open(tmpname)
    return f

def swift_read_h5_file(tmpname):
    f  = h5py.File(tmpname, 'r')
    return f

def swift_rm_root_file(tmpname):
    import os
    os.remove(tmpname)
    print("tmp file removed")

def checkfiletmp(run,tier,tmp=None):
    import os.path
    try:
        USER = os.environ['USER']
    except:
        USER = "" # os.environ['JUPYTERHUB_USER']
    tmpdir = tmp if tmp else '/tmp/'
    
    if tmpdir=='/tmp/':
         os.system('mkdir -p {tmpdir}/{user}'.format(tmpdir=tmpdir,user=USER))
         if tier=='root':
             return os.path.isfile("%s/%s/histograms_Run%05d.root" % (tmpdir,USER,run))
         elif tier=='h5':
             return os.path.isfile("%s/%s/histograms_Run%05d.h5" % (tmpdir,USER,run))
         else:
             return os.path.isfile("%s/%s/run%05d.mid.gz" % (tmpdir,USER,run))
    else:
        if tier=='root':
            return os.path.isfile("%s/histograms_Run%05d.root" % (tmpdir,run))
        elif tier=='h5':
            return os.path.isfile("%s/histograms_Run%05d.h5" % (tmpdir,run))
        else:
            return os.path.isfile("%s/run%05d.mid.gz" % (tmpdir,run))

def swift_download_midas_file(run,tmpdir,tag='LNGS'):
    print("download or open midas file for run ",int(run))
    mfile = cy.open_mid(int(run), path=tmpdir, cloud=True, tag=tag, verbose=True)
    return mfile
    
def root_TH2_name(root_file):
    pic = []
    wfm = []
    for i,e in enumerate(root_file.GetListOfKeys()):
        che = e.GetName()
        if ('pic_run' in str(che)):
            pic.append(che)
        elif ('wfm_run' in str(che)):
            wfm.append(che)
    return pic, wfm

def swift_pedestal_file(run):
    pedrun = selectPedestal(run)    
    
    BASE_URL = "https://s3.cloud.infn.it/v1/AUTH_2ebf769785574195bde2ff418deac08a/cygnus/Pedestals/"
    file_root = ('pedmap_run%05d_rebin1.root' % pedrun)
    return BASE_URL+file_root

def selectPedestal(run):
    
    f = open('runvspedmap.txt', "r")
    params = eval(f.read())
    
    for k,v in params.items():
        setattr(options,k,v)
        
    options.pedavailable
    
 
    return sel
