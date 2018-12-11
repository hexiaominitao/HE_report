#!/usr/bin/python3

'''
@author:Hemin
@date:2018-11-30
@contact:a8013heming@gmail.com
'''

import pyinotify
import os



class MyEventHandler(pyinotify.ProcessEvent):

    def process_IN_CREATE(self,event):
        name = event.pathname
        print(name)
        if name.endswith("fastq_qc"):
            return name



def watch_dir(dir):
    wm =pyinotify.WatchManager()
    wm.add_watch(dir,pyinotify.ALL_EVENTS,rec=True)
    eh = MyEventHandler()
    notifiter = pyinotify.Notifier(wm,eh)
    notifiter.loop()


if __name__ == "__main__":
    watch_dir()