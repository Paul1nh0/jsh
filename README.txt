
      # jsh - A JavaScript Fuzzing Harness.
      ((and a collection of other useful resources))

      # This Project is NOT maintained!
      # I Will Not answer any issues, or write any proper usage wiki other then this readme file.
      # I am only open sourcing this for the community benefit.



# provided here are examples of usage with:

      * domato (a modified version of the first release..) & dharma (both licensed [provided here])
      
            ((but you can run any generator | mutator with this setup.))
      
      * some of my own costum generators, mutators & dictionaries.
      
# makes use of the psutil python module ((only on windows)) (that is licensed [not provided here]).

# as per my usage this was very stable and fast.

why didn't i use bugid or something from mozilla or some other open source stuff?

  * because i wanted something that would fit my needs..
  
  * because this runs faster (less actions and analysis), and i didnt have much resources.
  
  * its very easy to see that a crash is not exploitable (null ptr assertion etc) directlly from asseambly..
  

this was mostly implemented for automating windows ((i know its hard to believe..)), 
but linux (and macos) support is provided as well 
( under the /automation_unix directory ).


the /mutation directory is my own js mutator, its not documented but you can read the code to
modify it for your needs.

RUNNING:


<< MACOS >>
(exampled here chromium-asan):

      for any other web browser see the content of 'somebrowser.app' and adjust the 
      file run.py (where its commented..) to launch the application:
      
            on one terminal:

                  python run.py Chromium /fullpath/to/asan/directory

            on another:

                  python killer.py Chromium


     or for js:

            on one terminal:

                  python run.py d8 /fullpath/to/asan/directory

            on another:

                  python killer.py d8


<< linux >>
(exampled here chromium-asan):

            on one terminal:

                  python run.py chrome /fullpath/to/asan/directory

            on another:

                  python killer.py chrome

      or for js:

            on one terminal:

                  python run.py d8 /fullpath/to/asan/directory

            on another:

                  python killer.py d8
                  
                  


              
<< WINDOWS >>

    recommended: disable windows defender anti-virus, for better performance.
    Run Only inside a virtual machine!!
    
    ((more instructions are under /automation directory at this repo..))

      install windbg..
      
      install vs runtime from ms..
      
      change the default web browser for the system to your own..
      
      install https://github.com/giampaolo/psutil
      
      additionally (on windows)-> extract psutil (downloaded from above link^^) to the automation\sc 
       (or automation\msedge, whatever your running..)
       
      add python to the systems path..

      download this repo.

      go to the automation directory.

      choose sc | msedge
      
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
      
      


   
TO VIEW RESULTS:

           python dspl.py.

           and open crash.log.txt and look for interesting crash's

           every once in a while erase crash.log.txt
           
           replace the content of crash.txt with this:
           
           set([])

           erase distil directory content ..



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
                    
                    ((not used on MacOs and linux because of no windbg usage..))
                    
                e) patched domato generator script to handle macos file system better..
                    
                    
 if you use this setup then see that you keep the license provided with dharma & domato & psutil.
 my own code is not licensed and you can do whatever you like..
 
 also provided here:
 som e extra dictionary's including webgl
 
 
 HAVE FUN AND PROFIT!                
                
                
                
                
  



