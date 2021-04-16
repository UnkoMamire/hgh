#!/usr/bin/env python3

import obscontrol
import streamlinkwrapper

slm = streamlinkwrapper.SLManager()

class _FewStreamManager:
    def __init__(self, basedesc, quantity):
        self.__basedesc = basedesc
        self.__quantity = quantity
        self.__count = 0

    def setURL(self, *urls):
        for url in urls:
            if url is not None:
                slm.start(self.__basedesc+self.__count, url)
                self.__count += 1

    def reset(self):
        while self.__count > 0:
            self.__count -= 1
            slm.stop(self.__basedesc+self.__count)
            print('Stopped {0}'.format(self.__basedesc+self.__count))

class _ManySteamManager:
    def __init__(self, basedesc, quantity1, quantity2):
        self.__waiting = list()
        for i in range(quantity1):
            self.__waiting.append(_FewStreamManager(basedesc+(i*quantity2), quantity2))
        self.__used = dict()

    def setURL(self, key, *urls):
        if key not in self.__used:
            self.__used[key] = self.__waiting.pop()
        self.__used[key].reset()
        self.__used[key].setURL(*urls)

    def reset(self):
        for k in reversed(list(self.__used)):
            self.__used[k].reset()
            self.__waiting.append(self.__used.pop(k))
