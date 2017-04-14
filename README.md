## dupe2links ##

search duped files and turn it to NTFS-links 


### require ###
operation system and file system that supports symlinks and hardlinks
(tested on NTFS on Windows 6.1) 

python 2.7

python modules: platform,ntfsutils,hashlib
and usual ones: numpy,ctypes,os,sys,os

### How to use: ###
```
usage: dupe2links.py [-h] [-m IGNORESZLESS] [-i] [-s] dir

search duped files and turn it to NTFS-links

positional arguments:
  dir                   dir0 to start recursive search

optional arguments:
  -h, --help            show this help message and exit
  -m IGNORESZLESS, --IgnoreSzLess IGNORESZLESS
                        ignore files with size less ... (def 1024)
  -i, --OnlyInfo        do not create links- just report
  -s, --noWaitEnter     do not wait Enter after finish
```
#### how it work:
found dupes and make them to hardlink (try use hardlink and symlink if hardlink fail) to one of copyes (random one).

## WARNING
 1. this script is provided AS IS without warranty, although all reasonable efforts was made to work it properly, but all possible damages is on your responsiblity!
 2. this script include file deletion operation - be carefully! (See item 1)
 3. There may be errors with the non-ASCII-filenames. I tryed to avoid them but, damn it, there are always such strange symbols that all efforts mean nothing. And anybody who use such symbols in filenames really deserved all errors that come from them.

### _____________ ###
(c) master_Nemo 2017 All right reserved