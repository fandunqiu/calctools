#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#

import cgi
import re
import hashlib
import wsgiref.handlers
from google.appengine.ext import webapp

class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write("""
      <html>
        <body>
          <form action="/hash" method="post">
            <div>HASH计算<div>	
            <div><input type="text" name="content" size="30" value=""></div>
            <div><input type="submit" value="计算"></div>
          </form>
	  <form action="/ip" method="post">
            <div>整数转换为IP<div>	
            <div><input type="text" name="intip" size="30" value=""></div>
            <div><input type="submit" value="转换"></div>
          </form>
	  <form action="/int" method="post">
            <div>IP转换为整数<div>	
            <div><input type="text" name="dotip" size="30" value=""></div>
            <div><input type="submit" value="转换"></div>
          </form>
        </body>
      </html>""")


class GetHash(webapp.RequestHandler):
  def post(self):
    self.response.out.write('<html><body><table>')
    content = cgi.escape(self.request.get('content')).encode('UTF-8')
    self.response.out.write("<tr><td><B>string:<B></td><td>%s</td></tr>" % content)
    md5 = hashlib.md5()
    md5.update(content)
    self.response.out.write("<tr><td><B>md5:</B></td><td>%s</td></tr>" % md5.hexdigest())

    sha1 = hashlib.sha1()
    sha1.update(content)
    self.response.out.write("<tr><td><B>sha1:</B></td><td>%s</td></tr>" % sha1.hexdigest())
    
    sha224 = hashlib.sha224()
    sha224.update(content)
    self.response.out.write("<tr><td><B>sha224:</B></td><td>%s</td></tr>" % sha224.hexdigest())

    sha256 = hashlib.sha256()
    sha256.update(content)
    self.response.out.write("<tr><td><B>sha256:</B></td><td>%s</td></tr>" % sha256.hexdigest())

    sha384 = hashlib.sha384()
    sha384.update(content)
    self.response.out.write("<tr><td><B>sha256:</B></td><td>%s</td></tr>" % sha384.hexdigest())

    sha512 = hashlib.sha512()
    sha512.update(content)
    self.response.out.write("<tr><td><B>sha512:</B></td><td>%s</td></tr>" % sha512.hexdigest())
    self.response.out.write("<table/>")

    self.response.out.write("""<hr/>
          <form action="/hash" method="post">
            <div>HASH计算<div>
            <div><input type="text" name="content" size="30" value="" ></div>
            <div><input type="submit" value="计算"></div>
          </form>
	  """)
    self.response.out.write('</body></html>')

class GetIP(webapp.RequestHandler):
  def IntToDottedIP(self,ip):
    return "%d.%d.%d.%d" % ((ip>>24)%256, ((ip&0x00FFFFFF)>>16)%256, ((ip&0x0000FFFF)>>8)%256, (ip&0x000000FF)%256)

  def post(self):
    self.response.out.write('<html><body>')
    content = cgi.escape(self.request.get('intip')).encode('UTF-8')
    try:
      ip = int(content)
      self.response.out.write(self.IntToDottedIP(ip))
    except:
      self.response.out.write("error ip") 
    self.response.out.write("""<hr/>
          <form action="/ip" method="post">
            <div>整数转换为IP<div>	
            <div><input type="text" name="intip" size="30" value=""></div>
            <div><input type="submit" value="转换"></div>
          </form>
	  """)
    self.response.out.write('</body></html>')



class GetINT(webapp.RequestHandler):
  def DottedIPToInt(self,dotted_ip):
    exp = 3
    intip = 0
    for quad in dotted_ip.split('.'):
      intip = intip + (int(quad) * (256 ** exp))
      exp = exp - 1
    return (intip)

  def post(self):
    self.response.out.write('<html><body>')
    content = cgi.escape(self.request.get('dotip')).encode('UTF-8')
    pattern = re.compile(
'^([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])$')
    if(pattern.match(content)):
      self.response.out.write(self.DottedIPToInt(content))
    else:
      self.response.out.write("error ip")
    self.response.out.write("""<hr/>
          <form action="/int" method="post">
            <div>IP转换为整数<div>	
            <div><input type="text" name="dotip" size="30" value=""></div>
            <div><input type="submit" value="转换"></div>
          </form>
	  """)
    self.response.out.write('</body></html>')




application = webapp.WSGIApplication([
  ('/', MainPage),
  ('/hash', GetHash),
  ('/ip', GetIP),
  ('/int', GetINT)
], debug=True)


def main():
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()
