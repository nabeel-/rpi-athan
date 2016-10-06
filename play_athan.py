#!/usr/bin/env python

import os
import time
import datetime
from soco import SoCo
from threading import Thread
from SocketServer import TCPServer
from __future__ import print_function
from SimpleHTTPServer import SimpleHTTPRequestHandler

# Athan files names - mp3 files should be placed in the same folder as script
REG_ATAHN  = '1016.mp3'
FAJR_ATHAN = '168410.mp3'

PORT  = 8000								# Port number for web server
MY_IP = '192.168.1.10'      # IP of the Raspberry Pi
SPEAKER_IP = '192.168.1.11' # IP of the Sonos speaker

class HttpServer(Thread):
	def __init__(self, port):
		super(HttpServer, self).__init__()
		self.daemon = True
		handler = SimpleHTTPRequestHandler
		self.httpd = TCPServer(('', port), handler)

	def run(self):
		print("Starting http server")
		self.httpd.serve_forever()

	def stop(self):
		print("Stopping http server")
		self.httpd.socket.close()


def play_athan(sonos, file):
	
	netpath = 'http://{}:{}/rpi_athan/{}'.format(MY_IP, PORT, file)
	sonos.volume = 50
	sonos.play_uri(netpath)


def main():
	
	sonos  = SoCo(SPEAKER_IP)
	server = HttpServer(port)
	isFajr = datetime.datetime.now().hour < 7
	athan_file    = FAJR_ATHAN if isFajr else REG_ATAHN
	current_track = sonos.get_current_track_info()


	if current_track:
		print("Found {} playing...".format(current_track['title']))

		seek_time    = current_track['position']
		prev_volume  = sonos.volume
		playlist_pos = int(current_track['playlist_position']) 

	server.start()
	play_athan(sonos, athan_file)

	# Sleep for the amount of time it takes the athan to play
	time.sleep(245 if isFajr else 190)

	if current_track:
		print("Returning to {}...".format(current_track['title']))

		sonos.volume = prev_volume
		sonos.play_from_queue(playlist_pos)
		sonos.seek(seek_time)

	server.stop()

main()
