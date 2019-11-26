# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 13:26:29 2019

@author: user
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
#from micronas import USBProgrammer
Builder.load_string('''
<RootWidget>:
    Screen:
        name: 'screen1'
        Button: 
            text: 'left'
            size_hint: None, None
            size: 100, 50
            pos: 550, 550
            on_press: root.test()
        Label: 
            text: 'SCREEN 1'
    Screen:
        name: 'screen2'
        Label: 
            text: 'SCREEN 2'
''')

class RootWidget(ScreenManager):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def test(self):
        self.current = 'screen2'

class setup(App):
    def on_stop(self):
        self.root_window.close()
        

    def build(self):
        return RootWidget()


if __name__ == '__main__':
    
    Window.fullscreen = 'auto'
    
    setup().run()