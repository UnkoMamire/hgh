#!/usr/bin/env python3

import subprocess

def ffmpegpopen(url='', headers=''):
    if headers == '':
        cmd = ['ffmpeg', '-i', url, '-f', 'avi', 'pipe:1'] 
    else:
        cmd = ['ffmpeg', '-headers', headers, '-i', url, '-f', 'avi', 'pipe:1'] 
    return subprocess.Popen(cmd, stdout=subprocess.PIPE)
