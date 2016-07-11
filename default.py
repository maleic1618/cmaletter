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

    def tweet(self, win):
        content = self.main_cls.user_input()
        if content != "":
            self.main_cls.tweet(content)

    def timeline_update(self, win):
        self.main_cls.get_home_timeline()

    def read_timeline(self, win):
        statuses = self.main_cls.get_loaded_status()[:]
        length = len(statuses)
        #swin = self.main_cls.win.subwin(self.main_cls.max_y-3, self.main_cls.max_x, 0,0)
        win.move(0,0)
        win.scrollok(True)
        statuses.reverse()
        self.show(win, statuses, 0)
        col = 0

        while 1:
            key = win.getkey()

            if key == 'q':
                break
            elif key == 'k':
                col = min(col+1, length-1)
                self.show(win, statuses, col)
            elif key == 'j':
                col = max(col-1, 0)
                self.show(win, statuses, col)
            elif key == 't':
                self.main_cls.retweet(statuses[col]['id'])
                self.main_cls.cmdbar_output("retweet:%d" % col)
            elif key == 'r':
                content = self.main_cls.user_input()
                if content != "":
                    self.main_cls.tweet(content=content, in_reply_to=statuses[col]['id'])
                    self.main_cls.cmdbar_output("reply:%d" % col)
            elif key == 'l':
                self.main_cls.create_favorite(statuses[col]['id'])
                self.main_cls.cmdbar_output("like:%d" % col)
            

    def show(self, win, statuses, num):
        length = len(statuses)
        max_y, max_x = win.getmaxyx()
        win.erase()
        win.move(max_y-1, 0)

        #2つ目のparamをmax(-1, num-2)とすれば選択しているツイートの次まで表示される
        for i in range(min(length-1,num+max_y-1) , num-1, -1):
            status = statuses[i]
            if i == num:
                win.addstr("\n%d:%s:%s" % (i, status['user']['screen_name'], status['text']), curses.A_REVERSE)
            else:
                win.addstr("\n%d:%s:%s" % (i, status['user']['screen_name'], status['text']))
        win.refresh()
        
