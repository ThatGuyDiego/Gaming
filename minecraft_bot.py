#!/usr/bin/python

'''
this was built with a Linux server in mind using with TAR and GZIP binaries installed. 
It launches at boot, starts up minecraft and run backups
Currently tested on a debian but it should work on any Linux distro
Has not been tested in OSX but again if TAR and GZIP are there, then it should work. 
'''

import re
import subprocess
import time
import os


pidre = "\w+\s+(\d+).+java.+-jar\s(/.+/).+"
mcdir = "" # directory where Minecraft runs
backupdir = "" #backup directory
backupname = "minecraft" # you can change this to anything
backuplookup = "\d+_%s.tar.gz" % (backupname)
startupscript = "minecraft.sh" # start up script
backupdays = 10 # number of days you want to have backups for
ltime = time.time()
butoffset = ltime - (backupdays * 86400)

def exists(filepath,filename):
    return filename in os.listdir(filepath)

def minecraftpid():
    pid = 0
    stringaux = subprocess.check_output(["ps","auxxx"])
    listaux = stringaux.split("\n")
    for items in listaux:
        if re.search(pidre,items):
            possible = re.search(pidre,items)
            if possible.group(2) == mcdir:
                pid = possible.group(1)
    return pid

def timestamp():
    N = time.localtime()
    return str(N[0])+str(N[1])+str(N[2])

# I use this while loop as i had an issue when in some cases the gzip would not occour if the server was rebooted
# this ensures the tar file is gziped
def backupzip(backupfile):
    while not exists(backupdir,backupfile+".gz"):
        subprocess.call(["gzip","-f",backupdir+backupfile])

def backup():
    ts = timestamp()   
    bf = str(ts) + "_" + backupname+ ".tar"
    fbf = backupdir + bf
    if not exists(backupdir,(bf+".gz")):
        spcmd = ["tar","-cvf",fbf,mcdir]
        subprocess.call(spcmd)
        backupzip(bf)
        
def rotatebackup():
    for items in os.listdir(backupdir):
        if re.search(backuplookup,items):
            if os.path.getctime(backupdir+items) <= butoffset:
                os.remove(backupdir+items)

def startmc():
    os.chdir(mcdir)
    sucmd  = mcdir+startupscript
    output = subprocess.Popen(["nohup",sucmd, "&"],\
                              preexec_fn=os.setpgrp\
                              )


laststamp = 0

while True:
    pid = minecraftpid()
    if laststamp + 86400 < time.time():
        backup()
        time.sleep(5)
        rotatebackup()
        laststamp = time.time()
    elif pid == 0:
        startmc()
    time.sleep(10)



