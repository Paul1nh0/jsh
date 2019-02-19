
import os, sys, threading
import shutil, string, random, time

import subprocess as s
from subprocess import Popen
from subprocess import STDOUT, check_output
import os, glob

class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None
        self.res = ''

    def run(self, timeout=30):
        def target():
            #print 'Thread started'
            self.process = s.Popen(self.cmd, stdin = s.PIPE,stdout = s.PIPE , stderr=s.PIPE)
            #self.process.communicate()
            (stdout, stderr) = self.process.communicate()
            time.sleep(30)
            o =  stdout
            er = stderr
            #ps.kill()
            self.res = str(o)+'\n'+str(er)
            #print 'Thread finished'

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(30)
        if thread.is_alive():
            print 'Terminating process'
            self.process.terminate()
            thread.join()
        return self.res
    
import subprocess
from threading import Timer

def run(cmd, timeout_sec):
    stdout,stderr = '', ''
    proc = subprocess.Popen(cmd, stdin = s.PIPE,stdout = s.PIPE , stderr=s.PIPE)
    kill_proc = lambda p: p.kill()
    timer = Timer(timeout_sec, kill_proc, [proc])
    try:
        timer.start()
        stdout,stderr = proc.communicate()
    finally:
        timer.cancel()
    return stdout,stderr
    

def log_crash(cmd, f):
        ps = Popen(cmd, stdin = s.PIPE,stdout = s.PIPE , stderr=s.PIPE)
        stdout, stderr = ps.communicate()
        o =  stdout
        er = stderr
        #ps.kill()
        #command = Command(cmd)
        #res = command.run(timeout=30)
        with open(f, 'w') as log:
                log.write(str(o)+'\n'+str(er))
        print 'crash log writen to '+f

while 1:
    for i in range(100):
        os.system('mkdir C:\\Users\\akayn\\desktop\\automation\\SC\\curpus\\'+str(i))
        os.chdir('C:\\Users\\akayn\\Desktop\\automation\\SC\\mDomato\\jscript')
        os.system('python generator.py --output_dir C:\\Users\\akayn\\Desktop\\automation\\SC\\curpus\\'+str(i)+' --no_of_files 1 --js_sh 1')
        os.chdir('C:\\Users\\akayn\\desktop\\automation\\SC')
        log_crash('python runner.py '+sys.argv[-1]+' C:\\Users\\akayn\\desktop\\automation\\SC\\curpus\\'+str(i)+'\\fuzz-0.js',
                  'C:\\Users\\akayn\\desktop\\automation\\SC\\curpus\\'+str(i)+'\\log.txt')
        os.system('taskkill /im '+sys.argv[-1]+' /f')
    time.sleep(30)
    os.system('python dist.py '+os.getcwd()+'\\curpus')