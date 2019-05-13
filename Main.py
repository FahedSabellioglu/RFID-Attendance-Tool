from kivy.app import  App
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
import Functions
import calendar
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.cache import Cache
from kivy.core.window import Window
from kivy.modules import inspector
from Arduino import *
from kivy.clock import Clock
from functools import partial
from SQL import *
import serial
Window.size = (800, 600)

Functions.load_string("Month")

class Months(BoxLayout):
    def __init__(self,**kwargs):
        super(Months,self).__init__(**kwargs)


class UserAttendance(Screen):
    Functions.load_string("UserAttendance")
    def on_pre_enter(self, *args):
        if Cache.get("counter","value") == None:
            Functions.Calendar(self,2)
        else:
            Functions.Calendar(self,Cache.get("counter","value"))
    def Exit(self):
        pages.append(LoginPage(name="LoginPage"))
        Functions.ChangePage(pages,screen)

    @staticmethod
    def callback(self):
        weekNumber = int(self.text.split()[-1])
        if Cache.get("counter",'value') == None:
            Cache.append("counter", 'value', weekNumber)
        else:
            Cache.remove("counter","value")
            Cache.append("counter",'value',weekNumber)
        pages.append(UserAttendance(name="UserAttendance"))
        Functions.ChangePage(pages,screen)

    @staticmethod
    def on_release(self):
        Functions.NotePopUp(self,self.text)




class LoginPage(Screen):
    Functions.load_string("LoginPage")

    def on_enter(self, *args):
        Clock.schedule_interval(self.scan,2)
    def scan(self,dt):
        self.ids['st_id'].text = ''
        self.ids['st_name'].text = ''
        if Cache.get('id','user') != None:
            value = card_exist(Cache.get('id','user'))
            if len(value) == 0:
                Clock.unschedule(self.scan)
                Functions.new_card_pop(self)
            else:
                values = attendance(Cache.get('id','user'))
                if values == 1:
                    self.ids['st_id'].text = str(value[0][3])
                    self.ids['st_name'].text = value[0][0] + " "+ value[0][1]
                    self.ids['st_warn'].opacity = 0
                elif values == 0:
                    self.ids['st_warn'].opacity = 1

    def OnLogin(self):
        pages.append(AttendanceLogin(name="LoginPage"))
        Functions.ChangePage(pages,screen)

    def LoginCre(self):
        if Functions.AttendanceLogin(self) and self.ids['CheckLogin'].active==True:
            pages.append(Admin_Page(name="Admin_Page"))
            Functions.ChangePage(pages, screen)
        elif Functions.AttendanceLogin(self) and self.ids['CheckLogin'].active==False:
            pages.append(UserAttendance(name='User_page'))
            Cache.append("user", "login", self.ids["input_id"].text)
            Cache.append('counter','value',1)
            Functions.ChangePage(pages,screen)

    def CheckButtonControl(self):
        if self.ids["CheckLogin"].active == True:
            self.ids['warning'].opacity = 0
            self.ids["input_pass"].opacity = 1
            self.ids["input_pass"].disabled = False
            self.ids["login_passw"].opacity = 1
            self.ids["input_id"].pos_hint = {"center_x": .65, "center_y": .520}
            self.ids['login_id'].pos_hint = {"center_x": .40, "center_y": .520}
            self.ids["input_pass"].pos_hint = {"center_x": .65, "center_y": .370}
        else:
            self.ids['warning'].opacity = 0
            self.ids["input_pass"].opacity = 0
            self.ids["login_passw"].opacity = 0
            self.ids["input_pass"].disabled = True
            self.ids["login_id"].pos_hint = {"center_x": .40, "center_y": .420}
            self.ids["input_id"].pos_hint = {"center_x": .65, "center_y": .420}


class Admin_Page(Screen):
    Functions.load_string("Admin_Page")
    def on_pre_enter(self, *args):
        Functions.on_pre_enter(self)
    def profile(self):
        Functions.profile(self)
    def del_students(self):
        Functions.on_delete(self)

class AttendanceApp(App):
    def build(self):
        inspector.create_inspector(Window,self)
        try:
            self.arduino = serial.Serial(
            port='COM3',
            baudrate=9600)
        except:
            pass

        Clock.schedule_interval(self.update,5)
        screen.current = "LoginPage"
        return screen
    def update(self,*args):
        self.new = self.arduino
        line = self.new.readline(self.new.inWaiting())
        self.new.flush()
        self.new.flushInput()
        self.new.flushOutput()
        print line.split()
        if len(line.split()) != 0 and "FF" not in line:
            if Cache.get('id', 'user') == None:
                Cache.append('id', 'user', line.strip())
            else:
                Cache.remove('id', 'user')
                Cache.append('id', 'user', line.strip())


pages = [LoginPage(name="LoginPage"),
         ]
Cache.register('counter',limit=1)
Cache.register("User",limit = 1)
Cache.register('user',limit=1)
Cache.register('days',limit=1)
Cache.register('id',limit=2)
Cache.register('instructor',limit=1)

screen = ScreenManager(transition=FadeTransition())
screen.add_widget(pages[0])

AttendanceApp().run()


