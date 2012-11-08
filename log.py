from oauth.oauth import OAuthRequest, OAuthSignatureMethod_HMAC_SHA1
from hashlib import md5
from ConfigParser import SafeConfigParser
import json, time
import random, math, re, urllib, urllib2
import os, datetime

STREAM_URL = "https://userstream.twitter.com/2/user.json"

class Token(object):
    def __init__(self,key,secret):
        self.key = key
        self.secret = secret

    def _generate_nonce(self):
        random_number = ''.join(str(random.randint(0, 9)) for i in range(40))
        m = md5(str(time.time()) + str(random_number))
        return m.hexdigest() 


parser = SafeConfigParser()
parser.read('settings.ini')

CONSUMER_KEY = parser.get('twitter', 'CONSUMER_KEY')
CONSUMER_SECRET = parser.get('twitter', 'CONSUMER_SECRET')
ACCESS_TOKEN = parser.get('twitter', 'ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = parser.get('twitter', 'ACCESS_TOKEN_SECRET')

DIR_PATH = parser.get('logging', 'path')

access_token = Token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
consumer = Token(CONSUMER_KEY,CONSUMER_SECRET)
    
parameters = {
    'oauth_consumer_key': CONSUMER_KEY,
    'oauth_token': access_token.key,
    'oauth_signature_method': 'HMAC-SHA1',
    'oauth_timestamp': str(int(time.time())),
    'oauth_nonce': access_token._generate_nonce(),
    'oauth_version': '1.0',
}


oauth_request = OAuthRequest.from_token_and_callback(access_token,
                http_url=STREAM_URL, 
                parameters=parameters)
signature_method = OAuthSignatureMethod_HMAC_SHA1()
signature = signature_method.build_signature(oauth_request, consumer, access_token)

parameters['oauth_signature'] = signature

data = urllib.urlencode(parameters)

req = urllib2.urlopen("%s?%s" % (STREAM_URL,data))
buffer = ''

yesterday = datetime.date.today()
file_name = "%s.log" % yesterday.strftime('%y-%m-%d')
file_path = os.path.join(DIR_PATH, file_name)
f = open(file_path, 'a')

while True:
    today = datetime.date.today()
    if yesterday.day is not today.day:
        f.close()
        file_name = "%s.log" % yesterday.strftime('%y-%m-%d')
        file_path = os.path.join(DIR_PATH, file_name)
        f = open(file_path, 'a')
        yesterday = today # Contradiction!

    chunk = req.read(1)
    if not chunk:
        f.write(chunk)
        f.flush()
        break
    chunk = unicode(chunk)
    buffer += chunk
    tweets = buffer.split("\n",1)
    if len(tweets) > 1:
        f.write(tweets[0])
        f.flush()
        buffer = tweets[1]
