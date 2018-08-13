import sys
import os
import random 
import os.path
import urllib2
import urllib
import json
import conf

import commands
import requests


def read_file(file_name, mode='rb'):
    data = None
    with open(file_name, 'rb') as f:
        data = f.read()

    return data


def get_all_file_names(dir_name):
    file_names = commands.getoutput("ls " + dir_name + "/*.*").split('\n')

    return file_names


def http_get(url, use_proxy=False):
    return https_get(url, use_proxy)
    if url.startswith('https'):
        return https_get(url)
    req = urllib2.Request(url)
    res = urllib2.urlopen(req, timeout=60)
    res = res.read()
    return res

def https_get(url, use_proxy):
    requests.adapters.DEFAULT_RETRIES = 50
    proxy = [{ 'http':'http://10.208.204.24:3128',
              'https':'http://10.208.204.24:3128'},
    	     { 'http':'http://10.211.209.13:3128',
              'https':'http://10.211.209.13:3128'}]
    random_num = random.randint(0,1)
    proxy_random= proxy[random_num]
    proxy_random = { 'http':'http://10.208.204.24:3128',
              'https':'http://10.208.204.24:3128'}
    s = requests.Session()
    s.keep_alive = False
    s.headers['User-Agent']=r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'
    s.headers['Connection']=r'close'
    if use_proxy:
        res = s.get(url,verify=False, timeout=60, proxies=proxy_random)
    else:
        res = s.get(url,verify=False, timeout=60)
    return res.content


def http_post(url, data,header):
    req = urllib2.Request(url)
    if header != None: 
    	req.add_header('Host', 'service.tieba.baidu.com') 
    data = urllib.urlencode(data) 
    #enable cookie 
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor()) 
    response = opener.open(req, data) 
    return json.loads(response.read()) 


def print_err(msg):
    sys.stderr.write("%s\n" % msg)


if __name__ == '__main__':
    files = get_all_file_names('./data')
    print files
    sys.exit()

    file_name = 'test.txt'
    data = read_file(file_name)
    text = data.decode('utf-8')
    length = len(text)
    print "read %d bytes" % (length)

    print text
