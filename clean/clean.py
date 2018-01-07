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

    def text(self):
        lines = ''
        with open(self.pa, mode='r') as raw_data:
            lines = raw_data.read()
        return str(lines)

    def getEx(self):
        text = self.text()
        if ('verifier!' in text):
            return 'vrf'
        if ('msvcrt!' in text):
            return 'ms'
        notZero = ['1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
        for ln in self.reader():
            if '?' in ln:
                if 'ds:' in ln:
                    d = ln.split('ds:')[1]
                    #print d
                    z = 0
                    sx = d.split('=')[0]
                    for x in range(len(sx)-3):
                        if sx[x] in notZero:
                            z += 1
                    #print z
                    #e = raw_input(' ..')
                    if 1 <= z:
                        return True
        return False

    def GetExpR(self):
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

    def GetExSig(self):
        pass


col = get_files(sys.argv[-1])

v = []
vr = []
rt = []

for t in col.keys():
    dg = digest(pa=col[t])
    ccc = dg.getEx()
    if (ccc == 'vrf'):
        vr.append([t, 'vrf_'+id_generator(size=6)])
        continue
    if (ccc == 'ms'):
        rt.append([t, 'ms_'+id_generator(size=6)])
    if (ccc == True):
        v.append([t, dg.GetExpR()])

#www = raw_input(' ..')

dupl = get_files(os.getcwd()+'\\v')
dpl = " ".join(dupl.keys())

numbers = []
ind = 0
for fi in v:
    exceptions = ['verifier!','msvcrt!']
    for e in exceptions:
        if e in fi[1]:
            ind += 1
            continue
    cha = ':!-+0123456789{}()\',. <>'
    zx = ''
    xz = ''
    xz = fi[1].split('\n')[0]
    if '+' in xz:
        zx =  xz.split('+')[0]
        for cc in cha:
            zx = zx.replace(cc,'_')
    if zx in dpl:
        numbers.append(ind)
    dpl += ' ' + zx
    ind += 1

#print numbers
#dddt = raw_input('STOPHERE')
Q = []

for i in range(len(v)):
    if i not in numbers:
        Q.append(v[i])

#print v

def finish(li):
    for w in li:
        if w[1] == '':
            continue
        dst = w[1].split('\n')[0]
        cha = ':!-+0123456789{}()\',. <>'
        for cc in cha:
            dst = dst.replace(cc,'_')
        rdst = os.getcwd()
        dst += id_generator(size=6)
        rdst += '\\v\\' + dst
        try:
            shutil.copytree(os.getcwd()+'\\'+w[0], rdst, symlinks=False, ignore=None)
            shutil.rmtree(os.getcwd()+'\\'+w[0])
        except:
            rdst = os.getcwd()
            rdst += '\\v\\' + id_generator(size=8)
            shutil.copytree(w[0], rdst, symlinks=False, ignore=None)
            shutil.rmtree(os.getcwd()+'\\'+w[0])


finish(Q)
finish(vr)
finish(rt)











