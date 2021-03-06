#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# -----------------------------------------------------------------------------
# Getting Things GNOME! - A personal organizer for the GNOME desktop
# Copyright (c) 2008-2013 Lionel Dricot & Bertrand Rousseau
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------

"""
GTG stress test
"""
import sys
import dbus
import uuid

def connect():
    # We will connect on the session bus
    bus = dbus.SessionBus()
    liste = bus.list_names()
    busname = "org.gnome.GTG"
    remote_object = bus.get_object(busname,"/org/gnome/GTG")
    return dbus.Interface(remote_object,dbus_interface="org.gnome.GTG")

if __name__ == '__main__':
    if len(sys.argv) == 1:
         print("Usage: " + sys.argv[0] + " <number-of-tasks> [number-of-words-in-bodies]")
         sys.exit(1)
    total_tasks = int(sys.argv[1])

    text_length = 0
    if len(sys.argv) > 2:
        text_length = int(sys.argv[2])

    gtg = connect()
    for i in range(total_tasks):
        lengthy_text = ""
        for i in range(text_length):
            lengthy_text += str(uuid.uuid4())
        gtg.NewTask("Active", str(uuid.uuid4()), '', '', '', [], lengthy_text, [])
