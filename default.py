#!/usr/bin/env python
#!-*-coding:utf-8-*-

import curses

class plugin_function(object):
    def __init__(self):
        self.cmd_list = [] #(name, func, bind)
        
    def on_status(self, status):
        pass

class default_plugin(plugin_function):
    def __init__(self, main_cls):
        super(default_plugin, self).__init__()
        self.main_cls = main_cls
        self.cmd_list.append(("tweet", self.tweet, "n"))
        self.cmd_list.append(("update", self.timeline_update, "."))
        self.cmd_list.append(("read timeline", self.read_timeline, "r"))

    def tweet(self):
        content = self.main_cls.user_input()
        if content != "":
            self.main_cls.tweet(content)

    def timeline_update(self):
        self.main_cls.get_home_timeline()

    def read_timeline(self):
        loaded_status = self.main_cls.get_loaded_status()
        length = len(loaded_status)
        swin = self.main_cls.win.subwin(self.main_cls.max_y-3, self.main_cls.max_x, 0,0)
        swin.scrollok(True)
        for i in range(length-1, 0, -1):
            status = loaded_status.reverse()[i]
            if i == 0:
                swin.addstr("%d:%s:%s"%(i, status['user']['name'], status['text']), curses.A_REVERSE)
            else:
                swin.addstr("%d:%s:$s"%(i, status['user']['name'], status['text']))
        swin.refresh()
        curses.delay_output(2000)
        swin.clearok(1)                    
