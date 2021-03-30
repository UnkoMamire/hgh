#!/usr/bin/env python3

import tkinter as tk
import functools as ft

from . import _utils as utils
from . import _ButtonCanBeSelected as bcbs
from . import _CheckbuttonCanBeSelected as ccbs

class CheckbuttonFromButtons:
    def __init__(self, btnframe, cbframe1, cbframe2):
        self.__bcbs = bcbs.OnlyTowButtonCanBeSelected(btnframe)
        self.__ccbs1 = ccbs.OnlyTowCheckbuttonCanBeSelected(cbframe1)
        self.__ccbs2 = ccbs.OnlyTowCheckbuttonCanBeSelected(cbframe2)

    def __buttonCommand(self, cmd, mem):
        kw = dict()

        if self.__bcbs.count == 1:
            kw['command'] = lambda: cmd(*self.__ccbs1.selected)
            targetframe = self.__ccbs1
        else:
            kw['command'] = lambda: cmd(*self.__ccbs2.selected)
            targetframe = self.__ccbs2

        for i in mem:
            kw['text'] = i
            bln = tk.BooleanVar()
            bln.set(False)
            kw['variable'] = bln
            targetframe.addCheckbutton(**kw).pack()

    def addButton(self, **kw):

        cmd = kw.pop('command') if 'command' in kw else None
        mem = kw.pop('member') if 'member' in kw else tuple()
        kw['command'] = ft.partial(self.__buttonCommand, cmd, mem)

        return self.__bcbs.addButton(**kw)

    def reset(self):
        self.__ccbs1.cleanFrame()
        self.__ccbs2.cleanFrame()
        self.__bcbs.deselectAll()

