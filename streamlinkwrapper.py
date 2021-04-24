#!/usr/bin/env python3

import subprocess
from urllib.parse import urlparse
import os.path

class SLManager:
    def __init__(self):
        self.__slset = {}

    def start(self, desc, url):
        parsed_url = urlparse(url)
        if parsed_url.netloc == 'www.youtube.com' or parsed_url.netloc == 'www.twitch.tv':
            proc = subprocess.Popen(['streamlink', url, '720p,720p60,480p,best' , '--player-external-http', '--player-external-http-port', str(desc), '--twitch-disable-ads'])
        elif parsed_url.netloc == 'do8w5ym3okkik.cloudfront.net':
            proc = subprocess.Popen([os.path.join(os.path.dirname(__file__), 'ffmpegserver.py'), str(desc), url, 'Referer: https://www.mildom.com/'])
        else:
            proc = subprocess.Popen([os.path.join(os.path.dirname(__file__), 'ffmpegserver.py'), str(desc), url])
        self.stop(desc)
        self.__slset[desc] = proc

    def stop(self, desc):
        if desc in self.__slset:
            proc = self.__slset.pop(desc)
            proc.kill()

if __name__ == '__main__':
    slm = SLManager()
    slm.start(49152, 'https://www.youtube.com/watch?v=IBflp1YeR3k')
    input()
    slm.stop(49152)
