# Msrc Case: 41548 CRM:0001020892 Microsoft Edge multiple race conditions leading to rce.

So it all started with ivan fratric project zero <html><a href="https://googleprojectzero.blogspot.co.il/2017/09/the-great-dom-fuzz-off-of-2017.html">blog post and the new open source fuzzer-DOMATO.</a></html>. i have read the post and decided to try and experiment a little with fuzzing this browser.<br> it didnt take long for me to realize that menuel fuzzing will be too much of a pain and i began to write my own harness, in addition i made some changes and added extra api's to the fuzzer in order to get a little heads-up on the big amount of people who are currently running the fuzzer (i only had one machine).<br>
anyone who had ever fuzzed edge knows that there are a big amount of un-exploitable bugs in edge that can make the fuzzing work very difficult, one has to capture the debug output but to filter out those, it seems as if microsoft has no intention to fix any of those bugs. (a list will be given at the end of this article of about 500 dos conditions that go from division by zero to mem-gc protected uaf's).<br>
but, maybe to reader suprise, the difficult part was not coding the harness and overcoming the recent changes to edge ( Edge has become a full Universal Windows Platform (UWP) App. This means that the main Edge process no longer spawns any of the sandboxed child processes directly, but that all processes are spawned by the UWP framework.) that makes fuzzing this program to a somewhat challenging task, the most difficult part of this bug hunting quest was contacting msrc. i will try to add as little description as i possibly can to not sound like i got any opinion on the issue (although it will be a little difficult).

it was not long before i came across some intersting crash's, but none of them seemed to have any security context, and all this time i was thinking that maybe ivan released this too fast. another one of my thoughts was, maybe he simply gave up contacting msrc, seeing posts like this <html> <a href="https://bugs.chromium.org/p/project-zero/issues/detail?id=1237&can=1&q=&start=1000">one</a></html>.

well, i was about to give up, and have stoped my harness. this was the first day stable rs3 was out and i have upgraded my computer. it was also the time of this <html> <a href="https://twitter.com/dwizzzleMSFT/status/920637599449939968">public relations post</a></html> was out. and i decided to give one last longshot to the fuzzer. after running the automation during the night i have noticed one weird crash it looked as if edgehtml was trying to get a length of a url-string from a bogus address way too high to have any meaning. it didnt look exploitable at first but i thought i'd submit this anyway to msrc.