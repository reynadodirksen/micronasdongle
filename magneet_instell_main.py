#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 13:26:29 2019

@author: user
"""

import time,sys
import libs.gertbot as gb
import configurations.products as products
import configurations.operators as operators
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from libs.micronas import USBProgrammer
import math
from kivy.uix.textinput import TextInput
import RPi.GPIO as GPIO 
Builder.load_string('''
<RootWidget>:


    Screen:
        name: 'start'
        Button:
            pos: 0, 0
            size_hint: None, None
            size: 100, 50
            on_press: root.current = 'screen1'
            text: 'analyse'

        Spinner:
            text: 'select product'
            values: root.products() 
            size: 200, 50
            pos: 100,  100
            size_hint: None, None
            on_text: root.set_product(self.text)                                                 
            
        Label:
            id: ZTVw
            pos: -400, 430
        Label:
            id: sensw
            pos: -400, 400

        Button:
            text: 'start positioning'
            pos: 800,  50
            size_hint: None, None
            size: 150, 100
            on_press: root.start()


        Label:
            pos: 0, 0
            font_size: 60
            id: progress

        Label:
            pos: 0, -120
            font_size: 40
            id: range

        Label:
            pos: 0, -240
            font_size: 40
            id: sensitivity




















            
    Screen:
        name: 'screen1'

        Label: 
            id: voltage
            pos: 0, -100
        Button:
            text: 'read'
            size_hint: None, None
            size: 100, 50
            pos: 100, 700
            on_press: root.read_voltage_contin()
        Spinner:
            text: 'select product'
            values: root.products() 
            size: 200, 50
            pos: 100,  100
            size_hint: None, None
            on_text: root.set_product(self.text)
        Label:
            id: product
            pos: 500, -450
            font_size: 50

        Button:
            text: 'move left'
            size_hint: None, None
            size: 100, 50
            pos: 600, 65
            on_press: root.move('L')
        Button:
            text: 'move right'
            size_hint: None, None
            size: 100, 50
            pos: 1000, 65
            on_press: root.move('R')
        Button:
            text: 'move up'
            size_hint: None, None
            size: 100, 50
            pos: 800,  180
            on_press: root.move('U')
        Button:
            text: 'move down'
            size_hint: None, None
            size: 100, 50
            pos: 800, 50
            on_press: root.move('D')
        Label:
            text: 'MRANGE 120: '
            pos: -580,  4
        Label:
            text: 'MRANGE 100: '
            pos: -580,  -36
        Label:
            text: 'MRANGE 80: '
            pos: -580,  -76
        Label:
            text: 'MRANGE 60: '
            pos: -580,  -116
        Label:
            text: 'minimum'
            pos: -480,  44
        Label:
            text: 'maximum'
            pos: -360, 44
        Label:
            text: 'MRANGE 40: '
            pos: -580,  -156
        
        TextInput:
            pos: 800, 700
            size_hint: None, None
            text: '0'
            id: steps
            height: 30
            width: 100
        TextInput:
            pos: 110, 500
            size_hint: None, None
            text: '0'
            height: 30
            width: 100
            id: range_120_min
        TextInput:
            pos: 230, 500
            size_hint: None, None
            text: '0'
            height: 30
            width: 100
            id: range_120_max
        TextInput:
            pos: 110, 460
            size_hint: None, None
            text: '0'
            height: 30
            width: 100
            id: range_100_min
        TextInput:
            pos: 230, 460
            size_hint: None, None
            text: '0'
            height: 30
            width: 100
            id: range_100_max
        TextInput:
            pos: 110, 420
            size_hint: None, None
            text: '0'
            height: 30
            width: 100
            id: range_80_min
        TextInput:
            pos: 230, 420
            size_hint: None, None
            text: '0'
            height: 30
            width: 100
            id: range_80_max
        TextInput:
            pos: 110, 380
            size_hint: None, None
            text: '0'
            height: 30
            width: 100
            id: range_60_min
        TextInput:
            pos: 230, 380
            size_hint: None, None
            text: '0'
            height: 30
            width: 100
            id: range_60_max
        TextInput:
            pos: 110, 340
            size_hint: None, None
            text: '0'
            height: 30
            width: 100
            id: range_40_min
        TextInput:
            pos: 230, 340
            size_hint: None, None
            text: '0'
            height: 30
            width: 100
            id: range_40_max




        Label:
            id: success
            pos: 0, 400
        Button:
            text: 'reset label'
            size_hint: None, None
            size: 100, 50
            pos: 1000, 400
            on_press: root.reset_label()

        Label:
            text: '0'
            pos: 400, 400
            font_size: 30
            id: counterLR
        Label:
            text: '0'
            pos: 400, 350
            font_size: 30
            id: counterUD
        Button:
            text: 'reset counter up/down'
            size_hint: None, None
            size: 180, 50
            pos: 1000, 550
            on_press: root.resetUD()

        Button:
            text: 'reset counter left/right'
            size_hint: None, None
            size: 180, 50
            pos: 1000, 600
            on_press: root.resetLR()
        Label:
            text: 'horizontal steps: '
            pos: 250, 400
            font_size: 30
        Label:
            text: 'vertical steps: '
            pos: 250, 350
            font_size: 30

        
        Button:
            pos: 0, 0
            size_hint: None, None
            size: 100, 50
            on_press: root.current = 'start'
            text: 'return'
''')

class RootWidget(ScreenManager):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.micronas = USBProgrammer('/dev/ttyUSB0')
        self.board = 3
        self.chan  = 0
        self.chan2 = 2
        self.setup = dict()
        gb.open_uart(0)
        for i in range(len(sys.argv)) :
          if sys.argv[i][0:2]=="-t" : 
            test = int(sys.argv[i][2:])
          if sys.argv[i][0:2]=="-b" :
            board = int(sys.argv[i][2:])
          if sys.argv[i][0:2]=="-c" :
            chan = int(sys.argv[i][2:])
        gb.set_mode(self.board,self.chan,gb.MODE_STEPG_PWR)
        gb.freq_stepper(self.board,self.chan,1000)#1k = frequency
        gb.set_mode(self.board,self.chan2,gb.MODE_STEPG_PWR)
        gb.freq_stepper(self.board,self.chan2,1000)#1k = frequency
        self.product_declared = 0
        self.V_steps = 0
        self.setup = self.micronas.read_setup()
        self.setup['mrange'] = 1
        self.micronas.write_setup(self.setup)
        self.vpsw = 0.02985 
        self.starting_pos = 'L'
        self.starting_direction = 'R'
        chan_list = [20, 21]
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(chan_list, GPIO.IN)
        print(GPIO.input(20), GPIO.input(21))
        self.schedule_find_zero1 = Clock.schedule_interval(self.find_zero_vertical1, 0.2)
 


    def find_zero_vertical1(self, dt):
        if GPIO.input(21) == 0:
            self.move_vert(100, 'D')
        elif GPIO.input(21) == 1:
            self.schedule_find_zero1.cancel()
            self.schedule_find_zero2 = Clock.schedule_interval(self.find_zero_vertical2, 0.1)

    def find_zero_vertical2(self, dt):
        self.move_vert(10, 'U')
        if (GPIO.input(21) == 0) and (GPIO.input(20) == 1):
            self.schedule_find_zero2.cancel()
            self.move_vert(50, 'U')
            self.zero = 0
            
      



    def set_product(self, text):
        self.defaults = products.defaultValues(text)
        self.ZTVw = float(self.defaults[6])
        self.sensw = float(self.defaults[3])
        self.ids.ZTVw.text = 'gewenste ZTV: ' + str(self.ZTVw) + 'V'
        self.ids.sensw.text = 'gewenste sensitivity: ' + str(self.sensw)
        self.product_declared = 1
        
    def move(self, direction):
        if self.ids.steps.text !='':
            steps = int(self.ids.steps.text)
        else:
            steps = 0
        if direction == 'D' or direction == 'U':
            self.move_vert(steps, direction)
            if direction == 'U':
                self.ids.counterUD.text =  str(int(self.ids.counterUD.text ) +  int(self.ids.steps.text))
            else:
                self.ids.counterUD.text =  str(int(self.ids.counterUD.text ) -  int(self.ids.steps.text))
        else:
            self.move_hor(steps, direction)
            if direction == 'R':
                self.ids.counterLR.text =  str(int(self.ids.counterLR.text ) +  int(self.ids.steps.text))
            if direction == 'L':
                self.ids.counterLR.text =  str(int(self.ids.counterLR.text ) -  int(self.ids.steps.text))
        
    def products(self):
        return products.products()
    
    def reset_label(self):
        self.ids.success.text = ''

    def start(self):
        self.ids.sensitivity.text = ''
        self.ids.range.text = ''
        self.setup = self.micronas.read_setup()
        if self.product_declared == 1:
            if self.micronas.read_continuous_voltage() > 3.6 :
                self.ids.progress.text = 'sensor not connected or '
                self.ids.range.text = 'magnet is in wrong position'
            elif self.setup['locked'] == True:
                self.ids.progress.text = 'sensor is locked '
            else:
                self.ids.sensitivity.text = ''
                self.ids.range.text = ''
                self.move_hor(400, self.starting_direction)
                self.product_declared = 0
                self.setup['mrange'] = int (self.defaults[2])
                self.setup['sensitivity'] = 64
                self.setup['offset'] = 0
                if len(self.defaults) > 9:
                    self.setup['tc'] = int(self.defaults[9])
                    self.setup['tcsq'] = int(self.defaults[10])
                else:
                    self.setup['tc'] = 25
                    self.setup['tcsq'] = -2
                self.setup['alignment'] = True
                self.setup['locked'] = False
                self.micronas.write_setup(self.setup)
                self.lastVoltage = 10
                self.ids.progress.text = 'finding initial magnetic range'
                self.scheduleMin = Clock.schedule_interval(self.find_minimum, 0.2)
        else:
            self.ids.progress.text = 'error: no product selected'

    def find_minimum(self, dt):
        self.move_hor(50, self.starting_direction)
##        time.sleep(0.2)
        Voltage = self.micronas.read_continuous_voltage()
        print(Voltage)
        print(self.lastVoltage)
        if Voltage > self.lastVoltage:
            self.scheduleMin.cancel()
            self.program_new_range()
        else:
            self.lastVoltage = Voltage
      

    def program_new_range(self):
        self.ids.progress.text = 'programming initial range'
        Voltage = self.micronas.read_voltage_out(1)
        range0 = (self.setup['mrange']+1)*20
        self.range0 = self.setup['mrange']+1
        value = ((2.5-Voltage)/2.5)*range0
        if str((value/20)-1)[0] != '-':
            self.range1 = int(str((value/20)-1)[0])
            self.setup['mrange'] = self.range1
            print(self.range1)
        else:
            self.range1 = self.setup['mrange']
        self.micronas.write_setup(self.setup)
        self.schedule4V = Clock.schedule_interval(self.find4V, 0.2)
        

    def find4V(self, dt):
        self.ids.progress.text = 'going to 4 Volts'
        self.move_hor(50, self.starting_direction)
##        time.sleep(0.2)
        Voltage = self.micronas.read_continuous_voltage()
        print(Voltage)
        if Voltage >= 4:
            self.V4 = Voltage
            self.stepsErr = 0
            self.schedule4V.cancel()
            self.shedule_find35V = Clock.schedule_interval(self.find_35V, 0.2)

    def find_35V(self, dt):
        self.ids.progress.text = 'finding approx 3.5 Volts'
        self.move_hor(50, self.starting_pos)
        self.stepsErr +=50
##        time.sleep(0.2)
        Voltage = self.micronas.read_continuous_voltage()
        if Voltage < 3.5:
            self.shedule_find35V.cancel()
            self.steps = 0
            self.schedule_find15V = Clock.schedule_interval(self.find_15V, 0.2)
            self.V35 = Voltage

    def find_15V(self, dt):
        self.ids.progress.text = 'finding approx 1.5 Volts'
        self.move_hor(50, self.starting_pos)
##        time.sleep(0.2)
        self.steps+=50
        Voltage = self.micronas.read_continuous_voltage()
        if Voltage < 1.5:
            self.V15 = Voltage
            self.schedule_find15V.cancel()
            print(self.steps)
            print(self.V35, self.V15)
            self.VperStep = (self.V35-self.V15)/self.steps
            print(self.VperStep)
            self.stepsExtra = self.stepsErr-((self.V4-self.V35)/self.VperStep)
            print(self.stepsExtra)
            print(Voltage) 
            
            tempo = (self.VperStep/self.vpsw)*((self.range1+1)*20)
            self.range2 = round(tempo/20)-1
            self.setup['mrange'] = self.range2
            self.ids.progress.text = 'programming final range'
            print(self.range2)
            
            self.micronas.write_setup(self.setup)
            range1 = (self.range1+1)*20
            range2 = (self.range2 + 1)*20
            self.VperStep = self.VperStep*(range1/range2)
            self.currentVoltage = self.micronas.read_continuous_voltage()
            
            self.theoreticalV = 2.5 - (2.5-Voltage)*(range1/range2)
            turn_steps = round(self.stepsExtra*0.75)
            self.ids.progress.text = 'setting magnet to final point'
            if self.theoreticalV > 0:
                if self.currentVoltage >= 0.6*self.ZTVw:
                    if self.currentVoltage > 0.9*self.ZTVw:
                        steps = (0.75*self.ZTVw-self.currentVoltage)/self.VperStep
                        self.move_hor(steps, self.starting_pos)
                        self.move_hor(20, self.starting_direction)
                else:
                    self.move_hor(turn_steps, self.starting_direction)
                    self.scheduleMove = Clock.schedule_interval(self.move_to_desired_point, 0.1)
            else:
                    self.move_hor(turn_steps, self.starting_direction)
                    self.scheduleMove = Clock.schedule_interval(self.move_to_desired_point, 0.1)


    def move_to_desired_point(self, dt):
        steps = round(0.15/self.VperStep)
        self.move_hor(steps, self.starting_direction)
        Voltage = self.micronas.read_continuous_voltage()
        if Voltage > 0.6*self.ZTVw:
            self.scheduleMove.cancel()
            if Voltage < 0.75*self.ZTVw:
                steps = round((Voltage-(self.ZTVw * 0.75))/self.VperStep)
                self.move_hor(steps, self.starting_direction)
                print(self.micronas.read_continuous_voltage())
                self.move_hor(20, self.starting_pos)
                self.end()
            else:
                self.move_hor(20, self.starting_pos)
                self.end()
                
            if Voltage > 0.9*self.ZTVw:
                print('please god no')
                

            
    def end(self):
        Voltage = self.micronas.read_voltage_out(20)
        self.ids.progress.text = 'Done! Final Voltage: ' + str("%0.3f" % (Voltage) )+ 'Volts'
        self.setup = self.micronas.read_setup()
        Mrange = (int(self.setup['mrange']) +1)*20
        self.ids.range.text = 'Magnetic Range: ' + str(Mrange) + '( = ' + str(self.setup['mrange']) + ')'
        print(self.VperStep)
        sens = round(((self.VperStep/self.vpsw)*75), 1)
        self.ids.sensitivity.text = 'approx. sensitivity: ' + str(sens)
        if sens <60:
            self.ids.sensitivity.text = 'sensitivity is too low. approx. sensitivity: ' + str(sens)
        if sens >90:
            self.ids.sensitivity.text = 'sensitivity is too high. approx. sensitivity: ' + str(sens)
        self.product_declared = 1
 

                  
   
            
    def resetLR(self):
        self.ids.counterLR.text = '0'

    def  resetUD(self):
        self.ids.counterUD.text = '0'
        
            
    def move_hor(self, steps, direction):
        if direction == 'L':
            steps = 0-steps
        gb.move_stepper(self.board,self.chan,steps)

    def move_vert(self, steps, direction):
        if direction == 'U':
            steps = 0-steps
        gb.move_stepper(self.board,self.chan2, steps)
    def read_voltage_contin(self):
        self.ids.range_80_max.text = str(self.micronas.read_voltage_out(1))

    def round_down(self, n,  decimals=0):
        multiplier = 10 ** decimals
        return math.floor(n * multiplier) / multiplier
                            
class setup(App):
    def on_stop(self):
        
        gb.emergency_stop()
        self.root_window.close()
        

    def build(self):
        return RootWidget()


if __name__ == '__main__':
    
    Window.fullscreen = 'auto'
    
    setup().run()
