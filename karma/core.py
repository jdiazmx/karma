#!/usr/bin/env python3

import requests
import re
import sys
import os

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

    def response_parser(self, response):
        """ Parse pwndb response """

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

        
    def email_request(self, email):
        """ Request with email """

        self.data['luser']  = email.split('@')[0]
        self.data['domain'] = email.split('@')[1]
        try:
            req = self.session.post(self.domain, data=self.data)
        except Exception as e:
            print('Error:', e)
            sys.exit(1)

        return req.text


    def search_localpart(self, target):
        """ Request with localpart """

        self.data['luseropr'] = 1
        self.data['luser'] = target

        try:
            req = self.session.post(self.domain, data=self.data)
        except Exception as e:
            print('Error:', e)
            sys.exit(1)

        return req.text

    def search_password(self, target):
        """ Requests with password """
        
        self.data['submitform'] = 'pw'
        self.data['password'] = target

        try:
            req = self.session.post(self.domain, data=self.data)
        except Exception as e:
            print('Error:', e)
            sys.exit(1)

        return req.text

    def search_domain(self, target):
        """ Requests with domain """

        self.data['domainopr'] = 1
        self.data['domain'] = target

        try:
            req = self.session.post(self.domain, data=self.data)
        except Exception as e:
            print('Error:', e)
            sys.exit(1)

        return req.text

    def search_info(self):
        
        search = self.args['search']
        target = self.args['<target>']

        if search:
            opts = {
                '--local-part': self.search_localpart,
                '--password'  : self.search_password,
                '--domain'    : self.search_domain}

            for key, value in self.args.items():
                if value and key in opts:
                   response = opts[key](target)
                   return self.response_parser(response)

        if self.check_email(target):
            response = self.email_request(target)
            return self.response_parser(response)
        
        if os.path.exists(target):
            emails = open(target, 'r').readlines()
            response = ''
            for email in emails:
                email = email.strip('\n')
                if self.check_email(email):
                    response += self.email_request(email)
            return self.response_parser(response)

