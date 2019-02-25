#!usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil, string, random
import subprocess as s
from subprocess import Popen 
import glob
import fnmatch
import sys

import string
import random
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def set_defaultencoding_globally(encoding='utf-8'):
    assert sys.getdefaultencoding() in ('ascii', 'mbcs', encoding)   
    import imp
    _sys_org = imp.load_dynamic('_sys_org', 'sys')
    _sys_org.setdefaultencoding(encoding)


set_defaultencoding_globally('utf-8')


def get_files(pa):
    matches = {}
    for root, dirnames, filenames in os.walk(pa):
        for filename in fnmatch.filter(filenames, '*.txt'):
            matches[root] = os.path.join(root, filename)
    return matches


class digest:

    def __init__(self, pa=''):
        self.pa = pa

    def reader(self):
        with open(self.pa, mode='r') as raw_data:
            lines = raw_data.readlines()
            for line in lines:
                if line != "" and line != "\n":
                    yield line

    def isGarbage(self):
        fd = open(self.pa)
        s = fd.read()
        if s == 'header\n':
            return True
        return False

    def GetExp(self):
        for ln in self.reader():
            if '==ERROR: AddressSanitizer' in ln:
                return ln
        return id_generator(size=6)

    


garbage1 = []

col = get_files(sys.argv[-1])
s = len(col)

for t in col.keys():
    dg = digest(pa=col[t])
    if dg.isGarbage():
        garbage1.append(t)

for gb in garbage1:
    #print gb
    col.pop(gb)


dup = set()
ng = []

with open('crash.txt','r') as cr4:
    cont = cr4.read()
    t12 = str(cont)
    if 'set([' in t12:
        dup = eval(t12)

for t in col.keys():
    dg = digest(pa=col[t])
    expr = dg.GetExp()
    if expr not in dup:
        dup.add(expr)
        ng.append([t,col[t],expr])
        col.pop(t)

with open('crash.txt','w') as cr:
    cr.write(str(dup))





for w in ng:
    #print w[0]
    if w[2] == '':
        continue
    dst = w[2].split('\n')[0]
    cha = ':!-+0123456789{}()\',. <>'
    for cc in cha:
        dst = dst.replace(cc,'_')
    rdst = os.path.abspath(os.getcwd())
    dst += id_generator(size=6)
    rdst += '/distil/' + dst
    try:
        shutil.copytree(w[0], rdst, symlinks=False, ignore=None)
    except:
        rdst = os.path.abspath(os.getcwd())
        rdst += '/distil/' + id_generator(size=8)
        shutil.copytree(w[0], rdst, symlinks=False, ignore=None)



try:
    shutil.rmtree(sys.argv[-1], ignore_errors=True, onerror=None)
except:pass

try:
    os.system('mkdir '+sys.argv[-1])
except:pass





