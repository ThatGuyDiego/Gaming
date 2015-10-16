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
single_day = 86400


# timestamps are used to creat part of the backup file name
def timestamp():
    N = time.localtime()
    return str(N[0])+str(N[1])+str(N[2])
# built if you wanted to make filenames where one would back 
# up once an hour. Currently not used 
def fulltimestamp():
    N = time.localtime()
    return str(N[0])+str(N[1])+str(N[2])+str(N[3])+str(N[4])

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

def backup():
    bf = backupdir + str(timestamp()) + "_" + backupname+ ".tar"
    spcmd = ["tar","-cvf",bf,mcdir]
    subprocess.call(spcmd)
    subprocess.call(["gzip","-f", bf])

def backup_list():
    dirlist = os.listdir(backupdir)
    backupfiles = []
    for items in dirlist:
        terms = "(\d{6,8})_%s.tar.gz" % (backupname)
        if re.search(terms,items):
            backupfiles.append(items)
    return backupfiles    

def up_to_date_backup():
    bkupfiles = backup_list()
    diff = 0
    day_old = time.time() - single_day
    for items in bkupfiles:
    	temp = backupdir + items
        current =  os.path.getmtime(temp)
        if diff == 0:
        	diff = current
        else:
        	if diff < current:
        		diff = current
    if  day_old > diff:
    	return False
    else:
    	return True
 
def backup_clean():
    bkup_files = backup_list()
    oldest_file =  time.time() - (single_day  * backupdays)
    for files in bkup_files:       
        date_of_file = os.path.getmtime(backupdir+files)  
        if oldest_file > date_of_file:
            delfile = backupdir+files
            os.remove(delfile)


def startmc():
    os.chdir(mcdir)
    sucmd  = mcdir+startupscript
    output = subprocess.Popen(["nohup",sucmd, "&"],\
                              preexec_fn=os.setpgrp\
                              )
    
while True:
    pid = minecraftpid()
    backup_clean()
    if not up_to_date_backup():
        backup()
    elif pid == 0:
        startmc()      
    time.sleep(60)



    '''
    Some notes:

    I didn't use pidof because one might run multiple instances of java:

    example:
    mc_admin  3004  0.8  7.9 5807308 647696 ?      Sl   17:48   1:48 java -server -Xms1G -Xmx4G -XX:+UseParNewGC -XX:+UseConcMarkSweepGC -XX:+CMSIncrementalPacing -XX:ParallelGCThreads=4 -XX:+AggressiveOpts -jar /home/minecraft_SNAP/minecraft_server.1.8.7.jar nogui
    mc_admin  4797 24.0 13.5 5918912 1107744 pts/0 Sl   21:14   2:27 java -server -Xms1G -Xmx4G -XX:+UseParNewGC -XX:+UseConcMarkSweepGC -XX:+CMSIncrementalPacing -XX:ParallelGCThreads=4 -XX:+AggressiveOpts -jar /home/minecraft/minecraft_server.1.8.7.jar nogui

    so minecraftpid uses pidre to look through ps auxxx . note only java 
    instance that match mcdir var. It also includes some other static 
    content to help avoid false positives. 


    fulltimestamp function may be used in the future if you want multiple backups in 24 hours

    '''
