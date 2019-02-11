#!/usr/bin/env python3

import random
import time

from string import ascii_letters, digits

char = lambda i: ' '.join(
        random.sample(ascii_letters + digits, k=i)).upper()

def shuffle(line, nlen):
    
    for x in range(0, random.randint(1, 4)):
        print('\t{}'.format(char(nlen)), end='\r')
        time.sleep(0.1)
    print('\t' + line)

def print_banner(name='Nameless', version='00.00.00', author='unknown'):

    nlen = len(name) + 4            # name legnth + four chars
    name = ' '.join(name.upper())   # space between letters

    # ? ? N A M E ? ?
    name = '{} \033[1m{} \033[0m{}'.format(char(2), name, char(2))

    lines = [char(nlen), name, char(nlen)]
    print(':\n')
    [shuffle(line, nlen) for line in lines]
    print("\n\t{}".format(author))
    print("\t{}\n".format(version))

