#!/usr/bin/env python3

import tkinter as tk
import tkinter.ttk as ttk

PAD = 3

class ManyBuutonsPacker:
    def __init__(self, width):
        self.__width = width
        self.__counter = 0

    def pack(self, w: tk.Widget):
        rtn = w.grid(padx=PAD, pady=PAD, row=int(self.__counter/self.__width), column=self.__counter%self.__width)
        self.__counter += 1
        return rtn

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, bar_x = True, bar_y = True):
        super().__init__(container)
        self.canvas = tk.Canvas(self)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        if bar_y:
            self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
            self.scrollbar_y.pack(side=tk.RIGHT, fill="y")
            self.canvas.configure(yscrollcommand=self.scrollbar_y.set)
        if bar_x:
            self.scrollbar_x = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
            self.scrollbar_x.pack(side=tk.BOTTOM, fill="x")
            self.canvas.configure(xscrollcommand=self.scrollbar_x.set)
        self.canvas.pack(side=tk.LEFT, fill="both", expand=True)

class FrameMaker:
    def __init__(self, master):

        u = tk.Frame(master)
        u.pack(padx=PAD, pady=PAD, side=tk.TOP)

        d = ScrollableFrame(master)
        d.pack(padx=PAD, pady=PAD, side=tk.TOP)

        ul = tk.Frame(u)
        ul.pack(padx=PAD, pady=PAD, side=tk.LEFT)

        ur = tk.Frame(u)
        ur.pack(padx=PAD, pady=PAD, side=tk.LEFT)

        self.__upperleft = ul
        self.__upperright = ur
        self.__down = d.scrollable_frame

    @property
    def upperleft(self):
        return self.__upperleft

    @property
    def upperright(self):
        return self.__upperright

    @property
    def down(self):
        return self.__down

def destroy_child(frame: tk.Frame):
    children = frame.winfo_children()
    for child in children:
        child.destroy()
