
import os, sys
import shutil, string, random

import subprocess as s
from subprocess import Popen 
import os, glob

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
        

cCount = 0
BackT = os.getcwd()

def log_crash(cmd, f):
        ps = Popen(cmd, stdin = s.PIPE,stdout = s.PIPE , stderr=s.PIPE)
        (stdout, stderr) = ps.communicate()
        p_status = ps.wait()
        o =  stdout
        er = stderr
        with open(f, 'w') as log:
                log.write(str(o)+'\n'+str(er))
        print 'crash log writen to '+f

def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

def mainLoop():
        global cCount
        global cmdline
        global curpus
        global logp
        for i in range(10):
                print('\n\n\n ============  test'+str(i)+' =======================\n\n\n')
                exitCode = os.system(cmdline+" "+curpus+"\\test"+str(i)+".js")
                print('=========================================================')
                if not (exitCode==0):
                        cCount += 1
                        if ( 4 <= cCount):
                                return 'dup'
                        print 'we have seen  crash!'
                        idl = id_generator()
                        shutil.copy2(curpus+"\\test"+str(i)+".js", logp+idl+'.js')
                        print('crash sample was writen to C:\\Users\\akayn\\Desktop\\test\\crash\\'+idl+'.js')
                        log_crash(cmdline+" "+curpus+"\\test"+str(i)+".js",logp+idl+'.txt')
                else: cCount -= 1
        return 'done'

def operate():
        global cCount
        global binpath
        global curpus
        cCount = 0
        while True:
                try:
                        os.chdir(BackT)
                except: pass
                for Sample in glob.glob(curpus+"\\*.js"):
                        os.remove(Sample)
                print 'Mutating And Writing New Samples .. \n\n'
                os.system('python mutate.py')
                os.system('python gen.py 10')
                os.chdir(binpath)
                bRet = mainLoop()
                

if __name__ == "__main__":
        operate()







                
