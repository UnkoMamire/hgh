#!/usr/bin/env python3

import ParticipantManager
import ui
import obscontrol
import copy
import utils

import functools as ft
import copy as cp

def onlyOne(teams, u, scene, text):

    tab = u.addTab(text)
    fr = ui.FrameDesignerD(tab, scene[0].seturl(''), lambda: print("トランジションした体"))

    for i in teams:
        for j in teams[i]:
            url = teams[i][j].videoURL
            cmd = scene[0].seturl('') if url is None else utils.fpf(scene[0].seturl(''), ft.partial(scene[0].seturl(url), cp.copy(url)))
            fr.add(text = '{0} - {1}'.format(i, j), command = cmd)

    return tab


def OnevOne(teams, u, desc, text):
    d = delivery._FewStreamManager(desc, 2)

    tab = u.addTab(text)
    fr = ui.FrameDesignerB(tab, d.reset, lambda: print("トランジションした体"))

    for i in teams:
        for j in teams[i]:
            url = teams[i][j].videoURL
            if url is not None:
                cmd = ft.partial(d.setURL, cp.copy(url))
            fr.add(text = '{0} - {1}'.format(i, j), command = cmd)

    return tab


def OneTeam(teams, u, desc, text):
    d = delivery._FewStreamManager(desc, 3)

    tab = u.addTab(text)
    fr = ui.FrameDesignerB(tab, d.reset, lambda: print("トランジションした体"))

    for i in teams:
        urls = [teams[i][j].videoURL for j in teams[i] if teams[i][j] is not None]
        cmd = utils.fpf(d.reset, ft.partial(d.setURL, *cp.copy(urls)))
        fr.add(text = i, command=cmd)

    return tab


def TowvTow(teams, u, desc, text):
    d = delivery._ManySteamManager(desc, 2, 2)

    tab = u.addTab(text)
    fr = ui.FrameDesignerA(tab, d.reset, lambda: print('トランジションした体'))

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

    imptab.append(onlyOne(teams, u, 49513, '一人視点 A'))
    imptab.append(onlyOne(teams, u, 49514, '一人視点 B'))

    imptab.append(OnevOne(teams, u, 49515, '1vs1 A'))
    imptab.append(OnevOne(teams, u, 49517, '1vs1 B'))

    imptab.append(OnevOne(teams, u, 49519, '収容所 A'))
    imptab.append(OnevOne(teams, u, 49521, '収容所 B'))

    imptab.append(OneTeam(teams, u, 49523, '1チーム視点 A'))
    imptab.append(OneTeam(teams, u, 49526, '1チーム視点 B'))

    TowvTow(teams, u, 49529, '2vs2 A')
    TowvTow(teams, u, 49533, '2vs2 B')

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
