import json
import sys
import os
import urllib2
import urllib
import urlparse
import BaseHTTPServer
import webbrowser
import fbGraphAPI

from authToken import *

def getUrl(path, args=None):
    args = args or {}
    if accessToken:
        args['access_token'] = accessToken
    if 'access_token' in args or 'client_secret' in args:
        endpoint = "https://"+ENDPOINT
    else:
        endpoint = "http://"+ENDPOINT
    return endpoint+path+'?'+urllib.urlencode(args)

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def getU(self,path, args=None):
        return urllib2.urlopen(getUrl(path, args=args)).read()

    def do_GET(self):
        global accessToken
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        code = urlparse.parse_qs(urlparse.urlparse(self.path).query).get('code')
        code = code[0] if code else None
        if code is None:
            self.wfile.write("<html><head><title>Failure :(</title></head><body bgcolor='black'><center><br><p1><font size='48px' color='red'>There was a problem logging into Facebook.  Please try again.</font></p1></center></body></html>")
            exit(1)

        response = self.getU('/oauth/access_token', {'client_id':appId,
                                               'redirect_uri':redirectUri,
                                               'client_secret':appSecret,
                                               'code':code})
        accessToken = urlparse.parse_qs(response)['access_token'][0]
        open(tokenFile,'w').write(accessToken)
        self.wfile.write("<html><head><title>Success!</title></head><body bgcolor='black'><center><p1><font size='48px' color='green'>You've successfully logged in to facebook</font></p1></center></body></html>")

class TokenHandler:
    def getToken(self):
        global accessToken
        if not os.path.exists(tokenFile):     #checking if the access token file already exists
            print 'Logging you in to facebook...'
            webbrowser.open(getUrl('/oauth/authorize',
                                    {'client_id':appId,
                                     'redirect_uri':redirectUri,
                                     'scope':FBPermission}))

            httpd = BaseHTTPServer.HTTPServer(('localhost', 13080), RequestHandler)     #request for the access token
            while accessToken is None:      # keep on requesting for the access token until success
                httpd.handle_request()
        else:
            accessToken = open(tokenFile).read()

        return accessToken

if __name__ == '__main__':
    print 'Attempting to obtain oauth token...'
    tokenObj = TokenHandler()
    accessToken = tokenObj.getToken()
    print 'Generating facebook graph api object...'
    graph = fbGraphAPI.GraphAPI(accessToken)
    print 'Getting the user profile...'
    myProfile = graph.get_object("me")
    print myProfile
    print 'Getting the user friends data...'
    myFriends = graph.get_connections(myProfile["id"], "friends")
    print myFriends
