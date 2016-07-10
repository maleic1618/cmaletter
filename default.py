#!/usr/bin/env python
#!-*-coding:utf-8-*-

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

    def tweet(self):
        content = self.main_cls.user_input()
        if content != "":
            self.main_cls.tweet(content)

    def timeline_update(self):
        self.main_cls.get_home_timeline()
