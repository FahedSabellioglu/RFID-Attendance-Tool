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



Functions.load_string("Weeks")

class Weeks(BoxLayout):
    def __init__(self,**kwargs):
        super(Weeks,self).__init__(**kwargs)


class UserAttendance(Screen):
    Functions.load_string("UserAttendance")
    def on_pre_enter(self, *args):
        Functions.existbutton(self)
        data = list(student_info(Cache.get('user','login'))[0])
        self.ids['user_name'].text = " ".join(data[0:2])
        self.ids['user_id'].text = str(data[4])

        if Cache.get("counter","value") == None:
            Functions.Calendar(self,2)
        else:
            Functions.Calendar(self,Cache.get("counter","value"))
    def Exit(self,dt):
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
        Clock.schedule_interval(self.clearwarning,4)
        if Cache.get('id', 'user') != None:
            Cache.remove('id', 'user')

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
                elif values == -1:
                    self.ids['st_warn'].text = "Attendance already taken"
                    self.ids['st_warn'].opacity = 1
                Cache.remove('id','user')
    def clearwarning(self,dt):
        self.ids['st_warn'].opacity = 0

    def OnLogin(self):
        pages.append(AttendanceLogin(name="LoginPage"))
        Functions.ChangePage(pages,screen)

    def LoginCre(self):
        if Functions.AttendanceLogin(self) and self.ids['CheckLogin'].active==True:
            pages.append(Admin_Page(name="Admin_Page"))
            Clock.unschedule(self.scan)
            Functions.ChangePage(pages, screen)
        elif Functions.AttendanceLogin(self) and self.ids['CheckLogin'].active==False:
            pages.append(UserAttendance(name='User_page'))
            Clock.unschedule(self.scan)
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
        data = list(get_ins_info(Cache.get('instructor','email'))[0])
        self.ids['ins_name'].text = " ".join(data[0:2])
        # Functions.existbutton(self)

    def Exit(self):
        pages.append(LoginPage(name='LoginPage'))
        Functions.ChangePage(pages, screen)

    def profile(self):
        Functions.profile(self)
    def del_students(self,dt):
        Functions.on_delete(self)

class AttendanceApp(App):
    def build(self):
        inspector.create_inspector(Window,self)
        self.icon = r"C:\Users\fahedshaabani\Documents\GitHub\Attendance\data\img\3592659-128.png"
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
        print line.split(),'arduino'
        if len(line.split()) != 0 and "FF" not in line:
            if Cache.get('id', 'user') == None:
                Cache.append('id', 'user', line.strip())
            else:
                Cache.remove('id', 'user'),'purge'
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


