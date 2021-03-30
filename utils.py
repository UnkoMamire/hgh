#!/usr/bin/env python3

class _fpf:
    def __init__(self, f1, f2):
        self.__f1 = f1
        self.__f2 = f2

    def __func(self):
        self.__f1()
        self.__f2()

    def func(self):
        return lambda: self.__func()

def fpf(f1, f2):
    '''
    関数同士をつなぎ合わせるだけ
    '''
    return _fpf(f1,f2).func()

