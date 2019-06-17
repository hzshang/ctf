# TODO finish this file after writing my thesis

import tempfile
import os, sys, signal, logging
import subprocess

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)
signal.alarm(60)

def fetch_output():
    # TODO check compile result, and return it
    raise Exception('fetch output not implemented yet')


def main():
    print('========================================')
    print('| RUSCAS -- RUSt Compiler As A Service |')
    print('========================================')

    print('Please give me your Rust code! Ends with "[newline]EOF"')
    
    code = ''
    while True:
        line = input()
        if line == 'EOF':
            break
        else:
            code += line

    print('Compiling...')

    with tempfile.NamedTemporaryFile(mode='w+') as f:
        f.write(code)
        f.flush()
        bin_name = f.name + '.out'
        res = subprocess.run(
            'rustc -O {} -o {}'.format(f.name, bin_name).split(),
            stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL).returncode
        if res < 0:
            print('compile failed')
        else:
            print('Done!')
            try:
                fetch_output()
            except:
                os.system('rm {} 2> /dev/null'.format(bin_name))


if __name__ == '__main__':
    main()
