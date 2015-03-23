#!/usr/bin/env python

import traceback

from Widgets._list import ListWidget
from Widgets._percentage import PercentageWidget


dial = 0


# MAIN MENU callbacks
def main_menu_callback(value):
    global wid
    if value == 0:
        wid = create_light_percentage()
    if value == 1:
        #wid = create_light_percentage()
        pass
    if value == 2:
        wid = create_light_switch_menu()

def create_main_menu():
    my_list = ["Change brightness", "Change scene", "Switch light on/off"]
    return ListWidget(my_list, main_menu_callback)

# light switch menu
def light_switch_menu_callback(value):
    global wid
    if value == 0:
        pass # TODO:
    if value == 1:
        pass # TODO:
    wid = create_main_menu()

def light_switch_menu_cancel_callback():
    global wid
    wid = create_main_menu()

def create_light_switch_menu():
    my_list = ["On", "Off"]
    return ListWidget(my_list, light_switch_menu_callback, light_switch_menu_cancel_callback)


# Light percentage callback
def light_percentage_callback(value):
    global wid
    wid = create_main_menu()
    pass

def create_light_percentage():
    return PercentageWidget(light_percentage_callback, "Change brightness")




wid = create_main_menu()


try:
    import curses
    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.keypad(1)
    dial = 0
    while True:
        wid.dial(dial)
        wid.refresh()

        key = stdscr.getch()
        stdscr.addch(20, 25, key)
        stdscr.refresh()
        if key == curses.KEY_UP:
            dial = (dial - 10) % 300
        if key == curses.KEY_DOWN:
            dial = (dial + 10) % 300
        if key == curses.KEY_RIGHT:
            wid.click()
    curses.endwin()
except (Exception, KeyboardInterrupt):
    curses.endwin()
    traceback.print_exc()

    pass

