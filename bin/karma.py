#!/usr/bin/env python3

project = 'Karma'
version = '17.02.19'
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

from os import path

import json
import time
import sys

# Colors
RESET, GREEN = '\033[0m', '\033[92m'

try:
    sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), '..')))
    from docopt import docopt
    from karma import banner
    from karma import core
except Exception as e:
    print("Error:", e )
    print("Please install the requirements:\n\t$ pip3 install -r requirements.txt")
    sys.exit(1)

def main():
    start = time.time()
    args  = docopt(usage, version=version)          # load args
    pwndb = core.pwndb(args)
    banner.print_banner(project, version, author)   # print banner
    
    print(':{} Searching{}'.format(GREEN, RESET))
    # get search results
    result = pwndb.search_info()
    
    if not result:
        end = time.time() - start
        print(':{} Results:{}\n'.format(GREEN, RESET))
        print('- None | None')
        print('\n:{} 0 Results found in {:.2f} segs.{}'.format(
            GREEN, end, RESET ))
        sys.exit()
    
    # print results
    print(':{} Results:{}\n'.format(GREEN, RESET))
    length = [result[key]['email'] for key in result.keys()]
    length = len(max(length, key=len))

    for key in result.keys():
        print('- {} | {}'.format(
            result[key]['email'].ljust(length),
            result[key]['passw']
        ))
    
    end = time.time() - start
    print('\n: {}{} Results found in {:.2f} segs.{}'.format(
        GREEN, len(result.keys()), end, RESET ))

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

