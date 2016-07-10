#!/usr/bin/env python
#-*- coding: utf-8 -*-

import locale
import curses, curses.textpad
from default import *
from secretkey import *
from twython import Twython, TwythonStreamer, TwythonError
from twython.streaming.types import TwythonStreamerTypesStatuses

class MainWindow(object):
    def __init__(self, c_key, c_secret, a_key, a_secret):
        self.win = curses.initscr()
        curses.noecho()
        curses.cbreak()
        locale.setlocale(locale.LC_ALL, "")
        self.max_y, self.max_x = self.win.getmaxyx()
        self.win.scrollok(True)
        self.win.refresh()
        self.mwin = self.win.subwin(self.max_y-2, self.max_x, 0, 0)
        self.cmdwin = self.win.subwin(1, self.max_x, self.max_y-1, 0)
        #self.cmdbox = curses.textpad.Textbox(self.cmdwin)
        self.statbar = self.win.subwin(1, self.max_x, self.max_y-2, 0)
        self.statbar.bkgd("-")
        self.statbar.refresh()
        self.latest_id = 0
        self.loaded_status = []
        

        self.plugin = []
        self.key_bind = {}
        self.add_plugin(default_plugin(self))
        self.change_modename("Waiting")

        self.api = Twython(c_key, c_secret, a_key, a_secret)
        self.streamer = cmaletter_streamer(self, c_key, c_secret, a_key, a_secret)

        self.get_home_timeline(num = 20)
        
    def main(self):
        while 1:
            key = self.cmdwin.getkey()

            if key == "q":
                break
            
            if key in self.key_bind:
                curses.curs_set(2)
                
                name, func = self.key_bind[key]
                self.change_modename(name)
                func()
                self.change_modename("Waiting")

                curses.curs_set(0)

        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def add_plugin(self, cls):
        self.plugin.append(cls)
        for name, func, bind in cls.cmd_list:
            self.key_bind[bind] = (name, func)
        
    def get_home_timeline(self, num=-1):
        if num == -1:
            statuses = self.api.get_home_timeline(since_id = self.latest_id)
        else:
            statuses = self.api.get_home_timeline(count = num)
            
        for status in statuses[::-1]:
            self.on_status(status)
            self.latest_id = status['id']

    def get_loaded_status(self):
        return self.loaded_status
            
    def user_input(self):
        self.cmdwin.refresh()
        curses.echo()
        input = self.cmdwin.getstr()
        curses.noecho()
        self.cmdwin.erase()
        self.cmdwin.refresh()
        return input
        
    def tweet(self, content):
        self.api.update_status(status=content)

    def change_modename(self, name):
        self.modename = name
        self.statbar_refresh()

    def statbar_refresh(self):
        self.statbar.erase()
        self.statbar.addstr("  (%s)" % self.modename)
        self.statbar.refresh()

    def on_status(self, status):
        self.mwin.addstr("%s: %s\n" % (status['user']['name'], status['text']))
        self.mwin.refresh()
        self.loaded_status.append(status)
        
class cmaletter_streamer(TwythonStreamer):
    def __init__(self, mainwindow, *args):
        super(cmaletter_streamer, self).__init__(*args)
        self.mainwindow = mainwindow

    def on_status(self, status):
        self.mainwindow.on_status(status)

if __name__ == '__main__':
    win = MainWindow(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
    win.main()

