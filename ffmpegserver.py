#!/usr/bin/env python3

import httpserver
import ffmpegpopen

import sys
import itertools as it
import functools as ft

chunk_size = 8192

def main(port=0, url='', header=''):
    server = httpserver.HTTPServer()

    server.bind(port=port)
    server.open()

    proc = ffmpegpopen.ffmpegpopen(url, header)
    prebuffer = proc.stdout.read(chunk_size)
    stream_iterator = it.chain([prebuffer], iter(ft.partial(proc.stdout.read, chunk_size), b''))

    for data in stream_iterator:
        server.write(data)

    server.close()


if __name__ == '__main__':
    main(int(sys.argv[1]), *sys.argv[2:])
