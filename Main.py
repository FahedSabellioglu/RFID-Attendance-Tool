from kivy.app import  App
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
import Functions
import calendar
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.cache import Cache
from kivy.core.window import Window
from kivy.modules import inspector
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
        Month = list(calendar.month_abbr).index(self.text)
        if Cache.get("counter",'value') == None:
            Cache.append("counter", 'value', Month)
        else:
            Cache.remove("counter","value")
            Cache.append("counter",'value',Month)
        pages.append(UserAttendance(name="UserAttendance"))
        Functions.ChangePage(pages,screen)

    @staticmethod
    def on_release(self):
        Functions.NotePopUp(self,self.text)


class LoginPage(Screen):

    Functions.load_string("LoginPage")
    def OnLogin(self):
        pages.append(AttendanceLogin(name="LoginPage"))
        Functions.ChangePage(pages,screen)


class Admin_Page(Screen):
    Functions.load_string("Admin_Page")
    def on_enter(self, *args):
        Functions.on_pre_enter(self)



class AttendanceLogin(Screen):

    Functions.load_string("AttendanceLogin")

    def checkButton(self):
        if self.ids["CheckLogin"].active == True:
            self.ids["input_password"].opacity = 1
            self.ids["input_password"].disabled = False
            self.ids["txt_password"].opacity = 1
            self.ids["input_userid"].pos_hint = {"center_x":.58,"center_y":.66}
            self.ids["txt_userid"].pos_hint = {"center_x":.35,"center_y":.66}
        else:
            self.ids["input_password"].opacity = 0
            self.ids["txt_password"].opacity = 0
            self.ids["input_password"].disabled = True
            self.ids["txt_userid"].pos_hint = {"center_x":.35,"center_y":.56}
            self.ids["input_userid"].pos_hint = {"center_x":.58,"center_y":.56}
        inspector.create_inspector(Window, self.ids["input_userid"])

    def Login(self):
        if Functions.AttendanceLogin(self) and (self.ids["CheckLogin"].active == False):
            pages.append(UserAttendance(name="UserAttendance"))
            Cache.append("User","username",self.ids["input_userid"].text)
            Functions.ChangePage(pages,screen)
        elif Functions.AttendanceLogin(self):
            pages.append(Admin_Page(name="Admin_Page"))
            Cache.append("User","username",self.ids["input_userid"].text)
            Functions.ChangePage(pages,screen)

    def Back(self):
        try:
            screen.switch_to(pages[0])
        except:
            screen.current = pages[0].name



class AttendanceApp(App):
    def build(self):
        screen.current = "LoginPage"
        return screen


pages = [LoginPage(name="LoginPage"),
         ]
Cache.register('counter',limit=1)
Cache.register("User",limit = 1)
screen = ScreenManager(transition=FadeTransition())
screen.add_widget(pages[0])


AttendanceApp().run()


