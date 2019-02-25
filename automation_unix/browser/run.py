
import os, sys, threading
import shutil, string, random, time

import subprocess as s
from subprocess import Popen
from subprocess import STDOUT, check_output
import glob

dir_ = os.path.abspath(os.getcwd())

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
    proc = subprocess.Popen(cmd.split(' '), shell=True, stdin = s.PIPE,stdout = s.PIPE , stderr=s.PIPE)
    kill_proc = lambda p: p.kill()
    timer = Timer(timeout_sec, kill_proc, [proc])
    try:
        timer.start()
        stdout,stderr = proc.communicate()
    finally:
        timer.cancel()
    return stdout,stderr

def log_crash(cmd,i):
    log = open(os.path.abspath(dir_+'/curpus/'+str(i)+'/log.txt'), 'a')
    log.write('header\n')
    log.flush()
    popen = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE, stderr=log, universal_newlines=True, preexec_fn=os.setsid)
    for stdout_line in iter(popen.stdout.readline, ""):
            #print stdout_line
            log.write(str(stdout_line))
            yield stdout_line
    

    return_code = popen.wait()



        

import platform


while 1:

    for i in range(100):
        os.system('killall '+sys.argv[-2])
        os.system('mkdir '+dir_+'/curpus/'+str(i))
        os.chdir(dir_+'/mDomato')
        os.system('python generator.py --output_dir '+dir_+'/curpus/'+str(i)+' --no_of_files 15')
        os.chdir(sys.argv[-1])
        
        if 'Dar' in platform.system():
            if sys.argv[-2] == 'Chromium':
                
                # this works..
                for i in log_crash('./'+sys.argv[-2]+'.app/Contents/MacOS/Chromium --no-sandbox '+os.path.abspath(dir_+'/curpus/'+str(i)+'/fuzz-1.html'),i):pass
            
            else:
                
                # this might not ..
                for i in log_crash('./'+sys.argv[-2]+'.app/Contents/MacOS/'+sys.argv[-2]+' '+os.path.abspath(dir_+'/curpus/'+str(i)+'/fuzz-1.html'),i):pass
        else:
            # we skip the first one because it contains the 'nothing' loop and
            # thats not interesting on unix like systems because of asan usage ..
            for i in log_crash('./'+sys.argv[-2]+' '+os.path.abspath(dir_+'/curpus/'+str(i)+'/fuzz-1.html'),i):pass
            
        os.chdir(dir_)
    
    time.sleep(30)
    os.system('python dist.py '+dir_+'/curpus')
        
 
