#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#

import cgi
import base64
import wsgiref.handlers
from google.appengine.ext import webapp

class GetBase64(webapp.RequestHandler):
  def printhead(self):
	self.response.out.write(
	"""
	<html><head><title>base64在线编码和解码</title></head><body><p/><p/><center>
	""")
  def printtail(self):
	self.response.out.write(
	"""
	</center></body></html>
	""")
  def printjs(self):
	self.response.out.write(
	"""
	<script type="text/javascript">
	function csubmit(obj)
	{
		var btype=document.getElementById("btype");
		var cf=document.getElementById("base64");
		if(obj.id == "encode")
			btype.value = "encode";
		else
			btype.value = "decode";
		cf.submit();
	}
	</script>
	""")
  def printbody(self):
	self.response.out.write(
	"""
	<form action="/base64" method="post" name=base64 id=base64>
            <div>请输入你要编码或解码的文字<div>
			<div><input type=hidden id=btype name=btype><div>
            <div><textarea name="content" rows="3" cols="60"></textarea></div>
            <div><input type=button id=decode name=decode onclick=csubmit(this) value="解 码">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
			<input type=button id=encode name=encode onclick=csubmit(this) value="编 码"></div>
	<form>
	""")

  def get(self):
	self.printhead()
	self.printjs()
	self.printbody()
	self.printtail()

  def post(self):
    self.printhead()
    btype = self.request.get('btype')
    content = cgi.escape(self.request.get('content')).encode('UTF-8')
    try:
        if(btype == "decode"):
            self.response.out.write(base64.decodestring(content))
        elif(btype == "encode"):
            self.response.out.write(base64.encodestring(content))
        else:
            self.response.out.write(content)
    except:
	    self.response.out.write("输入错误的base64编码:")
    self.response.out.write("<p/><p/><p/>")
    self.printjs()
    self.printbody()
    self.printtail()
    
application = webapp.WSGIApplication([('/base64', GetBase64)], debug=True)

def main():
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()
