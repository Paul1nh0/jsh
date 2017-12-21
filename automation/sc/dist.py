#!usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil, string, random
import subprocess as s
from subprocess import Popen 
import glob
import fnmatch
import sys


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
        for ln in self.reader():
            if 'Debugger' in ln:
                return False
        return True

    def Fail(self):
        for ln in self.reader():
            if ('Break instruction exception' in ln) or ('Access violation' in ln):
                return False
        return True

    def NotExp(self):
        for ln in self.reader():
            if ('NtWaitForWorkViaWorkerFactory' in ln) or ('NtGdiDdDDIWaitForVerticalBlankEvent' in ln) or ('NtUserMsgWaitForMultipleObjects' in ln):  
                return True
        return False

    def Ret(self):
        for ln in self.reader():
            if ('NtWaitForWorkViaWorkerFactory' in ln) or ('NtGdiDdDDIWaitForVerticalBlankEvent' in ln) or ('NtUserMsgWaitForMultipleObjects' in ln) or ('NtAlpcSendWaitReceivePort' in ln):  
                return True
        return False

    def GetExp(self):
        bRet = ''
        i = 0
        for ln in self.reader():
            if i == 0.5:
                bRet += ln +'\n'
                i += 1
            elif i == 1.5:
                bRet += ln +'\n'
                i = 0
            elif i == 1:
                i += 1
                continue
            elif i == 2:
                bRet += ln +'\n'
                i += 1
            elif i == 3:
                bRet += ln +'\n'
                i = 0
            if ('First chance exceptions are reported before any exception handling.' in ln):
                i += 1 
            elif ('Access violation - code c0000005 (!!! second chance !!!)' in ln):
                i = 0.5
        return bRet

    def RaisEx(self):
        for ln in self.reader():
            if 'RaiseException' in ln:
                return True
        return False

    


garbage1 = []
garbage2 = []
garbage3 = []
garbage4 = []
RaiseExp = []

col = get_files(sys.argv[-1])
s = len(col)
#print len(col)

for t in col.keys():
    dg = digest(pa=col[t])
    if dg.isGarbage():
        garbage1.append(t)

for gb in garbage1:
    #print gb
    col.pop(gb)

#print len(garbage1)

#for k in col:
#    print k, col[k]

#print len(col)
#print s - len(garbage1)

for t in col.keys():
    dg = digest(pa=col[t])
    if dg.Fail():
        garbage2.append(t)

for gb in garbage2:
    #print gb
    col.pop(gb)
    #print len(col)

#print len(garbage2)

#print s - (len(garbage1) + len(garbage2))
#print len(col)

for t in col.keys():
    dg = digest(pa=col[t])
    if dg.NotExp():
        garbage3.append(t)

for gb in garbage3:
    #print gb
    col.pop(gb)
    #print len(col)

#print len(garbage3)

#print s - (len(garbage1) + len(garbage2) +len(garbage3))
#print len(col)


for t in col.keys():
    dg = digest(pa=col[t])
    if dg.Ret():
        garbage4.append(t)

for gb in garbage4:
    #print gb
    col.pop(gb)
    #print len(col)

#print s - (len(garbage1) + len(garbage2) +len(garbage3) +len(garbage4))
#print len(col)

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

import string
import random
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



for w in ng:
    #print w[0]
    if w[2] == '':
        continue
    dst = w[2].split('\n')[0]
    cha = ':!-+0123456789{}()\',. <>'
    for cc in cha:
        dst = dst.replace(cc,'_')
    rdst = os.getcwd()
    dst += id_generator(size=6)
    rdst += '\\distil\\' + dst
    try:
        shutil.copytree(w[0], rdst, symlinks=False, ignore=None)
    except:
        rdst = os.getcwd()
        rdst += '\\distil\\' + id_generator(size=8)
        shutil.copytree(w[0], rdst, symlinks=False, ignore=None)
    #print w[1]
    #print w[2]
    #d = raw_input('.')

#

#for t in col.keys():
#    dg = digest(pa=col[t])
#    if dg.RaisEx():
#        dst = id_generator(size=24)+id_generator(size=7)
#        kdst = os.getcwd()
#        kdst += '\\rexp\\' + dst 
#        shutil.copytree(t, kdst, symlinks=False, ignore=None)

try:
    shutil.rmtree(sys.argv[-1], ignore_errors=True, onerror=None)
except:pass

try:
    os.system('mkdir '+sys.argv[-1])
except:pass





