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



    def get_requests(self, data):
        
        try:
            req = self.session.post(self.domain, data=data)
        except Exception as e:
            print('{}E:{}{}'.format(RED, e, RESET))
            sys.exit(2)
        
        return req.text


    def response_parser(self, response):
        """ Parse pwndb response """

        print(":{} Analyzing response{}".format(GREEN, RESET))

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
    
    
    def check_email(self, email):
        """ Verify that the email is valid """

        regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if re.match(regex, email):
            return True

        print(':{} Invalid email: {}{}'.format(RED, email, RESET))
        

        
    def email_request(self, email):
        """ Request with email """

        print(":{} Request email: {}{}".format(GREEN, email, RESET))

        self.data['luser']  = email.split('@')[0]
        self.data['domain'] = email.split('@')[1]

        return self.get_requests(self.data)


    def search_localpart(self, target):
        """ Request with localpart """

        print(":{} Request local-part: {}{}".format(GREEN, target, RESET))

        self.data['luseropr'] = 1
        self.data['luser'] = target

        return self.get_requests(self.data)


    def search_password(self, target):
        """ Requests with password """

        print(":{} Request password: {}{}".format(GREEN, target, RESET))
        
        self.data['submitform'] = 'pw'
        self.data['password'] = target

        return self.get_requests(self.data)


    def search_domain(self, target):
        """ Requests with domain """

        print(":{} Request domain: {}{}".format(GREEN, target, RESET))

        self.data['domainopr'] = 1
        self.data['domain'] = target

        return self.get_requests(self.data)


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
        
        target = self.args['<target>']
        if os.path.exists(target):
            lines = open(target, 'r').readlines()
            response = ''
            
            for item in lines:
                item = item.strip('\n')
                response += self.choose_function(item) if opt_search else None

                if opt_target and self.check_email(item):
                    response += self.email_request(item)
                        
            return self.response_parser(response)

        if self.check_email(target):
            response = self.email_request(target)
            return self.response_parser(response)
