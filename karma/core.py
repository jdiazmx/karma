#!/usr/bin/env python3

import requests
import sys
import re
import os

# Colors
GREEN, RED, RESET = '\033[92m', '\033[91m', '\033[0m'


class pwndb(object):

    """Docstring for pwndb. """

    def __init__(self, args):
        self.domain = 'http://pwndb2am4tzkvold.onion/'
        self.args = args
        self.data = {
            'luseropr'  : 0,
            'domainopr' : 0,
            'submitform': 'em'
        }
        
        proxy = self.args['--proxy']
        if '//' in proxy:
            proxy = proxy.split('//')[1]

        self.session = requests.session()
        self.session.proxies = {
            'http' : 'socks5h://%s' % proxy,
            'https': 'socks5h://%s' % proxy
        }



    def get_request(self, data):
        """ Get requests """
        
        try:
            req = self.session.post(self.domain, data=data)
        except Exception as e:
            print('{}E:{}{}'.format(RED, e, RESET))
            sys.exit(2)
        
        return req.text


    def response_parser(self, response):
        """ Parse pwndb response """

        print("\n:{} Analyzing response{}".format(GREEN, RESET))

        if not response:
            return ''

        resp = re.findall(r'\[(.*)', response)
        resp = [ resp[n:n+4] for n in range(0, len(resp), 4) ]
        results = {}
        getinfo = lambda s: s.split('=>')[1].strip()
        for item in resp:
            results[getinfo(item[0])] = {
                'email':'{}@{}'.format(getinfo(item[1]), getinfo(item[2])),
                'passw': getinfo(item[3])
            }

        return results
    
       
    def email_request(self, target):
        """ Request with email """
        
        regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if re.match(regex, target):
            print(':{} Request email: {}{}\033[J'.format(GREEN, target, RESET), end='\r')

            self.data['luser']  = target.split('@')[0]
            self.data['domain'] = target.split('@')[1]

            return self.get_request(self.data)
        
        print(':{} Invalid email: {}{}\033[J'.format(RED, target, RESET))
        return ""

    
    def search_localpart(self, target):
        """ Request with localpart """

        regex = r"(^[a-zA-Z0-9_.+%-]+$)"
        if re.match(regex, target):
            print(':{} Request local-part: {}{}\033[J'.format(GREEN, target, RESET), end='\r')

            self.data['luseropr'] = 1
            self.data['luser'] = target

            return self.get_request(self.data)

        print(':{} Invalid local-part: {}{}\033[J'.format(RED, target, RESET))
        return ""


    def search_domain(self, target):
        """ Requests with domain """

        regex = r"(^[a-zA-Z0-9-%]+\.[a-zA-Z0-9-.%]+$)"
        if re.match(regex, target):
            print(':{} Request domain: {}{}\033[J'.format(GREEN, target, RESET), end='\r')

            self.data['domainopr'] = 1
            self.data['domain'] = target

            return self.get_request(self.data)

        print(':{} Invalid domain: {}{}\033[J'.format(RED, target, RESET))
        return ""


    def search_password(self, target):
        """ Requests with password """
        
        print(':{} Request password: {}{}\033[J'.format(GREEN, target, RESET), end='\r')
            
        self.data['submitform'] = 'pw'
        self.data['password'] = target

        return self.get_request(self.data)


    def choose_function(self, target):
        """
        Choose the corresponding function 
        according to the parameter
        """

        opts = {
            '--local-part': self.search_localpart,
            '--password'  : self.search_password,
            '--domain'    : self.search_domain
        }
            
        for key, value in self.args.items():
            if value and key in opts:
                return opts[key](target)


    def search_info(self):
        """Start the information search"""

        opt_search = self.args['search']
        opt_target = self.args['target']
        
        response = ''
        target = self.args['<target>']

        if os.path.exists(target):
            lines = open(target, 'r').readlines()
            for item in lines:
                item = item.strip('\n')
                
                try:
                    if opt_search:
                        response += self.choose_function(item)

                    if opt_target:
                        response += self.email_request(item)

                except KeyboardInterrupt:
                    print('\n:{} break{}'.format(RED, RESET))
                    break
                
            return self.response_parser(response)
        
        if opt_search:
            response = self.choose_function(target)

        if opt_target and target:
            response = self.email_request(target)
        
        return self.response_parser(response)
