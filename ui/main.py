#!/usr/bin/env python3

import tkinter as tk
import functools as ft

from ._utils import *
from ._ButtonCanBeSelected import *

from . import _CheckbuttonFromButtons as cbfb

RESETBUTTONTEXT = 'リセット'
TRANSITIONBUTTONTEXT = 'トランジション'

class FrameDesignerA:
    '''
    ボタンを押すと左上にチェックボタンが現れます。ボタンは2個まで押せます。
    '''

    def __init__(self, master, resetfunc, transfunc):

        self.__packer = ManyBuutonsPacker(12)

        frames = FrameMaker(master)

        cbframe1 = tk.Frame(frames.upperleft)
        cbframe1.pack(side=tk.LEFT)

        cbframe2 = tk.Frame(frames.upperleft)
        cbframe2.pack(side=tk.LEFT)

        self.__cbfb = cbfb.CheckbuttonFromButtons(frames.down, cbframe1, cbframe2)

        def reset():
            resetfunc()
            self.__cbfb.reset()
        resetbutton = tk.Button(frames.upperright, text=RESETBUTTONTEXT, command=reset, height=3)
        resetbutton.pack(padx=PAD, pady=PAD, side=tk.LEFT)

        transbutton = tk.Button(frames.upperright, text=TRANSITIONBUTTONTEXT, command=transfunc, height=3)
        transbutton.pack(padx=PAD, pady=PAD, side=tk.LEFT)


    def add(self, **kw):

        kw.setdefault('width', 12)

        btn = self.__cbfb.addButton(**kw)
        self.__packer.pack(btn)

class FrameDesignerB:
    '''
    ボタンを2個まで押せます。
    '''

    def __init__(self, master, resetfunc, transfunc):
        self.__packer = ManyBuutonsPacker(6)
        self.__resetfunc = resetfunc
        self.__transfnuc = transfunc

        frames = FrameMaker(master)

        resetbutton = tk.Button(frames.upperright, text=RESETBUTTONTEXT, command=self.reset, height=3)
        resetbutton.pack(padx=PAD, pady=PAD, side=tk.LEFT)

        transbutton = tk.Button(frames.upperright, text=TRANSITIONBUTTONTEXT, command=transfunc, height=3)
        transbutton.pack(padx=PAD, pady=PAD, side=tk.LEFT)

        self.__mbc = OnlyTowButtonCanBeSelected(frames.down)

    def __buttonCommand(self, cmd):
        if cmd is not None:
            cmd()

    def add(self, **kw):

        kw.setdefault('width', 27)

        btn = self.__mbc.addButton(**kw)
        self.__packer.pack(btn)

    def reset(self):
        self.__resetfunc()
        self.__mbc.deselectAll()


class FrameDesignerC:
    def __init__(self, master):
        self.__master = master

    def add(self, **kw):
        btn = tk.Button(self.__master, **kw)
        btn.pack()

class FrameDesignerD:
    '''
    ボタンは1個しか押せません。
    '''

    def __init__(self, master, resetfunc, transfunc):
        self.__packer = ManyBuutonsPacker(6)
        self.__resetfunc = resetfunc
        self.__transfnuc = transfunc

        frames = FrameMaker(master)

        resetbutton = tk.Button(frames.upperright, text=RESETBUTTONTEXT, command=self.reset, height=3)
        resetbutton.pack(padx=PAD, pady=PAD, side=tk.LEFT)

        transbutton = tk.Button(frames.upperright, text=TRANSITIONBUTTONTEXT, command=transfunc, height=3)
        transbutton.pack(padx=PAD, pady=PAD, side=tk.LEFT)

        self.__mbc = OnlyOneButtonCanBeSelected(frames.down)

    def __buttonCommand(self, cmd):
        if cmd is not None:
            cmd()

    def add(self, **kw):

        kw.setdefault('width', 27)

        btn = self.__mbc.addButton(**kw)
        self.__packer.pack(btn)

    def reset(self):
        self.__resetfunc()
        self.__mbc.deselectAll()


class UI(tk.Tk):
    '''
    タブ付きウィンドウを作る
    '''

    def __init__(self):
        super().__init__()
        self.__notebook = ttk.Notebook(self)
        self.__notebook.pack()
        self.__cmdlist = {}
        self.__openingtab = None

    def addTab(self, text = '', openfunc = None, closefunc = None):
        frame = tk.Frame(self.__notebook)
        self.__notebook.add(frame, text = text)
        return frame

