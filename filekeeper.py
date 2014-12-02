#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filekeeper.py 

import os, sys, hashlib, fnmatch
from functools import partial

import argparse
parser = argparse.ArgumentParser(
  description='Files keeper, keeps your files unique',
  epilog="Find duplicate files, save storage space")
#parser.add_argument('-p', '--path', help='/path/to/scan/', dest='inputPath', type=str)
parser.add_argument('-p', '--path', help='/path/to/scan/', dest='inputPath', type=str, required=True)
#parser.add_argument('-p', '--path', help='/path/to/scan/', dest='inputPath', type=str, default="./")
parser.add_argument('-s' ,'--save', help='save to file', dest='outputFile', type=str)
# for multiple input paths, use nargs ## https://docs.python.org/2/library/argparse.html#nargs

# set to false for quieter output
debug = True 
maxdebug = False


if len(sys.argv) <= 1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()
path = args.inputPath
outputFile=args.outputFile


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
  #save to file option
  if outputFile != None:
    print("results will we saved to: %s" %outputFile) 
  
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




if __name__ == "__main__":
  indexer(path)
