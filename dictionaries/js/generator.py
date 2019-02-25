#   WeirDOM - main generator script
#   -------------------------------
#
#   Written and maintained by Ivan Fratric <ifratric@google.com>
#
#   Copyright 2017 Google Inc. All Rights Reserved.
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


from __future__ import print_function
import os
import re
import random
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
from grammar import Grammar

_N_MAIN_LINES = 120
_N_EVENTHANDLER_LINES = 60

def generate_function_body(jsgrammar, num_lines, special=0):
    ab = ['a','b']
    if special==0:
        js = ''
        js += '//beginjs\n'
        js += jsgrammar._generate_code(num_lines)
        js += '\n//endjs\n'
        #js += 'CollectGarbage();\n'
        if random.random() < 0.1:
          js += 'return vars[' + str(random.randint(0,99)) + '];\n'
        else:
          js += 'return vars[' + str(random.randint(0,99)) + '];\n'
        return js
    elif special==1:
        js = ''
        rnd = random.randint(0,1)
        js += jsgrammar._generate_code(num_lines).replace('vars',ab[rnd]) + '\n'
        if rnd == 0:
            js = js.replace('ret',ab[1])
        else:
            js = js.replace('ret',ab[0])
        d = random.randint(0,4)
        if (d!=0):
            #js = js.split('[')[0] + js.split(']')
            pass
        js += 'return ' + ab[random.randint(0,1)] + ';\n'
        js = js.replace('aurn ','return ')
        js = js.replace('burn ', 'return ')
        return js
    elif special==2:
        jitted = ['a = a|0;return a;',
                  'b = b|0;return b;','a = (a - 1)|0; return ++b;']
        js = ''
        rnd = random.randint(0,len(jitted)-1)
        js += jitted[rnd] + '\n'
        return js
    elif special==3:
        js = ''
        fint = ['100','1000','0x7ffc5','0x400']
        rnd = random.randint(0,len(fint)-1)
        js += fint[rnd] + ' '
        return js
    elif special==4:
        js = ''
        js1 = ''
        js2 = ''
        rnd = random.randint(0,1)
        rnd2 = 0
        if rnd == 0:
            rnd2 = 1
        js1 += jsgrammar._generate_code(num_lines).replace('vars',ab[rnd]) + '\n'
        if rnd == 0:
            js1 = js1.replace('ret',ab[1])
        else:
            js1 = js1.replace('ret',ab[0])
        js2 += jsgrammar._generate_code(num_lines).replace('vars',ab[rnd2]) + '\n'
        if rnd == 0:
            js2 = js2.replace('ret',ab[1])
        else:
            js2 = js2.replace('ret',ab[0])
        d = random.randint(0,4)
        if (d!=0):
            #js = js.split('[')[0] + js.split(']')
            pass
        js = js1+js2
        js = js.replace('aurn ','return ')
        js = js.replace('burn ', 'return ')
        return js

def GenerateNewSample(template, jsgrammar, fi=''):
    """Parses grammar rules from string.

    Args:
      template: A template string.
      htmlgrammar: Grammar for generating HTML code.
      cssgrammar: Grammar for generating CSS code.
      jsgrammar: Grammar for generating JS code.

    Returns:
      A string containing sample data.
    """

    result = template

    handlers = False
    while '<jsfuzzer>' in result:
        numlines = _N_MAIN_LINES
        if handlers:
            numlines = _N_EVENTHANDLER_LINES
        else:
            handlers = True
        result = result.replace(
            '<jsfuzzer>',
            generate_function_body(jsgrammar, numlines),
            1
        )

    while '<fff>' in result:
        result = result.replace(
            '<fff>',
            generate_function_body(jsgrammar, 1, special=1),
            1
        )
    while '<ffh>' in result:
        result = result.replace(
            '<ffh>',
            generate_function_body(jsgrammar, 1, special=4),
            1
        )

    while '<asm>' in result:
        result = result.replace(
            '<asm>',
            generate_function_body(jsgrammar, 1, special=2),
            1
        ) #

    while '<randint>' in result:
        result = result.replace(
            '<randint>',
            generate_function_body(jsgrammar, 1, special=3),
            1
        )

    result = result.replace('&&&&&&&',fi)

    return result


def generate_samples(grammar_dir, outfiles, _js_=0):
    """Generates a set of samples and writes them to the output files.

    Args:
      grammar_dir: directory to load grammar files from.
      outfiles: A list of output filenames.
    """

    if _js_ == 0:
        f = open(os.path.join(grammar_dir, 'template.html'))
    elif _js_ == 1:
        f = open(os.path.join(grammar_dir, 'template.js'))
    template = f.read()
    f.close()

    jsgrammar = Grammar()
    err = jsgrammar.parse_from_file(os.path.join(grammar_dir, 'jscript.txt'))
    if err > 0:
        print('There were errors parsing grammar')
        return

    ttt = 0

    for outfile in outfiles:

        if _js_ == 0:
            uf = outfile.replace('\\','/')
            uf = uf.replace(str(ttt),str(ttt+1))
            ttt += 1
        elif _js_ == 1:
            uf = ''
            outfile = outfile.replace('.html','.js')
        
        result = GenerateNewSample(template, jsgrammar, fi=uf)

        if result is not None:
            print('Writing a sample to ' + outfile)
            try:
                f = open(outfile, 'w')
                f.write(result)
                f.close()
            except IOError:
                print('Error writing to output')


def get_option(option_name):
    for i in range(len(sys.argv)):
        if (sys.argv[i] == option_name) and ((i + 1) < len(sys.argv)):
            return sys.argv[i + 1]
        elif sys.argv[i].startswith(option_name + '='):
            return sys.argv[i][len(option_name) + 1:]
    return None


def main():
    global _N_MAIN_LINES
    global _N_EVENTHANDLER_LINES
    fuzzer_dir = os.path.dirname(__file__)

    multiple_samples = False

    for a in sys.argv:
        if a.startswith('--output_dir='):
            multiple_samples = True
    if '--output_dir' in sys.argv:
        multiple_samples = True

    if multiple_samples:
        #print('Running on ClusterFuzz')
        out_dir = get_option('--output_dir')
        nsamples = int(get_option('--no_of_files'))
        jsshell = int(get_option('--js_sh'))
        if jsshell==1:
            _N_MAIN_LINES = 100
            _N_EVENTHANDLER_LINES = 50
        print('Output directory: ' + out_dir)
        print('Number of samples: ' + str(nsamples))

        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        outfiles = []
        for i in range(nsamples):
            outfiles.append(os.path.join(out_dir, 'fuzz-' + str(i) + '.html'))

        generate_samples(fuzzer_dir, outfiles, _js_=jsshell)

    elif len(sys.argv) > 1:
        outfile = sys.argv[1]
        generate_samples(fuzzer_dir, [outfile])

    else:
        print('Arguments missing')
        print("Usage:")
        print("\tpython generator.py <output file>")
        print("\tpython generator.py --output_dir <output directory> --no_of_files <number of output files>")

if __name__ == '__main__':
    main()
