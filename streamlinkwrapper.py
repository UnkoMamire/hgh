#!/usr/bin/env python3

import subprocess

class SLManager:
    def __init__(self):
        self.__slset = {}

    def start(self, desc, url):
        proc = subprocess.Popen(['streamlink', url, 'best' , '--player-external-http', '--player-external-http-port', str(desc), '--twitch-disable-ads'])
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
