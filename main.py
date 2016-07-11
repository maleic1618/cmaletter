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
        self.win.refresh()
        self.mwin = self.win.subwin(self.max_y-2, self.max_x, 0, 0)
        self.mwin.scrollok(True)
        self.cmdbar = self.win.subwin(1, self.max_x, self.max_y-1, 0)
        self.statbar = self.win.subwin(1, self.max_x, self.max_y-2, 0)
        self.statbar.bkgd("-")

        self.latest_id = 0
        self.loaded_statuses = []
        

        self.plugin = []
        self.key_bind = {}
        self.add_plugin(default_plugin(self))
        self.change_modename("Waiting")

        self.api = Twython(c_key, c_secret, a_key, a_secret)
        self.streamer = cmaletter_streamer(self, c_key, c_secret, a_key, a_secret)

        self.get_home_timeline(num = 40)
        
    def main(self):
        while 1:
            key = self.cmdbar.getkey()

            if key == "q":
                break
            
            if key in self.key_bind:
                name, func = self.key_bind[key]
                self.change_modename(name)
                func(self.mwin)
                self.change_modename("Waiting")

                curses.curs_set(0)

            self.show_timeline()

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
        return self.loaded_statuses
            
    def user_input(self):
        self.cmdbar.erase()
        self.cmdbar.refresh()
        curses.echo()
        input = self.cmdbar.getstr()
        curses.noecho()
        return input

    def fit_window(self):
        self.max_y, self.max_x = self.win.getmaxyx()
        self.mwin.resize(self.max_y-2, self.max_x)
        self.mwin.mvwin(0,0)
        self.statbar.resize(1,self.max_x)
        self.statbar.mvwin(self.max_y-2, 0)
        self.cmdbar.resize(1, self.max_x)
        self.cmdbar.mvwin(self.max_y-1, 0)
        self.win.refresh()
        
    def show_timeline(self, all=False):
        self.fit_window()
        self.mwin.erase()
        length = len(self.loaded_statuses)
        if all == True:
            show_range = range(length)
        else:
            show_range = range(max(0, length-self.max_y), length)

        for i in show_range:
            status = self.loaded_statuses[i]
            self.mwin.addstr("\n%s:%s" % (status['user']['screen_name'], status['text']))
        self.mwin.refresh()
    
    def tweet(self, content, in_reply_to=None):
        if in_reply_to == None:
            self.api.update_status(status=content)
        else:
            self.api.update_status(status=content, in_reply_to_status_id=in_reply_to) 

    def retweet(self, id):
        self.api.retweet(id=id)

    def create_favorite(self, id):
        self.api.create_favorite(id=id)
        
    def change_modename(self, name):
        self.modename = name
        self.statbar_refresh()

    def statbar_refresh(self):
        self.statbar.erase()
        self.statbar.addstr("  (%s)" % self.modename)
        self.statbar.refresh()

    def cmdbar_output(self, text):
        self.cmdbar.erase()
        self.cmdbar.addnstr(text, self.max_x)
        self.cmdbar.refresh()
        
    def on_status(self, status):
        self.mwin.addstr("%s: %s\n" % (status['user']['screen_name'], status['text']))
        self.mwin.refresh()
        self.loaded_statuses.append(status)
        
class cmaletter_streamer(TwythonStreamer):
    def __init__(self, mainwindow, *args):
        super(cmaletter_streamer, self).__init__(*args)
        self.mainwindow = mainwindow

    def on_status(self, status):
        self.mainwindow.on_status(status)

if __name__ == '__main__':
    win = MainWindow(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
    win.main()

