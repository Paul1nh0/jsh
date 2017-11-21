import os, sys, random
import re
import struct

dbg = False

cmdline = ''
path = ''
curpus = ''
logp = ''
with open(os.getcwd()+'\\config.txt', 'r') as conf:
    tr = conf.read()
    hi = tr.split('\n')
    for i in hi:
        if 'BINPATH' in i:
            binpath=i.split('=')[1]
        elif 'BINCMDLINE' in i:
            cmdline=i.split('=')[1]
        elif 'LOG' in i:
            logp=i.split('=')[1]
        elif 'CURPUS' in i:
            curpus=i.split('=')[1]

text = ''
H = 0

flags = {
    'all':'--allow-natives-syntax'
}

ty = {
    'fn':'fn',
    'var':'var',
    'arr':'arr',
    'proxy':'proxy',
}

fn = {
    'apply' : '///b.apply()',
    'call()' : '///a().call()',
    'def' : 'function() { return ///b; }',
    'defgen': '(x for (x in []))',
    'defyld':'function(///a) { yield ///a; }',
    'eval': 'function(///a) { eval(///a);}',
    #'gc': 'try{gc();}catch(e){}',
    'hasOwnProperty':'(///a).hasOwnProperty("///b");',
    '__lookupGetter__':'///b.__lookupGetter__("///c")',
    '__lookupSetter__':'///c.__lookupSetter__("///b")',
    'new': 'new Function()',
    'pow': 'Math.pow(///a,///b)',
    'map':'///c.map(///b)',
    'print':'print(///a);',
    'replace':'///a.replace("///b","///c");',
    'slice':'///c.slice(1,2)',
    'split':'///c.toString().split("///b")',
    'split':'///c.split("///b")',
    'fromCharCode':'///a.fromCharCode(///b)',
    'valueOf':'///a.valueOf(///b)',
    'constructor':'(function* () { }).constructor()',
    'delete':'delete ///a.prototype;',
    'assign':'///c;',
    'isNaN':'isNaN',
    'assignLet:':'b; let b = [{///b: ///a}, ///c];',
    'loopLet':'///a.forEach(obj =///c; {}',
    'repeat':'///b.repeat(0xFFFFFC)',
    'fill':'///b.fill(0xFFFFFC)',
    'plus':'///b + ///c',
    'setProto':'///b.setPrototypeOf()',
    'isExt':'///b.isExtensible()',
    'has':'///b.has()',
    'getOwnProp':'///b.getOwnPropertyDescriptor()',
    'ownK':'///b.ownKeys()',
    'Se':'///b.set()',
    'delp':'///b.deleteProperty()'
}

arr = {
    'ArrayBuffer':'new ArrayBuffer(///a);',
    'Uint32Array':'new Uint32Array(///b)',
    'Uint32Array9':'new Uint32Array()',
    'Arr':'new Array();'
}

asm = {
    'decl':'"use asm";',
}

proxy = {
    #'p1':'new Proxy(target, { get: (target, name, receiver) => { return target[name];}); target = 0xFFFFFFF; try{f.property = "value";console.log(f.property)}catch(e){}',
    'p2':'f.apply(); const handler///g = { get: (target, name, receiver) => {const p = this;return target[name];}; f = new Proxy(handler///g,this);',
    'const':'f.apply();const target///g = { ///c }; const handler///g = { ///b }; const f = new Proxy(target///g, handler///g);',
    'arrow':'new Proxy(() => {}, {});',
    'class':'f.apply(); Class = {///b}; const f = new Proxy(Class, {});',
    'object' :'f();const f =  new Proxy({}, {});}',
    'deref': 'function(foo = function(){///b}) {///c}',
    #'deref2':'try {  function foo() =///b;var b = foo(); b();}catch(e){}',
    'thisdef':'this.__defineSetter__("x", function(){});',
}


prop = {
    'byteLength':'.__defineGetter__("byteLength", function() { return 0xFFFFFFFC; });',
}

ops = {
    'loop':'for (var i=0;i<=0x1000;++i){///b += ///c;}',
   'break':'break;',
    'case':'case ///a:',
    'export':'export ///a:',
    'opt':'if (obj.hasOwnProperty("///b")) {console.log(obj["///c"]);}',
}

misc = {
    'roll':'<<<',
}

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

keyWords = {
    'semi':';',
    ',':',',
    'super':'super',
    'switch':'switch',
    'throw':'throw -1;',
    'with':'with',
}

cnt = ''
with open(os.getcwd()+'\\mutation\\formula.txt', 'r') as foo:
    cnt = str(foo.read())
    proxy['spec'] = cnt

class LineWriter:
    def __init__(self,t=0):
        self._t = t

    def gen(self):
        for i in range(5):
            tag = random.choice(ty.keys())
            elem = eval(tag) #[random.choice(eval(tag.keys()))
            #print elem, type(tag)
            e = dict(elem)
            #print e, type(e)
            #print '\n\n\n'
            a = e[random.choice(e.keys())]
            #print a, type(a)
            #print '\n\n\n'
            line = 'try { eval(\'var'+str(self._t)+' = '+ a + '\')}catch(e){yyy+=1}'
            #if ((self._t%50)==0):
                #line += 'try {'+ops[random.choice(ops.keys())]+'}catch(e){}'
            line = line.replace('///a', var[random.choice(var.keys())])
            if 5 <= self._t:
                if (self._t%2):
                    line = line.replace('///b', 'var'+str(random.randint(0, self._t+1)))
                else:
                    if (self._t%3):
                        line = line.replace('///b', 'var'+str(random.randint(0, self._t+1))+'()')
                    else:
                        line = line.replace('///b', 'var'+str(random.randint(0, self._t+1))+'.apply()')
            else:
                line = line.replace('///b', var[random.choice(var.keys())])
            if '///a' in line:
                if 5 <= self._t:
                    line = line.replace('///a', 'var'+str(random.randint(0, self._t+1)))
                else:
                    line = line.replace('///a', var[random.choice(var.keys())])
            if '///c' in line:
                if 5 <= self._t:
                    line = line.replace('///c', 'var'+str(random.randint(0, self._t+1)))
                else:
                    line = line.replace('///c', var[random.choice(var.keys())])
            if '///g' in line: line = line.replace('///g', str(self._t))
            #print line
            global text
            text += line+'\n'
            self._t += 1
            #ooo = raw_input('l')
            


for u in range(int(sys.argv[-1])):
    lw = LineWriter()
    text += 'var yyy = 0;\n'
    for i in range(2000):
        lw.gen()
    text += 'console.log("----------------------------------------------------No Of Syntax Errors:----------------------------------------------");\n'
    text += 'console.log(yyy);\n'
    text += 'console.log("----------------------------------------------------------------------------------------------------------------------");\n'
    with open(curpus+'\\test'+str(H)+'.js','a+') as ab:
                ab.write(text)
    text = ''
    H += 1
    print 'wrote test'+str(u)+'.js to directory ..'


#mod = os.getcwd()
#p = sys.platform
#
#if ('win' in p):
#    mod += '\\tc\\modules'
#else:
#    mod += '/tc/modules'
#if dbg: print mod + '\n\n\n'


