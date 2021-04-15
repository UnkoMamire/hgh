#!/usr/bin/env python3

import ParticipantManager
import ui
import delivery
import obscontrol
import copy
import utils

import functools as ft
import copy as cp


def trainsition(scene: list):
    for item in scene:
        item.align()


def onlyOne(teams, u, desc, text, scene):
    d = delivery._FewStreamManager(desc, 1)

    tab = u.addTab(text)
    fr = ui.FrameDesignerD(tab, d.reset, ft.partial(trainsition, scene))

    for i in teams:
        for j in teams[i]:
            url = teams[i][j].videoURL
            cmd = d.reset if url is None else utils.fpf(d.reset, ft.partial(d.setURL, cp.copy(url)))
            fr.add(text = '{0} - {1}'.format(i, j), command = cmd)

    return tab


def OnevOne(teams, u, desc, text, scene):
    d = delivery._FewStreamManager(desc, 2)

    tab = u.addTab(text)
    fr = ui.FrameDesignerB(tab, d.reset, ft.partial(trainsition, scene))

    for i in teams:
        for j in teams[i]:
            url = teams[i][j].videoURL
            if url is not None:
                cmd = ft.partial(d.setURL, cp.copy(url))
            fr.add(text = '{0} - {1}'.format(i, j), command = cmd)

    return tab


def OneTeam(teams, u, desc, text, scene):
    d = delivery._FewStreamManager(desc, 3)

    tab = u.addTab(text)
    fr = ui.FrameDesignerB(tab, d.reset, ft.partial(trainsition, scene))

    for i in teams:
        urls = [teams[i][j].videoURL for j in teams[i] if teams[i][j] is not None]
        cmd = utils.fpf(d.reset, ft.partial(d.setURL, *cp.copy(urls)))
        fr.add(text = i, command=cmd)

    return tab


def TowvTow(teams, u, desc, text, scene):
    d = delivery._ManySteamManager(desc, 2, 2)

    tab = u.addTab(text)
    fr = ui.FrameDesignerA(tab, d.reset, ft.partial(trainsition, scene))

    for i in teams:

        mem = teams[i].keys()

        def cmd(team, *selmem):
            d.setURL(id(team), *[team[j].videoURL for j in selmem])

        fr.add(text=i, command=ft.partial(cmd, cp.copy(teams[i])), member=mem)


    return tab

def OptionTab(u: ui.UI, text: str, listreload):
    tab = u.addTab(text)
    fr = ui.FrameDesignerC(tab)

    fr.add(text='リスト再読込', command = listreload)

    return tab

def imptabCreate(teams: ParticipantManager.Participant, u: ui.tk.Widget):

    imptab = list()
    db = obscontrol.read_db()

    imptab.append(onlyOne(teams, u, 49513, '一人視点 A', db['1a']))
    imptab.append(onlyOne(teams, u, 49514, '一人視点 B', db['1b']))

    imptab.append(OnevOne(teams, u, 49515, '1vs1 A', db['2a']))
    imptab.append(OnevOne(teams, u, 49517, '1vs1 B', db['2b']))

    imptab.append(OnevOne(teams, u, 49519, '収容所 A', db['ga']))
    imptab.append(OnevOne(teams, u, 49521, '収容所 B', db['gb']))

    imptab.append(OneTeam(teams, u, 49523, '1チーム視点 A', db['3a']))
    imptab.append(OneTeam(teams, u, 49526, '1チーム視点 B', db['3b']))

    TowvTow(teams, u, 49529, '2vs2 A', db['4a'])
    TowvTow(teams, u, 49533, '2vs2 B', db['4b'])

    return imptab

def main():
    teams = ParticipantManager.readFile()
    u = ui.UI()

    imptab = imptabCreate(teams, u)

    def listreload():
        teams = ParticipantManager.readFile()
        u.destroy()
        main()
    OptionTab(u, 'オプション', listreload)

    u.mainloop()


if __name__ == '__main__':
    main()
