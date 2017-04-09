import pycurl
import urllib
import json
import StringIO
from flask import Flask
from flask import render_template
from flask import request, url_for
from flask.ext.session import Session
import logging
app = Flask(__name__)
from auth import Authentication
@app.route('/')
def root():
     return render_template('login.html')
@app.route("/handle_login")
def handle_login():
    access_token = request.args['access_token']
    b = StringIO.StringIO()
    #logging.error(str(type(access_token)))
    #logging.error(str(access_token))
    access_token = access_token.encode('utf-8') #access code is unicode convert to utf-8
    # verify that the access token belongs to us
    c = pycurl.Curl()
    c.setopt(pycurl.URL, "https://api.amazon.com/auth/o2/tokeninfo?access_token=" + urllib.quote_plus(access_token))
    c.setopt(pycurl.SSL_VERIFYPEER, 1)
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    
    c.perform()
    d = json.loads(b.getvalue())
    
    if d['aud'] != 'amzn1.application-oa2-client.74e27ed5f3da48d18b60b6b156787d9a' :
        # the access token does not belong to us
        raise BaseException("Invalid Token")
    
    # exchange the access token for user profile
    b = StringIO.StringIO()
    
    c = pycurl.Curl()
    c.setopt(pycurl.URL, "https://api.amazon.com/user/profile")
    c.setopt(pycurl.HTTPHEADER, ["Authorization: bearer " + access_token])
    c.setopt(pycurl.SSL_VERIFYPEER, 1)
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    
    c.perform()
    d = json.loads(b.getvalue())
    #todo implement sessions
    #Session['user_id'] = d['user_id']
    #return "%s %s %s"%(d['name'], d['email'], d['user_id'])
    Authentication.post_token(d['name'], d['email'], d['user_id'])

    #    print "%s %s %s"%(d['name'], d['email'], d['user_id'])
if __name__ == "__main__":
    app.run()