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
from google.appengine.api import taskqueue


class FallbackHandler(webapp2.RequestHandler):
	def post(self):
		client = TwilioRestClient(account_sid, auth_token)
		client.messages.create(to = self.request.get("to"), from_="+12159876841", body=self.request.get("message"))

class CallAttempter(webapp2.RequestHandler):
	def post(self):
		param = {"to": self.request.get("fallback"),
		"message": self.request.get("to")+" didn't pick up the phone"}
		if(self.request.get("AnsweredBy")=="machine"):
			taskqueue.add(url='/hackfest/fallback', method = "POST", params = param, countdown = 0)
		
		#Make phone call/leave message
		param = {"language" : self.request.get("lang"), 
			"message" : self.request.get("message")
		}
		resp = '<?xml version="1.0" encoding="UTF-8"?><Response><Pause length = "1"/><Say voice = "woman" loop = "5" language = "%(language)s">%(message)s</Say></Response>'
		resp = resp % param
		self.response.write(resp)

class CallInitiator(webapp2.RequestHandler):
	def post (self):
		number = self.request.get("num")
		message = self.request.get("msg")
		language = self.request.get("lang")
		fallback = self.request.get("fallback")

		client = TwilioRestClient(account_sid, auth_token)
		message = message.replace(" ", "%20")

		number = "+"+number[1:]
		fallback = "+"+fallback[1:]
 
		call = client.calls.create(url="http://www.neon-carrot.appspot.com/hackfest/attempt?message="+message+"&lang="+language+"&fallback="+fallback+"&to="+number,
   			to=number,
    		from_="+12159876841", 
    		method = "POST", 
    		if_machine = "Continue")

class CallGenerator(webapp2.RequestHandler):
	def get(self):
		number = self.request.get("send_to")
		message = self.request.get("msg")
		language = self.request.get("lang")
		fallback = self.request.get("fallback")

		param = {
		"num":number,
		"msg":message,
		"lang":language,
		"fallback":fallback
		}

		minutes_to_wait = int(self.request.get("countdown"))

		taskqueue.add(url = '/hackfest/initiate', method="POST", params = param, countdown = minutes_to_wait*60)


		self.response.write('<script>window.location.replace("http://kshar.me");window.alert("Reminder set! You will be notified if the receipient does not pick up");</script>')


app = webapp2.WSGIApplication([
    ('/hackfest/fallback', FallbackHandler), ('/hackfest/attempt', CallAttempter),
    ('/hackfest/initiate', CallInitiator), ('/hackfest/generate', CallGenerator)
], debug=True)
