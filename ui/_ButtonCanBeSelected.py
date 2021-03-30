#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk

class _ManyButtonsCreater:
    def __init__(self, master):
        self.__master = master

    def addButton(self, **kw):
        return tk.Button(self.__master, **kw)


class _ButtonCanBeSelected(_ManyButtonsCreater):

    def deselectAll():
        pass


def _selectButton(btn):
    btn['state'] = 'disable'


def _deselectButton(btn):
    btn['state'] = 'active'


class OnlyOneButtonCanBeSelected(_ButtonCanBeSelected):
    def __init__(self, master):
        super().__init__(master)
        self.__selected = None

    def __buttonClicked(self, btn):
        if self.__selected != None:
            _deselectButton(self.__selected)
        self.__selected = btn
        _selectButton(btn)

    def __clickCommand(self, btn, cmd):
        self.__buttonClicked(btn)
        if cmd is not  None:
            cmd()

    def addButton(self, **kw):
        if 'command' in kw:
            cmd = kw.pop('command')
        else:
            cmd = None
        btn = super().addButton(**kw)
        btn['command'] = lambda: self.__clickCommand(btn, cmd)
        return btn

    def deselectAll(self):
        if self.__selected is not None:
            _deselectButton(self.__selected)
            self.__selected = None


class OnlyTowButtonCanBeSelected(_ButtonCanBeSelected):
    def __init__(self, master: tk.Widget):
        super().__init__(master)
        self.__selected = []

    def __buttonClicked(self, btn):
        self.__selected.append(btn)
        _selectButton(btn)

    def __clickCommand(self, btn, cmd):
        if len(self.__selected) < 2:
            self.__buttonClicked(btn)
            if cmd is not None:
                cmd()

    def addButton(self, **kw):
        if 'command' in kw:
            cmd = kw.pop('command')
        else:
            cmd = None
        btn = super().addButton(**kw)
        btn['command'] = lambda: self.__clickCommand(btn, cmd)
        return btn

    def deselectAll(self):
        while self.__selected:
            _deselectButton(self.__selected.pop())

    @property
    def count(self):
        return len(self.__selected)

