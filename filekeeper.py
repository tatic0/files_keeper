#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filekeeper.py 

import os, sys, hashlib, fnmatch

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
              f = open(current_file_name, 'rb')
              h = hashlib.md5()
              h.update(f.read())
              md5sum = h.hexdigest()
              f.close()
              md5sumlist.append(md5sum)
              filelist[current_file_name]=md5sum
            except IOError:
              print("weird filename: %s") %current_file_name
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

if __name__ == "__main__":
  indexer(path)