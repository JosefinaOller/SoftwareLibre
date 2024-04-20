#!/usr/bin/env python

import sys, time
from weatherdaemon import WeatherDaemon

TOKEN = '7007180975:AAFK3P7eOyonHF5pSj_vStvWrGluN3Fohb8'
BOT_USERNAME = '@joelcoyos_bot'

if __name__ == "__main__":
	daemon = WeatherDaemon('/tmp/daemon-example.pid',TOKEN,BOT_USERNAME)
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print ("Unknown command")
			sys.exit(2)
		sys.exit(0)
	else:
		print ("usage: %s start|stop|restart") % sys.argv[0]
		sys.exit(2)
