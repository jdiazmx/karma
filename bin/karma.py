#!/usr/bin/env python3

project = 'Karma'
version = '10.02.19'
author  = 'decoxviii'

usage = """Karma
Usage:
    karma.py target <target> [-o FILENAME] [--proxy=<proxy>]
    karma.py search <target> (--password | --local-part | --domain) 
                             [-o FILENAME] [--proxy=<proxy>]
    karma.py (-h | --help)
    karma.py --version

Options:
    -o --output         Save output in json format.
    --proxy=<proxy>     Set Tor proxy [default: 127.0.0.1:9050].
    -h --help           Show this screen.
    --version           Show version.
"""

import sys
import json
import time
from os import path

try:
    from docopt import docopt
    
    sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), '..')))
    from karma import banner
    from karma import core
except Exception as e:
    print("Error:", e )
    print("Please install the requirements:\n\t$ pip3 install -r requirements.txt")
    sys.exit(-1)

def main():
    args  = docopt(usage, version=version)          # load args
    pwndb = core.pwndb(args)
    banner.print_banner(project, version, author)   # print banner
    
    print(': Searching\n')
    # get search results
    result = pwndb.search_info()
    
    if not result:
        print(': 0 Results found.')
        sys.exit()
    
    # print results
    for key in result.keys():
        print('- {} : {}'.format(
            result[key]['email'], 
            result[key]['passw']))
    
    print('\n: %s Results found.' % len(result.keys()))

    if args['--output']:
        output = json.dumps(result, indent=2)
        filename = args['FILENAME']
        filename = filename if filename else '%s' % time.strftime('%d%m%y-%H%M%S')
        f = open('%s.json' % filename, 'w')
        f.write(output)
        f.close()
        print(': The file %s.json was created.' % filename)


if __name__ == "__main__":
    main()

