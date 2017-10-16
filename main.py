
---
title: main
date: 2017-09-15 22:54:44
tags:
---
        from os import listdir
from os.path import isfile, join, splitext
import os
def insert(originalfile, prepent_line):
    with open(originalfile,'r') as f:
        with open('./new/newfile.txt','w') as f2: 
            f2.write(prepent_line)
            f2.write(f.read())
    os.rename('./new/newfile.txt', './new/{}'.format(originalfile))

if __name__ == '__main__':
    mypath = '.'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for fname in onlyfiles:
        basename = splitext(fname)[0]
        
        basename = basename.decode('GBK')
        prepent_line = u'''
---
title: {}
date: 2017-09-15 22:54:44
tags:
---
        '''.format(basename)
        
        
        
        insert(fname, prepent_line.encode('utf-8'))
