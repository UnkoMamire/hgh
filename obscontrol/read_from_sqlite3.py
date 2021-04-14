#!/usr/bin/env python3

from .main import *

import sqlite3
from os.path import expanduser

class MyScene(list):
    def __init__(self, obs: ObsControl, scene_name: str, scene_id: str, *items):
        super().__init__(*items)
        self.__obs = obs
        self.__name = scene_name
        self.__id = scene_id

    @property
    def name(self):
        return self.__name

    @property
    def id(self):
        return self.__id


class MyItem:
    def __init__(self, obs: ObsControl, scene: MyScene, item_name: str, item_id: str, source_id: str,
            position_x: int, position_y: int, size_width: int, size_height: int):
        self.__obs = obs
        self.__scene = scene
        self.__name = item_name
        self.__item_id = item_id
        self.__source_id = source_id
        self.__position_x = position_x
        self.__position_y = position_y
        self.__size_width = size_width
        self.__size_height = size_height

    @property
    def scene(self):
        return self.__scene

    @property
    def name(self):
        return self.__name

    @property
    def item_id(self):
        return self.__item_id

    @property
    def source_id(self):
        return self.__source_id

    def align(self):
        self.__obs.set_sceneitem_size(self.scene.id, self.item_id, self.__size_width, self.__size_height)
        self.__obs.set_sceneitem_position(self.scene.id, self.item_id, self.__position_x, self.__position_y)


def read_db(db_file: str = expanduser('~/myobs.sqlite3')):
    ret = dict()
    obs = ObsControl()
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    cur.execute('select name, id from scene')
    for row in cur:
        scene_name, scene_id = row
        ret[scene_name] = MyScene(obs, scene_name, scene_id)

    cur.execute('select scene.name, scene_id, item_name, item_id, source_id, position_x, position_y, size_width, size_height from item innner join scene on scene_id = scene.id')
    for row in cur:
        scene_name = row[0]
        newitem = MyItem(obs, *row[1:])
        ret[scene_name].append(newitem)

    conn.close()
    return ret
