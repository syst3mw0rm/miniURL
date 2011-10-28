#!/usr/bin/env python
#
# Copyright 2011 Aamir Khan
#
# 
import redis
import json
import tornado.web
import tornado.ioloop
import urllib
import urlparse
import datetime
import re
import tornado.httpserver
import tornado.options
import os.path

from tornado.options import define, options

define("config")
define("port", type=int)

#redisServer = redis.StrictRedis(host='localhost',port=6379 ,db=0)

class ShortenApplication(tornado.web.Application):
	def __init__(self):
		#self.redisServer = redis.StrictRedis(host='localhost',port=6379 ,db=0)
		
		settings = {
  
          
     	 }
		
		tornado.web.Application.__init__(self, [
   			   tornado.web.url(r"/s/([^/]+)", Shorten, name="Index"),
			   tornado.web.url(r"/([a-zA-Z0-9]+)", Expand, name="Index"),
			   tornado.web.url(r"/", MainHandler ,name = "Index"),
      	], **settings)



class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.redisServer = redis.StrictRedis(host='localhost',port=6379 ,db=0)
		self.write("Index Page..To be Updated with content")




class Shorten(tornado.web.RequestHandler):
   
	def get(self,id):
		self.redisServer = redis.StrictRedis(host='localhost',port=6379 ,db=0)
		self.write(self.shorten(id))

   	def shorten(self, long_url=None):
   
   		url_hash = '%x' % self.redisServer.incr('next.url.id')	#hex value of counter
		
		#next we store the long_url against this hashed key
		
		self.redisServer.set('url:%s:id' % url_hash, long_url)
	   
		#push this short url in global list of URLs
		self.redisServer.lpush('global:urls',url_hash)
		
		return long_url + url_hash
		

class Expand(tornado.web.RequestHandler):

	def get(self, id):
		self.redisServer = redis.StrictRedis(host='localhost',port=6379 ,db=0)
		long_url = self.expand(id)
		self.write("Redirecting to "+long_url)
		self.redirect(long_url)

	def expand(self, shorten_url=None):
	
		long_url = self.redisServer.get('url:%s:id' % shorten_url)

		return long_url



#class Visit(tornado.web.RequestHandler):

#	def get(self, id):
#		self.redisServer = redis.StrictRedis(host='localhost',port=6379 ,db=0)
#		self.write(self.shorten(id))


#	def visit(self, shorten_url=None, ip_addr=None,agent=None,referrer=None):
		
		#create an object of Visitor type
#		visitor = Visitor(ip_addr, agent, referrer)

		#push the visitor object in visitor list of this shorten URL in json encoded form
#		self.redisServer.push('visitors:%s' % shorten_url, json.dumps(visitor))

#		return self.redisServer.incr('clicks:%s:url' % shorten_url)


		


	

def main():
	tornado.options.parse_command_line()
	if options.config:
		tornado.options.parse_config_file(options.config)
	else:
		path = os.path.join(os.path.dirname(__file__), "settings.py")
		tornado.options.parse_config_file(path)
	ShortenApplication().listen(options.port)
	tornado.ioloop.IOLoop.instance().start()





if __name__ == "__main__":
	main()


