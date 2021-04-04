#!/usr/bin/env python3

import csv
import os.path

class Player:
    def __init__(self, videourl = ''):
        self.__videourl = videourl

    @property
    def videoURL(self):
        return self.__videourl

    @videoURL.setter
    def videoURL(self, videourl):
        self.__videourl = videourl

class Team(dict[str,Player]):
    pass

class Participant(dict[str,Team]):
    pass

def readFile(filepath = os.path.expanduser('~/ParticipantList.txt')):
    ret = Participant()

    with open(filepath, 'r',encoding="utf-8_sig") as fd:
        reader = csv.DictReader(fd, skipinitialspace = True)

        for part in reader:
            ret.setdefault(part['TeamName'], Team())
            ret[part['TeamName']][part['PlayerName']] = Player(videourl = part['VideoURL'])

    return ret

