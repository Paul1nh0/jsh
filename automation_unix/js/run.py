import os, sys, threading
import shutil, string, random, time

import subprocess as s
from subprocess import Popen
from subprocess import STDOUT, check_output
import glob


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


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

class Runner:
    def __init__(self):
        self.rc = 0

    def log_crash(self,cmd,i):
        log = open(os.path.abspath(dir_+'/curpus/'+str(i)+'/log.txt'), 'a')
        log.write('header\n')
        log.flush()
        popen = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE, stderr=log, universal_newlines=True, preexec_fn=os.setsid)
        for stdout_line in iter(popen.stdout.readline, ""):
            #print stdout_line
            log.write(str(stdout_line))
            yield stdout_line

        
        return_code = popen.wait()
        self.rc = return_code
        log.close()
            
            
    def get_rc(self):
        return self.rc






import platform


while 1:

    for i in range(100):
        os.system('killall '+sys.argv[-2])
        os.system('mkdir '+dir_+'/curpus/'+str(i))
        os.chdir(dir_+'/mDomato/jscript')
        os.system('python generator.py --output_dir '+dir_+'/curpus/'+str(i)+' --no_of_files 1 --js_sh 1')
        os.chdir(sys.argv[-1])
        
        thread = Runner()
        
        if 'Dar' in platform.system():
            for i in thread.log_crash('./'+sys.argv[-2]+' '+os.path.abspath(dir_+'/curpus/'+str(i)+'/fuzz-0.js'),i):pass
            if (thread.get_rc() != 0) and (thread.get_rc() > 0):
                with open(os.path.abspath(dir_+'/curpus/'+str(i)+'/log.txt'),'a') as l:
                    l.write(id_generator(size=6))
        else:
            
            # we use a goddamn generator so we actually wait for output ..
            for i in thread.log_crash('./'+sys.argv[-2]+' '+os.path.abspath(dir_+'/curpus/'+str(i)+'/fuzz-0.js'),i):pass
            
            # maybe asan didnt output but the process exit with error? (on unix like systems if the thread were killed
            # then the return_code from subprocess would be negative, so we check that..)
            # if its true then we mark the file as a crashing sample by inserting some random bullshit to the file (because the cleaner
            # would see this as an error ..).
            if (thread.get_rc() != 0) and (thread.get_rc() > 0):
                with open(os.path.abspath(dir_+'/curpus/'+str(i)+'/log.txt'),'a') as l:
                    l.write(id_generator(size=6))
        
        os.chdir(dir_)
    
    time.sleep(30)
    os.system('python dist.py '+dir_+'/curpus')


