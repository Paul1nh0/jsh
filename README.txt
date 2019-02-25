# This Project is NOT maintained!
# I Will Not answer any issues, or write a proper usage wiki.
# I am only open sourcing this for the community benefit.


# JSH - A JavaScript Fuzzing Harness.
# provided here are examples of usage with 
      domato (a modified version of the first release..) & dharma (both licensed [provided here]),
# but you can run any generator with this setup.
# as per my usage this was very stable and fast.

a collection of javascript fuzzers and harness.
this is mostly implemented for automating windows, but you can change the files needed to the setup under
  the /mutation directory in this repo to support unix.
      (or download jsf64linux.zip from bin directory->
              you would have to make some changes for this to work but its provided as
              a general guidance)
              
in this setup:
 1) a modified ver of @ifratric domato (that is licensed [provided here]).
 2) a modified ver of @mozillasecurity dharma (that is licensed [provided here]).
 3) some of my own costum generators & mutators.
 4) makes use of psutil python module (that is licensed [not provided here]).


why didn't i use bugid?
  because this runs faster (less actions and analysis), and i didnt have much resources.
  its very easy to see that a crash is not exploitable (null ptr assertion etc) directlly from asseambly..


usage:

    recommended: disable windows defender anti-virus, for better performance.
    Run Only inside a virtual machine!!
    ((more instructions are under /automation directory at this repo..))

install windbg..
install vs runtime from ms..
change the default web browser for the system to your own..
       you might have to change all the directory paths to point to your own (you might not..).
install https://github.com/giampaolo/psutil
additionally (on windows)-> extract psutil (downloaded from above link^^) to the automation\sc 
 (or automation\msedge, whatever your running..)

download this repo.

go to the automation directory.

choose sc//msedge
open some cmd's.

sc->javascript fuzzer for shells (see the --use_js_sh=1 argument and other modifications).
msedge->domato based harness that connects windbg and collects crash repro and asseambly log.
  (this is also good for ie, just change the default web browser and the runner.py)
 
change all the paths under automation directory to point to your working path!

read readme.txt (at automation) there for fuzzing.


you should be able to run: 
 
 
python killer.py

in another cmd:

python run.py

(if you run sc, e.g the js shell then run:
   python run.py C:\Users\akayn\Desktop\jssh\chakra\cc_windows_1_7_5\x64_release\ch.exe
   replace this full path with the full path of where you saved//compiled chakra or any other engine..)
   
   ^^ adjust killer.py cmdline in a similar manner..
   
   
to view results:

python dspl.py.

and open crash.log.txt and look for interesting crash's

every once in a while erase crash.log.txt
replace the content of crash.txt with this:
set([])
erase distil directory content ..

have fun

if you are dom fuzzing then the fuzzer would clean the output and save the reproducing cases and the windbg output to
the /maybe_exploitable directory.
the repro cases are saved as a pack of 15 files (0->14) so check every single one (by connecting a debugger
to the program and comparing the asseambly crashing instruction written at the log.txt to the output of the debugger).
the js shell fuzzing would not clean the crash cases because they are much more rare.
but you can clean the directory manually: python clean.py distil



# Note:
moz's dharma and ifratic's domato are Licensed (they are provided under the corresponding directorys)
^^ Modifications done by me are not part of there original code..

modifications that i remember:

  main changes to domato:
  
                a) changed the dictionary for dom fuzzing.
                
                b) created (from jscript.txt) a javascript compatible and more extended dictionary.
                
                c) the generator create's (for dom fuzzing) a set of 15 files (and adds javascript to 
                    navigate to all the files->so we wont have to launch the program so many times...)
                    
                d) the first file consume cpu time (by a js loop that do nothing),
                    so we can reliably connect a debugger to the right MicrosoftEdgeCp.exe (or ie) child process.
                    
                    
 if you use this setup then see that you keep the license provided with dharma & domato & psutil.
 my own code is not licensed and you can do whatever you like..
 
 also provided here:
 som e extra dictionary's including webgl
                
                
                
                
                
  



