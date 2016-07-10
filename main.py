#!/usr/bin/env python
#-*- coding: utf-8 -*-

import curses, curses.textpad
from secretkey import *
from twython import Twython, TwythonStreamer, TwythonError
from twython.streaming.types import TwythonStreamerTypesStatuses

class MainWindow(object):
    def __init__(self, c_key, c_secret, a_key, a_secret):
        self.win = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.max_y, self.max_x = self.win.getmaxyx()
        self.win.refresh()
        self.mwin = self.win.subwin(self.max_y-2, self.max_x, 0, 0)
        self.cmdwin = self.win.subwin(1, self.max_x, self.max_y-1, 0)
        self.cmdbox = curses.textpad.Textbox(self.cmdwin)
        self.statbar = self.win.subwin(1, self.max_x, self.max_y-2, 0)
        self.statbar.bkgd("-")
        self.statbar.refresh()

        self.change_modename("Waiting")

        self.api = Twython(c_key, c_secret, a_key, a_secret)
        self.streamer = cmaletter_streamer(self, c_key, c_secret, a_key, a_secret)
        
    def main(self):
        while 1:
            key = self.cmdwin.getkey()
            
            if key == "n":
                self.change_modename("tweet mode")
                self.cmdwin.refresh()
                tweet = self.cmdbox.edit()
                self.cmdwin.erase()
                self.cmdwin.refresh()
                self.tweet(tweet)
                self.change_modename("Waiting")
            if key == "q":
                break
            if key == "t":
                self.streamer.on_status({"user":{"name":"maleic"}, "text":"test"})
            if key == ".":
                self.change_modename("Getting latest Tweets...")
                self.get_home_timeline()
                self.change_modename("Waiting")

        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def get_home_timeline(self):
        statuses = self.api.get_home_timeline()
        for status in statuses[::-1]:
            self.on_status(status)

    def tweet(self, tweet):
        self.api.update_status(tweet)

    def change_modename(self, name):
        self.modename = name
        self.statbar_refresh()

    def statbar_refresh(self):
        self.statbar.erase()
        self.statbar.addstr("  (mode:%s)" % self.modename)
        self.statbar.refresh()

    def on_status(self, status):
        self.mwin.addstr("%s: %s\n" % (status['user']['name'], status['text']))
        self.mwin.refresh()
        
class cmaletter_streamer(TwythonStreamer):
    def __init__(self, mainwindow, *args):
        super(cmaletter_streamer, self).__init__(*args)
        self.mainwindow = mainwindow

    def on_status(self, status):
        self.mainwindow.on_status(status)

if __name__ == '__main__':
    win = MainWindow(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
    win.main()

