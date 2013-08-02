#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filekeeper.py 

import os, sys, hashlib, fnmatch
from functools import partial

# TODO
# os.link(source, link_name)

# set to false for quieter output
debug = True 
#debug = False 
#debug = False 
maxdebug = False


if len(sys.argv) > 1:
  path=sys.argv[1]
else:
  print("usage: %s /path/to/scan/") %sys.argv[0]
  sys.exit(1)

def indexer(path):
  filelist={}
  md5sumlist=[]
  if os.path.isdir(path):
    filesindir= os.listdir(path)

    for directory, subdirectories, filenames in os.walk(path):
      if filenames != []:
        for filename in filenames:
          if fnmatch.fnmatch(filename, '*'):
            current_file_name = os.path.join(directory,filename)
            if maxdebug==True:
              print current_file_name
            try:
              md5sum = get_md5sum(current_file_name)
              md5sumlist.append(md5sum)
              filelist[current_file_name]=md5sum
            except IOError:
              print("weird file: %s") %current_file_name
              pass
  else:
    print("%s is a file, not a directory") %path
  
  print("\nRepeated files and md5s:\n")
  for eachmd5 in sorted(set(md5sumlist)):
    x=md5sumlist.count(eachmd5)
    if maxdebug == True:
      print("%s %s") %(eachmd5,x)
    if x > 1:
      for m,n in filelist.items():
        if n == eachmd5:
          print n,m 


# from http://stackoverflow.com/questions/7829499/using-hashlib-to-compute-md5-digest-of-a-file-in-python3
def get_md5sum(filename):
    with open(filename, mode='rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
    return d.hexdigest()

##
# TODO
# os.link works (checked with stat 'filename1' 'filename2')
# in order to link we first need to mv the 'dst' file, 
# then, if link was successful, rm it
# shutil.copy(src,dst)
# os.remove(path) should do it
# 
# another useful feature to add is and --arvg to provide two paths to scan, instead of searching over entire filesystems
# first, put some argparse 




if __name__ == "__main__":
  indexer(path)
