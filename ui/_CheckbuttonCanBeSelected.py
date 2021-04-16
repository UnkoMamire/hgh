#!/usr/bin/env python3

import tkinter as tk
import functools as ft

from . import _utils as utils

class _ManyCheckbuttonCreater:
    def __init__(self, master):
        self.__master = master

    def addCheckbutton(self, **kw):
        return tk.Checkbutton(self.__master, **kw)

    def cleanFrame(self):
        utils.destroy_child(self.__master)


class _CheckbuttonCanBeSelected(_ManyCheckbuttonCreater):
    pass


def _selectCheckbutton(cb: tk.Checkbutton):
    cb.select()

def _deselectCheckbutton(cb: tk.Checkbutton):
    cb.deselect()


class OnlyOneCheckbuttonCanBeSelected(_CheckbuttonCanBeSelected):
    def __init__(self, master):
        super().__init__(master)
        self.__selected = None

    def __checkbuttonSelected(self, cb):
        if self.__selected != None:
            _deselectCheckbutton(self.__selected)
        self.__selected = cb

    def __selectCommand(self, cb, cmd):
        self.__checkbuttonSelected(cb)
        if cmd is not  None:
            cmd()

    def addCheckbutton(self, **kw):
        if 'command' in kw:
            cmd = kw.pop('command')
        else:
            cmd = None
        cb = super().addCheckbutton(**kw)
        # cb['command'] = lambda: self.__selectCommand(cb, cmd)
        cb['command'] = ft.partial(self.__selectCommand, cb, cmd)
        return cb

    def cleanFrame(self):
        self.__selected = None
        super().cleanFrame()

class OnlyTowCheckbuttonCanBeSelected(_CheckbuttonCanBeSelected):
    def __init__(self, master: tk.Widget):
        super().__init__(master)
        self.__selected = list()

    def __checkbuttonSelected(self, cb):
        self.__selected.append(cb)

    def __checkbuttonDeselected(self, cb):
        _deselectCheckbutton(cb)
        self.__selected.remove(cb)

    def __selectCommand(self, cb, cmd):
        if len(self.__selected) < 2:
            self.__checkbuttonSelected(cb)
            if cmd is not None:
                cmd()
        else:
            _deselectCheckbutton(cb)

    def __deselectCommand(self, cb, cmd):
        self.__checkbuttonDeselected(cb)
        if cmd is not None:
            cmd()

    def __command(self, cb, cmd):
        if cb in self.__selected:
            self.__deselectCommand(cb, cmd)
        else:
            self.__selectCommand(cb, cmd)

    def addCheckbutton(self, **kw):
        if 'command' in kw:
            cmd = kw.pop('command')
        else:
            cmd = None
        cb = super().addCheckbutton(**kw)
        # cb['command'] = lambda: self.__command(cb, cmd)
        cb['command'] = ft.partial(self.__command, cb, cmd)
        return cb

    def cleanFrame(self):
        self.__selected.clear()
        super().cleanFrame()


    @property
    def count(self):
        return len(self.__selected)

    @property
    def selected(self):
        return tuple([i['text'] for i in self.__selected])

