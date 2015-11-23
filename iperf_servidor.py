#!/usr/bin/env python


import os
import time

def main():
	print 'INICIANDO SERVIDOR'
	os.system("iperf -s")
	
if __name__ == '__main__':
	main()
