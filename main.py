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
import webapp2
import jinja2
import output27
import json

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape = False)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainHandler(Handler):
	def get(self):
		self.render("mainInputs.html")

	def post(self):
		amount = self.request.get("amount")
		company = self.request.get("company")
		
		#This formats the company parameter to an array of strings.
		symbol = str(company).split()
		#Setting the time series of stock information
		start_date = '20140101'
		end_date = '20140701'

		#Run the Static Model Calculations and get the outputs of the Models into an array.
		calculatedResults = output27.results(symbol, start_date, end_date)
		returns = float(calculatedResults[0])*100.0
		risks = float(calculatedResults[1])*100
		allocation = calculatedResults[2]*100

		#Formatting the piedata in order to display
		piedata =[{"label": "joe", "value": 50},{"label": "mike","value": 50}, {"label": "pete","value": 70}]
		print symbol
		print amount
		
		self.render("mainOutputs.html", returns=returns, risks=risks, allocation=piedata)


app = webapp2.WSGIApplication([('/', MainHandler)], debug=True)
