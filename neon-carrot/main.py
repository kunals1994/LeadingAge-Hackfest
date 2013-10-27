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
import webapp2
from twilio.rest import TwilioRestClient

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Goodbye world!')

class CallGenerator(webapp2.RequestHandler):
	def get(self):
		param = {}
		param["message"] = self.request.get("msg")
		param["language"] = self.request.get("lang")
		resp = '<?xml version="1.0" encoding="UTF-8"?><Response><Pause length="3"/><Say voice = "alice" loop="0" language = "%(language)s">%(message)s</Say><Pause length="2"/></Response>'
		resp = resp % param
		self.response.write(resp)

class CallHandler(webapp2.RequestHandler):
	def get (self):
		number = self.request.get("num")
		message = self.request.get("msg")
		language = self.request.get("lang")

		account_sid = "AC03701871ae569b1ec0facf7b8ad41e19"
		auth_token  = "9908bfe073c98b4ac3fc0afce32ff77f"
		client = TwilioRestClient(account_sid, auth_token)

		message = message.replace(" ", "%20")
 
		call = client.calls.create(url="http://neon-carrot.appspot.com/twiml?msg="+message+"&lang="+language,
   			to=number,
    		from_="+18084197884", 
    		method = "GET")


app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/call', CallHandler), ('/twiml', CallGenerator)
], debug=True)
