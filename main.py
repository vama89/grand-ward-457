#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
#Sign-in import Code will go here:
import re
import random
import hashlib
import hmac
from string import letters

#imports that are not part of sign-in/register
import output27
import json

import webapp2
import jinja2

#Database Code
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape = False)

######Code for the Regular Website#################
class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class About(Handler):
	def get(self):
		self.render("about.html")

class Blog(Handler):
	def get(self):
		self.render("blog.html")

class Login_Register(Handler):
	def get(self):
		self.render("Login_Register.html")

class Test_Graph(Handler):
	def get(self):
		self.render("testGraphs.html")

class MainHandler(Handler):
	def get(self):
		self.render("mainInputs.html")

	def post(self):
		

		#Run the Static Model Calculations and get the outputs of the Models into an array.
		try:
			amount = float(self.request.get("amount"))
			company = self.request.get("company")
			models = self.request.get("models")
			modelLabel=str(models)

			#This formats the company parameter to an array of strings.
			symbol = str(company).split()
			
			#Setting the time series of stock information
			start_date = '20140101'
			end_date = '20140701'
			
			#Setting the results of the calculations:
			calculatedResults = output27.results(symbol, start_date, end_date, models)
			returns = float(calculatedResults[0])*100.0
			anuityFactor = float(calculatedResults[0])+1.0
			totalMoneyMade = amount*anuityFactor
			moneyReturned = totalMoneyMade-1000.0
			risks = float(calculatedResults[1])*100.0

			symbolSort = calculatedResults[3]

			if len(symbolSort) == 1:
				allocation = [1]
			else:
				allocation = calculatedResults[2]

			self.render("mainOutputs.html", returns=returns, 
											risks=risks, 
											symbolSort=symbolSort, 
											allocation=allocation, 
											amount=amount, 
											moneyReturned=moneyReturned, 
											totalMoneyMade=totalMoneyMade, 
											modelLabel=modelLabel)
		except:
			self.render("mainInputsError.html")
				
		
		#checking for correct input

		#resp = urllib2.urlopen(req)
		#content = str(resp.read().decode('utf-8').strip())
		#daily_data = content.splitlines()
		#t = len(daily_data)

		#Formatting the piedata in order to display
		#piedata =[{"label": "joe", "value": 50},{"label": "mike","value": 50}, {"label": "pete","value": 70}]
		
##################################	

####Code for User Login and registration#######

secret = 'fart'

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))
"""
def render_post(response, post):
    response.out.write('<b>' + post.subject + '</b><br>')
    response.out.write(post.content)

class MainPage(BlogHandler):
  def get(self):
      self.write('Hello, Udacity!')
"""
##### user stuff
def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

def users_key(group = 'default'):
    return db.Key.from_path('users', group)

class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent = users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent = users_key(),
                    name = name,
                    pw_hash = pw_hash,
                    email = email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u

##### blog stuff
"""
def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p = self)

class BlogFront(BlogHandler):
    def get(self):
        posts = greetings = Post.all().order('-created')
        self.render('front.html', posts = posts)

class PostPage(BlogHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        self.render("permalink.html", post = post)

class NewPost(BlogHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/login")

    def post(self):
        if not self.user:
            self.redirect('/blog')

        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(parent = blog_key(), subject = subject, content = content)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, content=content, error=error)


###### Unit 2 HW's

class Rot13(BlogHandler):
    def get(self):
        self.render('rot13-form.html')

    def post(self):
        rot13 = ''
        text = self.request.get('text')
        if text:
            rot13 = text.encode('rot13')

        self.render('rot13-form.html', text = rot13)

"""
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Signup(BlogHandler):
    def get(self):
        self.render("signup-form.html")

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username = self.username,
                      email = self.email)

        if not valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError
"""
class Unit2Signup(Signup):
    def done(self):
        self.redirect('/unit2/welcome?username=' + self.username)
"""
class Register(Signup):
    def done(self):
        #make sure the user doesn't already exist
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('signup-form.html', error_username = msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect('/unit3/welcome')

class Login(BlogHandler):
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/unit3/welcome')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error = msg)

class Logout(BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/')

class Unit3Welcome(BlogHandler):
    def get(self):
        if self.user:
            self.render('mainInputsUser.html', username = self.user.name)
        else:
            self.redirect('/signup')

    def post(self):
		

		#Run the Static Model Calculations and get the outputs of the Models into an array.
		try:
			amount = float(self.request.get("amount"))
			company = self.request.get("company")
			models = self.request.get("models")
			modelLabel=str(models)

			#This formats the company parameter to an array of strings.
			symbol = str(company).split()
			
			#Setting the time series of stock information
			start_date = '20140101'
			end_date = '20140701'
			
			#Setting the results of the calculations:
			calculatedResults = output27.results(symbol, start_date, end_date, models)
			returns = float(calculatedResults[0])*100.0
			anuityFactor = float(calculatedResults[0])+1.0
			totalMoneyMade = amount*anuityFactor
			moneyReturned = totalMoneyMade-1000.0
			risks = float(calculatedResults[1])*100.0

			symbolSort = calculatedResults[3]

			if len(symbol) == 1:
				allocation = [1]
			else:
				allocation = calculatedResults[2]

			self.render("mainOutputsUser.html", returns=returns, 
											risks=risks, 
											symbolSort=symbol, 
											allocation=allocation, 
											amount=amount, 
											moneyReturned=moneyReturned, 
											totalMoneyMade=totalMoneyMade, 
											modelLabel=modelLabel,
											username=self.user.name)
		except:
			self.render("mainInputsErrorUser.html", username=self.user.name)
"""
class Welcome(BlogHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
            self.redirect('/unit2/signup')
"""
#########


app = webapp2.WSGIApplication([('/', MainHandler),
								('/About', About),
								('/Blog', Blog),
								('/Login_Register', Login_Register),
								('/Test_Graph', Test_Graph),
								#('/', MainPage),
								#('/unit2/rot13', Rot13),
								#('/unit2/signup', Unit2Signup),
								#('/unit2/welcome', Welcome),
								#('/blog/?', BlogFront),
								#('/blog/([0-9]+)', PostPage),
								#('/blog/newpost', NewPost),
								('/signup', Register),
								('/login', Login),
								('/logout', Logout),
								('/unit3/welcome', Unit3Welcome),], debug=True)
