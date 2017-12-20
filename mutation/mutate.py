import os, sys, random
import re
import struct

import shutil, string

import subprocess as s
from subprocess import Popen 
import os, glob

dbg = False

cmdline = ''
binpath = ''
with open(os.getcwd()+'\\config.txt', 'r') as conf:
    tr = conf.read()
    hi = tr.split('\n')
    for i in hi:
        if 'BINPATH' in i:
            binpath=i.split('=')[1]
        elif 'BINCMDLINE' in i:
            cmdline=i.split('=')[1]
    

BackT = os.getcwd()

var = {
    'false':'false',
    'true':'true',
    'null':'null',
    'this':'this',
    '{}':'{}',
    'dot':'///b.///c',
    'fl':'666905.4448493933333333333',
    'bi':'0xFFFFFFFFC',
    'bs':'0x20',
    'undefined':'undefined',
    #'void':'void;',
    'unicode':'"\u0001"',
    'string':'"AAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBBBBBBBBBBBBBCCCCCCCCCCCCCCCCCCDDDDDDDDDDDDDDDDDDDDDDDDDDDD"',
    'string1':'"a"',
    'string3':'"onot87gmv==-"'
}

ty = {
    'arr':'arr',
    'cond':'cond',
    'obj':'obj',
    'func':'func',
}

arr = {
    'ArrayBuffer':'a1 = new ArrayBuffer(///a);',
    'Uint32Array':'a2 = new Uint32Array(///b);',
    'Uint32Array9':'a1 = new Uint32Array();',
    'Arr':'a2 = new Array();',
    'Li':'a3 = [];'
}

cond = {
    'if1':'if (a1.hasOwnProperty("///b"))',
    'if1':'if (///c)',
    'if1':'if (a2*a1)',
    'if1':'if (a2+a1)',
    'if1':'if (a2-a1)',
    'if1':'if (a2==a1)',
    'if1':'if (a2<=a1)',
    'if1':'if (a2>a1)',
    'if1':'if (///c >>> ///b)',
    'if1':'if (///c <<< ///b)',
}

obj = {
    'obj':'var ttt = {}',
    'obj2':'a1 : {},',
    'obj3':'///b : {},',
    'objM':'Object.toString(a2.a1)',
    'objM5':'Object.toString(///c)'
}

func = {
    'arrow':'new Proxy(() => {}, {});',
    'class':'f.apply(); Class = {///b}; const f = new Proxy(Class, {});',
    'object' :'f(); f =  new Proxy({}, {});}',
    'thisdef':'this.__defineSetter__("x", function(){});',
    'byteLength':'///a.__defineGetter__("byteLength", function() { return 0xFFFFFFFC; });',
    'loop':'for (var i=0;i<=0x1000;++i){a1 += ///c;}',
    'opt':'if (obj.hasOwnProperty("///b")) {console.log(obj["///c"]);}',
    'super':'///b = super;',
    'dotThis':'a1 = this.///b;',
    'dotThis':'a1.a2;',
    'retThis':'return this;',
    'ret':'return a1;',
    'ret2':'return a2',
    'ret3':'return a2 - a1;',
    'ret4':'return this.a1;',
    'ret5':'return this.a1.a2;',
    'ret Func':'return y;',
    'retRec':'return Rec;'
}

rec = {
    'r1':'rec(a1, a2);',
    'r2':'rec(a1, a2 + ///a);',
    'r2':'rec(a1, a2 + ///b);',
    'r2':'rec(a1, a2 + ///c);',
    'r2':'rec(a1, a2 >>> ///a);',
    'rs1':'rec(a1, a2)',
    'rs2':'rec(a1, a2 + ///a),',
    'rs2':'rec(a1, a2 + ///b),',
    'rs2':'rec(a1, a2 + ///c),',
    'rs2':'rec(a1, a2 >>> ///a),',
    'rd':'',
}

Sub = []
S = ''
with open(os.getcwd()+'\\mutation\\candidate.txt', 'r') as foo:
    S = str(foo.read())
    Sub = S.split('$$')

with open(os.getcwd()+'\\mutation\\LastOne.txt', 'w') as fi:
    fi.write(S)

if dbg:
    for t in Sub: print t
    print '\n\n\n'

def log_rez(cmd):
        ps = Popen(cmd, stdin = s.PIPE,stdout = s.PIPE , stderr=s.PIPE)
        (stdout, stderr) = ps.communicate()
        p_status = ps.wait()
        o =  stdout
        er = stderr
        if dbg:
            print o
            print er
            print 
        if ('INVALID SYNTAX' in o) or ('INVALID SYNTAX' in er):
            return False
        return True

class LineWriter:
    def __init__(self,t=0):
        self._t = t

    def gen(self):
        global Sub
        global cmdline
        global binpath
        fs = False
        jc = ''
        ind = 0
        while not fs:
            jc = Sub[random.randint(1,len(Sub)-1)]
            if ('b' not in jc) and ('///b' not in jc)\
                and ('a1' not in jc) and ('a2' not in jc)\
                    and ('///c' not in jc) or ('go' in jc):
                        continue
            else:
                ind = Sub.index(jc)
                fs = True
        if 'if' in jc:
            tag = random.choice(cond.keys())
            a = cond[str(tag)]
        elif 'rec' in jc:
            tag = random.choice(['rec','obj'])
            e = eval(tag)
            d = dict(e)
            t = random.choice(d.keys())
            a = d[str(t)]
        else:
            tag = random.choice(['rec','obj','func','arr'])
            e = eval(tag)
            d = dict(e)
            t = random.choice(d.keys())
            a = d[str(t)]
        if dbg:
            print jc
            print a
            print
        num = random.randint(0,100)
        if (num%2) or ('if' in jc):
            m1 = [Sub[x] for x in range(ind)] + [a] + [Sub[x] for x in range(ind+1,len(Sub))]
        else:
            m1 = [Sub[x] for x in range(ind)] + [a] + [Sub[x] for x in range(ind,len(Sub))]
        end = ''
        for y in m1:end += y + ' ' 
        #print end
        #rd = raw_input(' ..')
        tst = ''
        b = 0
        while b < 5:
                b += 1
                tst = end.replace('///b', var[random.choice(var.keys())])
                tst = tst.replace('///c', var[random.choice(var.keys())])
                tst = tst.replace('///a', var[random.choice(var.keys())])
                testFunc = "try { eval('var g = "+tst+"');}catch(e){console.log('INVALID SYNTAX')}"
                print
                print testFunc
                print
                with open(os.getcwd()+"\\mutation\\temp.js", 'w') as tmp:
                    tmp.write(testFunc)
                os.chdir(binpath)
                boo = log_rez(cmdline+" "+os.getcwd()+"\\mutation\\temp.js")
                if boo:
                    b = 10000
                    if dbg:print('found a different valid formula, done ..')
                    return m1
                else:
                    if dbg:print('invalid, rotating formula ..')
        os.chdir(BackT)
        return ''
                
        
su = LineWriter()
g = ''
while (g==''):
    g = su.gen()



os.chdir(BackT)
with open(os.getcwd()+'\\mutation\\candidate.txt', 'w') as fnt:
    ln = ''
    for gg in range(len(g)):
        if gg != len(g)-1:
            ln += g[gg] + '$$'
        else:
            ln += g[gg]
    fnt.write(ln)

with open(os.getcwd()+'\\mutation\\formula.txt', 'w') as lm:
    ll = ''
    for gg in g:
        ll += gg + ''
    lm.write(ln)

print('found a different valid formula, done mutating sample..')
os.remove(os.getcwd()+'\\mutation\\temp.js')
