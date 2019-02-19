# JSF
a collection of javascript fuzzers and harness.
this is mostly implemented for automating windows, but there is unix support.
i used:
 1) a modified ver of @ifratric domato (that is licensed).
 2) a modified ver of @mozillasecurity dharma (that is licensed).
 3) some of my own costum generators & mutators.
 
# This Project is not maintained!
# I Will Not answer any issues, or write a proper usage wiki.
# I am only open sourcing this for the community benefit.

why didn't i use bugid?
  because this runs faster (less actions and analysis), and i didnt have much resources.
  its very easy to see that a crash is not exploitable (null ptr assertion etc) directlly from asseambly..


This is very straightforward:

install windbg..
install vs runtime from ms..
change the default web browser for the system to your own..
change all the directory paths to point to your own (i know its annoying..).
install https://github.com/giampaolo/psutil
additionally (on windows)-> extract psutil (downloaded from above link^^) to the automation\sc 
 (or automation\msedge, whatever your running..)

download this repo.

go to the automation directory.

choose sc//msedge
open some cmd's.

sc->javascript fuzzer for shels (see the --use_js_sh=1 argument and other modifications).
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
   
   ^^ adjust killer in a similar manner..
   ^^ adjust runner.bat (e.g change the code..)
   
   
to view results:

python dspl.py.

and open crash.log.txt and look for interesting crash's

have fun ..


# Note:
moz's dharma and ifratic's domato are licanced..
