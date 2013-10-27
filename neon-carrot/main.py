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
import time

mach = False

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Goodbye world!')

class CallGenerator(webapp2.RequestHandler):
	def get(self):
		global mach
		param = {}
		param["message"] = self.request.get("msg")
		param["language"] = self.request.get("lang")
		if(self.request.get("AnsweredBy")=="machine"):
			mach = True
		if(self.request.get("flag")=="0"):
			resp = '<?xml version="1.0" encoding="UTF-8"?><Response><Pause length = "3"/><Play loop = "3">http://neon-carrot.appspot.com/index/1.wav</Play></Response>'
		else:
			resp = '<?xml version="1.0" encoding="UTF-8"?><Response><Pause length = "3"/><Say voice = "woman" loop = "0" language = "%(language)s">%(message)s</Say></Response>'
			resp = resp % param
		self.response.write(resp)

class CallHandler(webapp2.RequestHandler):
	def get (self):
		number = self.request.get("num")
		message = self.request.get("msg")
		language = self.request.get("lang")
		flag = self.request.get("flag")
		global mach
		account_sid = "AC03701871ae569b1ec0facf7b8ad41e19"
		auth_token  = "9908bfe073c98b4ac3fc0afce32ff77f"
		client = TwilioRestClient(account_sid, auth_token)

		message = message.replace(" ", "%20")

		mach = False
 
		call = client.calls.create(url="http://neon-carrot.appspot.com/twiml?msg="+message+"&lang="+language+"&flag="+flag,
   			to=number,
    		from_="+18084197884", 
    		method = "GET", 
    		if_machine = "Continue")

		time.sleep(45)

		if (mach):
			self.response.write("fail")
		else:
			self.response.write("success")




app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/call', CallHandler), ('/twiml', CallGenerator)
], debug=True)
