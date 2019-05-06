from kivy.app import App
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from functools import partial
from kivy.uix.textinput import TextInput
import calendar
from kivy.uix.listview import ListView,ListItemButton
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.filechooser import FileChooserListView
import os
from kivy.modules import inspector
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
import re
from kivy.cache import Cache
from SQL import *
import time
from kivy.clock import Clock
from Arduino import *
from kivy.uix.image import Image
import xlrd
import datetime
from calendar import c as CalendarObject

def add_2_pop(pop_name,widgets):
    for widget in widgets:
        pop_name.add_widget(widget)



def txt_input(hint,id,font_size,background_normal,background_active,size_hint_x,size_hint_y,pos_hint,multiline=False,readonly=False,focus=False,is_focusable = True):
    txt = TextInput(hint_text = hint, id = id, font_name = "data/font/CaviarDreams_Bold.ttf", font_size = font_size, background_normal = background_normal, background_active = background_active,
                    size_hint_x = size_hint_x,size_hint_y = size_hint_y,pos_hint = pos_hint, multiline = multiline, readonly = readonly, focus = focus,write_tab = False)
    return txt
def btn(text,font_size,background_normal,background_active,size_hint_x,size_hint_y,height,pos_hint,on_release):
    cr_btn = Button(text=text,font_name ="data/font/LibelSuit.ttf",font_size = font_size,background_normal = background_normal,
                    background_active = background_active,size_hint_x = size_hint_x,size_hint_y = size_hint_y,height = height,
                    pos_hint = pos_hint,on_release = on_release)

    return cr_btn

def AddStudent(self):
    self.parent.parent.dismiss()
    popup_content = FloatLayout()
    def Add(dt):
        Name = self.Name.text.strip()
        Surname = self.Surname.text.strip()
        ID = self.StudentID.text.strip()
        Dept = self.Dept.text.strip()
        BankCardId = self.BankCardID.text.strip()
        email = self.email.text.strip()
        Courses = self.AllCourses.adapter.selection

        if not Name or not Surname or not ID or not Dept or not BankCardId or len(Courses) == 0 or not email:
            self.warn.text = 'Please Fill The Fields'
            self.warn.opacity = 1
        else:
            info = [" ".join(course.text.split()[1:3]) for course in Courses]
            value = register_student_w_courses(Name,Surname,Dept,BankCardId,ID,email,info)
            self.warn.opacity = 0
            popup.dismiss()
    def Scan(dt):
        try:
            id = Read()
            self.BankCardID.text = id
            self.warn.opacity = 0
        except:
            self.warn.text = "No Scan"
            self.warn.opacity = 1

    """
        SQL Commands to bring all courses, form a list of lists with course_code and name
    """
    self.data_all_ids = dict([(c_info[2],c_info[0])for c_info in uni_courses()])

    self.StudentID = txt_input('Student ID','user_id',self.parent.parent.parent.height/25,"data/img/widget_gray_75.png","data/img/widget_red_select.png",
                               .30, .1,{"center_x": .18, "center_y": .885})

    self.Dept = txt_input('Dept','user_password',self.parent.parent.parent.height/25,"data/img/widget_gray_75.png","data/img/widget_red_select.png",
                          .30,.1,{"center_x": .18, "center_y": .480})

    self.Name = txt_input('Name','user_name',self.parent.parent.parent.height/25,"data/img/widget_gray_75.png","data/img/widget_red_select.png",
                          .30,.1,{"center_x": .18, "center_y": .750})

    self.Surname = txt_input('Surname','user_surname',self.parent.parent.parent.height/25,"data/img/widget_gray_75.png",
                             "data/img/widget_red_select.png",.30,.1,{"center_x": .18, "center_y": .610})
    self.email = txt_input('Email','user_email',self.parent.parent.parent.height/25,"data/img/widget_gray_75.png","data/img/widget_red_select.png"
                           ,.5,.1,{"center_x": .280, "center_y": .340})


    self.BankCardID = txt_input('Bank Card ID','user_bCId',self.parent.parent.parent.height/25,"data/img/widget_gray_75.png","data/img/widget_red_select.png"
                                ,.5,.1,{"center_x": .280, "center_y": .200})

    popup_content.add_widget(btn('Scan', self.parent.parent.parent.height/40,"data/img/widget_red.png","data/img/widget_red.png",
                                 size_hint_x=.25,size_hint_y=.1,height=self.parent.parent.parent.height/25,
                                 pos_hint={"center_x": .750, "center_y": .200},on_release=Scan ))



    """
        Courses List View
    """
    self.AllCourses = ListView(size_hint=(.45, .53), pos_hint={"center_x": .70, "center_y": .68})
    Courses_Convertor = lambda row_index, x: {"text": "ID: {id} - Name: {N} ".format(id=x[0], N=x[1]), "markup": True,
                                              "selected_color": (.50, .50, .40, 0.6),"deselected_color": (.0, .2, .2, 0.3),
                                              "font_name": "data/font/CaviarDreams_Bold.ttf","font_size": self.height / 3.5, "size_hint_y": None,
                                              "size_hint_x": 1, "height": self.height / 1.2}

    self.AllCourses.adapter = ListAdapter(data=[[Student, self.data_all_ids[Student]] for Student in self.data_all_ids],
                                          selection_mode='multiple',cls=ListItemButton, args_converter=Courses_Convertor,
                                          allow_empty_selection=False)



    popup = Popup(title="Student Detail",title_color = [0,0,0,1],title_align="center",font_name = "data/font/LibelSuit.ttf",title_size=19,
                  content=popup_content,separator_color=[0.0, 0.0, 0.0, 0.4],size_hint=(None, None),
                  size = (self.parent.parent.parent.width /1.2 , self.parent.parent.parent.height/1.2 ),
                  background_color=[0.0, 0.0, 0.0, 0.4], background="T.png")

    self.warn = Label(font_name="data/font/LibelSuit.ttf", id='warn',
                      text='',
                      pos_hint={'center_x': .75, 'center_y': .4}, color=[0, 0, 0, 1], opacity=0)
    popup_content.add_widget(self.warn)


    popup_content.add_widget(btn("Cancel",self.parent.parent.parent.height/40,"data/img/widget_red.png","data/img/widget_red_select.png",.45,
                                 .1,self.parent.parent.parent.height/25,{"center_x": .750, "y": 0},popup.dismiss))


    popup_content.add_widget(btn('Confirm',self.parent.parent.parent.height/40,"data/img/widget_red.png","data/img/widget_red_select.png",
                                 .45,.1,self.parent.parent.parent.height/25,{"center_x": .250, "y": 0},Add))



    add_2_pop(popup_content,[self.StudentID,self.Name,self.Surname,self.Dept,self.email,self.BankCardID,self.AllCourses])
    popup.open()



def on_delete(self):
    self.condition1 = True
    self.condition2 = True
    def CourseSelection(self,dt):
        SelectedStudent = self.Students.adapter.selection
        SelectedCourse = self.AllCourses.adapter.selection
        if len(SelectedStudent) == 0 and len(SelectedCourse)==0:
            self.condition1 = True
            CoursesTaken = dict([(c_info[2],c_info[0])for c_info in courses_taken()])
            students = [[student[4],student[0]+" "+student[1], student[2].upper()]for student in students_taking_courses()]
            self.AllCourses.adapter.data = CoursesTaken.items()
            self.Students.adapter.data = students
            self.AllCourses.populate()
            self.Students.populate()
        elif len(SelectedCourse) > 0 and len(SelectedStudent) >=0 and self.condition2:
            self.condition1 = False
            pattern = re.compile('[A-Z]{0,5}\s\d{0,3}\s')
            Codes = [re.findall(pattern, r.text)[0].strip() for r in SelectedCourse]
            CommonStudents = [[student[4], student[0] + " " + student[1], student[2].upper()] for student in
                              getStudentsfromCourses(Codes)]
            self.Students.adapter.data = CommonStudents
            self.Students.populate()

    def StudentInCourse(self,dt):
        SelectedStudent = self.Students.adapter.selection
        SelectedCourse = self.AllCourses.adapter.selection

        if len(SelectedStudent) == 0 and len(SelectedCourse)==0:
            self.condition2 = True
            CoursesTaken = dict([(c_info[2],c_info[0])for c_info in courses_taken()])
            students = [[student[4],student[0]+" "+student[1], student[2].upper()]for student in students_taking_courses()]
            self.AllCourses.adapter.data = CoursesTaken.items()
            self.Students.adapter.data = students
            self.AllCourses.populate()
            self.Students.populate()

        elif len(SelectedStudent) >= 1 and len(SelectedCourse) >= 0 and self.condition1:
            self.condition2 = False
            pattern = re.compile("\s\d{7,9}\s")
            chosen_students = [int(re.findall(pattern,id.text)[0]) for id in SelectedStudent]
            CommonCourses = dict([(c[2],c[0]) for c in getCommonCourses(chosen_students)])
            self.AllCourses.adapter.data = CommonCourses.items()
            self.AllCourses.populate()
    def Delete(dt):
        SelectedStudent = self.Students.adapter.selection
        SelectedCourse = self.AllCourses.adapter.selection

        if len(SelectedStudent) == 0 and len(SelectedCourse) == 0: 
            self.warn.text =  "Chose a student first"
            self.warn.opacity = 1

        elif len(SelectedCourse) != 0 and len(SelectedStudent) == 0:
            CourseCode = [" ".join(selected.text.split()[1:3]) for selected in SelectedCourse]
            delete_allstudent_course(CourseCode)

            self.popup.dismiss()
            on_delete(self)
        elif len(SelectedStudent) != 0 and len(SelectedCourse) == 0:
            pattern = re.compile("\s\d{7,9}\s")
            chosen_students = [int(re.findall(pattern, id.text)[0]) for id in SelectedStudent]
            delete_student_allcourses(chosen_students)
            self.warn.opacity = 0
            """
                delete the student from all courses
            """
            self.popup.dismiss()
            on_delete(self)
        elif len(SelectedStudent) != 0 and len(SelectedCourse) != 0:
            idpatterns = re.compile("\s\d{7,9}\s")
            chosen_students = [int(re.findall(idpatterns, id.text)[0]) for id in SelectedStudent]
            coursepattern = re.compile('[A-Z]{0,5}\s\d{0,3}\s')
            Codes = [re.findall(coursepattern, r.text)[0].strip() for r in SelectedCourse]
            delete_student_course(chosen_students,Codes)
            self.warn.opacity = 0

            """
                delete the chosen students from the chosen courses
            """
            self.popup.dismiss()
            on_delete(self)
    Data = [[student[4],student[0]+' '+student[1],student[2]]for student in students_taking_courses()]


    self.Students = ListView(size_hint=(.5, .65),pos_hint={"center_x": .25, "center_y": .58})

    args_converter = lambda row_index, x: {"text": "ID: {id} - Name: {N} - Dept: {D} ".format(id=x[0], N=x[1].encode('utf-8'), D = x[2].encode('utf-8')),
                                           "markup": True,"selected_color": (.50, .50, .40, 0.6),"deselected_color": (.0, .2, .2, 0.3),
                                           "font_name": "data/font/CaviarDreams_Bold.ttf","font_size": self.height / 60,
                                           "size_hint_y": None,"size_hint_x":1,"height": 40,"on_release": partial(StudentInCourse,self)}

    self.Students.adapter = ListAdapter(data=Data,selection_mode="multiple"
                                        ,cls=ListItemButton,args_converter=args_converter,allow_empty_selection=True)




    self.data_all_ids = dict([(c_info[2],c_info[0])for c_info in courses_taken()])
    popup_content = FloatLayout()
    self.popup = Popup(id="pop",title="Delete students",font_name = "data/font/CaviarDreams_Bold.ttf",title_size = 23,title_align="center",title_color = [0,0,0,1],
                       content=popup_content,separator_color=[0,0,0, 0.1],size_hint=(None, None),size=(750, self.height/1.2 )
                       ,background="T.png",pos_hint = {"center_x":.5,"center_y":.50})

    popup_content.add_widget(Label(text="Students",pos_hint = {'center_x':.25,'center_y':.95},color=[0,0,0,1]))
    popup_content.add_widget(Label(text="Courses", pos_hint={'center_x': .75, 'center_y': .95}, color=[0, 0, 0, 1]))


    self.warn = Label(text="warning",pos_hint = {'center_x':.50,'center_y':.20},color=[0,0,0,1],font_name = "data/font/CaviarDreams_Bold.ttf",opacity = 0)
    popup_content.add_widget(self.warn)


    """
        SQL commands for getting all courses in the university, list of lists [[course_code, name]]
    """
    if len(self.data_all_ids) != 0:
        x = float(len(self.data_all_ids.items())) * 16 / float(len(self.data_all_ids.items())) / 40
        y = float(len(self.data_all_ids.items())) * 28.2 / float(len(self.data_all_ids.items())) / 40
    else:
        x = 0.4
        y = 0.705


    self.AllCourses = ListView(size_hint=(.48, x),pos_hint={"center_x": .76, "center_y": y})

    Courses_Convertor = lambda row_index, x: {"text": "ID: {id} - Name: {N} ".format(id=x[0], N=x[1]),"markup": True,
                                           "selected_color": (.50, .50, .40, 0.6),"deselected_color": (.0, .2, .2, 0.3),
                                           "font_name": "data/font/CaviarDreams_Bold.ttf","font_size": self.height / 50,"size_hint_y": None,
                                           "size_hint_x":1,"height": 35,"on_release": partial(CourseSelection,self)}

    self.AllCourses.adapter = ListAdapter(data=self.data_all_ids.items(),selection_limit=-1,selection_mode="multiple",
                                          cls=ListItemButton,args_converter=Courses_Convertor,allow_empty_selection=True)

    popup_content.add_widget(btn('Confirm',self.height/25,"data/img/widget_red.png","data/img/widget_red.png",.25,None,self.height/20,
                                 {"center_x": .35, "center_y": .075},Delete))

    popup_content.add_widget(btn('Close',self.height/25,"data/img/widget_red.png","data/img/widget_red.png",.25,None,self.height/20,
                                {"center_x": .65, "center_y": .075},self.popup.dismiss))


    add_2_pop(popup_content,[self.AllCourses,self.Students])

    self.popup.open()


def Importlist(self):

    def selected(self):
        try:
            self.parent.parent.parent.parent.dismiss()
        except:
            pass


    def open_list(dt):
        out = FloatLayout(size_hint=(.4,.85),pos_hint = {'center_x':.55,'center_y':.2})
        popup_in = Popup(title="Import List Of Students",
                        content=out,
                        separator_color=[140 / 255., 55 / 255., 95 / 255., 1.],
                        size_hint=(None, None),
                        size=(720, 300)
                        )

        self.filechooser = FileChooserListView(path=os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop"),
                                          filters=["*.xlsx"],
                                          size=(self.width, 40),
                                          pos_hint={"center_x": .5, "center_y": .99}
                                          )
        out.add_widget(Button(text='Choose',pos_hint={"center_x":.25,"center_y":.35},on_release = selected,size_hint= (.28,.2)))
        out.add_widget(self.filechooser)
        popup_in.open()
    def confirm(dt):
        try:
            if len(self.filechooser.selection) == 0 or len(AllCourses.adapter.selection) == 0:
                WarningLabel.opacity = 1
            else:
                WarningLabel.opacity = 0
                file_xl = xlrd.open_workbook(self.filechooser.selection[0]).sheet_by_index(0)
                data = [tuple([file_xl.cell_value(row, col) for col in range(file_xl.ncols)]) for row in range(1, file_xl.nrows)]
                pattern = re.compile('[A-Z]{0,5}\s\d{0,3}\s')
                courses = AllCourses.adapter.selection
                Codes = [re.findall(pattern, r.text)[0].strip() for r in courses]
                add_students_w_courses(data,Codes)
                self.popup.dismiss()
        except:
            WarningLabel.opacity = 1


    self.data_all_ids = dict([(course[2], course[0]) for course in get_ins_courses(find_ins_id(Cache.get('instructor','email'))[0][0])])

    popup_content = FloatLayout()
    img = Image(source="data/img/excel_ico.png", size_hint_y=.18, pos_hint={'center_x': .05, 'center_y': .83},
                size_hint_x=.18, keep_ratio=True)
    WarningLabel = Label(text='Please Choose the files first', color=[0, 0, 0, 1],
                         pos_hint={'center_x': .5, 'center_y': .5},opacity = 0)
    popup_content.add_widget(WarningLabel)
    popup_content.add_widget(img)

    popup_content.add_widget(Label(text="Courses", pos_hint={"center_x": .75, "center_y": .99}, size_hint=(.08, .08)))

    self.popup = Popup(id="pop", title="Import List", font_name="data/font/CaviarDreams_Bold.ttf", title_size=23,
                       title_align="center", title_color=[0, 0, 0, 1],
                       content=popup_content, separator_color=[0, 0, 0, 0.1], size_hint=(None, None),
                       size=(520, (float(self.parent.height) / .140) - 660)
                       , background="T.png", pos_hint={"center_x": .5, "center_y": .50})

    """
        SQL commands for getting all courses in the university, list of lists [[course_code, name]]
    """

    AllCourses = ListView(size_hint=(.53, 0.6), pos_hint={"center_x": .74, "center_y": 0.68})

    Courses_Convertor = lambda row_index, x: {"text": "ID: {id} - Name: {N} ".format(id=x[0], N=x[1]), "markup": True,
                                              "selected_color": (.50, .50, .40, 0.6),
                                              "deselected_color": (.0, .2, .2, 0.3),
                                              "font_name": "data/font/CaviarDreams_Bold.ttf",
                                              "font_size": self.height / 3, "size_hint_y": None,
                                              "size_hint_x": 1, "height": self.height / 1.2,
                                              }

    AllCourses.adapter = ListAdapter(data=self.data_all_ids.items(), selection_limit=-1, selection_mode="multiple",
                                          cls=ListItemButton, args_converter=Courses_Convertor,
                                          allow_empty_selection=True)
    popup_content.add_widget(btn("Import List",self.height/2.3,"data/img/widget_red.png","data/img/widget_red.png",.25,None,self.height/1.8,
                                  { "center_x": .28, "center_y": .83},open_list))

    popup_content.add_widget(btn("Confirm",self.height/2.3,"data/img/widget_red.png","data/img/widget_red.png",.25,None,self.height/1.8,
                                 {"center_x": .35, "center_y": .05 - (len(AllCourses.adapter.data) * self.height / 2) / 1000},
                                 confirm))
    popup_content.add_widget(btn("Close",self.height/2.3,"data/img/widget_red.png","data/img/widget_red.png",.25,None,self.height/1.8,
                                 {"center_x": .65, "center_y": .05 - (  len(AllCourses.adapter.data) * self.height / 2) / 1000},
                                 self.popup.dismiss))
    add_2_pop(popup_content,[AllCourses])
    self.popup.open()



def profile(self):
    popup_content = FloatLayout()

    def update(self,dt):
        updated = updatepass(self.passwd.text,self.newpasswd.text,email)
        if updated:
            popup.dismiss()
            profile(self)
        else:
            self.Label.opacity = 1


    self.Label =  Label(id='notice',text="password has not been updated", pos_hint={"center_x": .67, "center_y": .400},color=[0,0,0,1],opacity = 0)

    self.Name = txt_input("Name",'user_name',self.parent.parent.parent.height/25,"data/img/widget_gray_75.png","data/img/widget_red_select.png",.45,.1,
                          {"center_x": .25, "center_y": .855},focus=False,is_focusable=False,readonly=True)
    self.email = txt_input('email','user_email',self.parent.parent.parent.height/25,"data/img/widget_gray_75.png","data/img/widget_red_select.png",
                           .45,.1,{"center_x": .75, "center_y": .700},readonly=True,is_focusable=False)
    self.Surname = txt_input('Surname','user_surname',self.parent.parent.parent.height/25,"data/img/widget_gray_75.png",
                             "data/img/widget_red_select.png",.45,.1,{"center_x": .75, "center_y": .855},is_focusable=False,
                             readonly=True)


    self.Dept = txt_input('Dept','user_dept',self.parent.parent.parent.height/25,"data/img/widget_gray_75.png","data/img/widget_red_select.png",
                          .45,.1,{"center_x": .25, "center_y": .700},is_focusable=False,readonly=True)
    self.passwd = txt_input('current password','ins_password', self.parent.parent.parent.height/25,"data/img/widget_gray_75.png",
                            "data/img/widget_red_select.png",.45,.1,{"center_x": .25, "center_y": .550})
    self.newpasswd = txt_input('new password','new_password',self.parent.parent.parent.height/25,"data/img/widget_gray_75.png",
                               "data/img/widget_red_select.png",.45,.1,{"center_x": .25, "center_y": .400})

    popup = Popup(title="Instructor Detail",title_color = [0,0,0,1],title_align="center",font_name = "data/font/LibelSuit.ttf",title_size=19,
                  content=popup_content,separator_color=[0.0, 0.0, 0.0, 0.4],size_hint=(None, None),
                  size = (self.parent.parent.parent.width /1.2 , self.parent.parent.parent.height/1.35 ),
                  background_color=[0.0, 0.0, 0.0, 0.4], background="T.png")

    if get_ins_info(Cache.get('instructor','email')):
        info = get_ins_info(Cache.get('instructor','email'))[0]
        Name,surname,email,dept = info[0],info[1],info[2],info[3]
        self.Name.text = Name
        self.email.text = email
        self.Surname.text = surname
        self.Dept.text = dept
    else:
        Name,surname,email,dept = None,None,None,None

    add_2_pop(popup_content,[self.Label,self.Name,self.Surname,self.Dept,self.email,self.passwd,self.newpasswd])
    popup_content.add_widget(btn('Cancel',self.height/20,"data/img/widget_red.png","data/img/widget_red.png",.45,.1,self.height/1.8,
                                 {"center_x": .75, "center_y": .085},popup.dismiss))

    popup_content.add_widget(btn('Update',self.height/20,"data/img/widget_red.png","data/img/widget_red_select.png",.45,.1,
                                 self.height/3.5,{"center_x": .25, "center_y": .085},partial(update,self)))

    popup.open()





def DropdownControl(self,dt):

    data = self.children[0].children
    counter = 0
    for i in data:
        try:
            if i.btn_id == 1:
                i.pos_hint = {"center_x": .150, "center_y": .700}
            elif i.btn_id == 2:
                i.pos_hint = {"center_x": .150, "center_y": .550}
            elif i.btn_id == 3:
                i.pos_hint = {"center_x": .150, "center_y": .400}
            counter += 1
        except:
            continue

def h(self,dt):

    if dt.text == "Manage Students":
        self.StudentDropDown.open(dt)
    elif dt.text ==  "Manage Courses":
        self.CoursesDropDown.open(dt)
    widgets = self.children[0].children
    for i in widgets:
        try:
            if dt.text == "Manage Students":
                if i.btn_id == 1:
                    i.pos_hint = {"center_x": .150, "center_y": .750}
                elif i.btn_id == 2:
                    i.pos_hint = {"center_x": .150, "center_y": .40}
                elif i.btn_id == 3:
                    i.pos_hint = {"center_x": .150, "center_y": .250}
            elif dt.text == "Manage Courses":
                if i.btn_id == 3:
                    i.pos_hint = {"center_x": .150, "center_y": .270}

        except:
            continue




def on_pre_enter(self):
    self.StudentDropDown = DropDown(pos_hint = {"center_x":.165,"center_y":.59}, on_dismiss = Clock.schedule_once(partial(DropdownControl,self) ))
    student_add = Button(text="add student",size_hint_y = None,height = 40,size_hint_x = None, width = 120,background_normal = "data/img/but_red_down.png",background_active ="data/img/but_red_down.png",on_release = AddStudent)
    import_list = Button(text="import list",size_hint_y = None,height = 40,size_hint_x = None, width = 120,background_normal = "data/img/but_red_down.png",background_active ="data/img/but_red_down.png",on_release = Importlist)
    student_delete = Button(text="delete student",size_hint_y = None,height = 40,size_hint_x = None, width = 120,background_normal = "data/img/but_red_down.png",background_active ="data/img/but_red_down.png",on_release = self.del_students)


    self.CoursesDropDown = DropDown(pos_hint = {'center_x':.165,'center_y':.430},on_dismiss = Clock.schedule_once(partial(DropdownControl,self) ))
    course_add = Button(text="add course",size_hint_y = None,height = 40,size_hint_x = None, width = 120,background_normal = "data/img/but_red_down.png",background_active ="data/img/but_red_down.png",on_release = add_course)
    course_delete = Button(text="delete course",size_hint_y = None,height = 40,size_hint_x = None, width = 120,background_normal = "data/img/but_red_down.png",background_active ="data/img/but_red_down.png",on_release = delete_course)

    self.CoursesDropDown.add_widget(course_add)
    self.CoursesDropDown.add_widget(course_delete)
    self.CoursesDropDown.container.spacing = 5



    self.StudentDropDown.container.spacing = 5
    self.StudentDropDown.add_widget(student_add)
    self.StudentDropDown.add_widget(import_list)
    self.StudentDropDown.add_widget(student_delete)



    self.ids["Co_btn"].bind(on_release = partial(h,self))
    self.ids["St_btn"].bind(on_release = partial(h,self))


def load_string(File):

    with open("{FileName}.RA".format(FileName = File),"r") as KivyFile:
        Builder.load_string(KivyFile.read())


def AttendanceLogin(self):
    if self.ids["CheckLogin"].active == False:
        id = self.ids['input_id'].text.strip()

        user_id = studentlogin(id)
        if user_id == None :
            self.ids['warning'].text = "Wrong student id, Please try again."
            self.ids['warning'].pos_hint  = {"center_x": .62, "center_y": .280}
            self.ids["warning"].opacity = 1
            return False
        else:
            self.ids['warning'].opacity = 0
            Cache.append("user", "login", self.ids["input_id"].text.strip())
            return True
    elif self.ids['CheckLogin'].active == True:
        email = self.ids['input_id'].text.strip()
        password = self.ids['input_pass'].text.strip()
        data = ins_login(email,password)
        if data == None:
            self.ids['warning'].text = 'Wrong email or password, Please try again.'
            self.ids['warning'].pos_hint = {"center_x": .65, "center_y": .280}
            self.ids["warning"].opacity = 1
            return False
        else:
            self.ids["warning"].opacity = 0
            Cache.append('instructor','email',email)
            return True
def Calendar(self,Value):
        layout = self.ids['BOX']
        self.cols = 7
        month = datetime.datetime.now().month
        weekdays = semester_weeks(month,Cache.get('counter','value'))
        Days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for Day in Days:
            layout.add_widget(Button(text=Day,color=[ 1,1,1,1],font_name= "data/font/CaviarDreams_Bold.ttf",background_color = [0.0,0.0,0.0,0.70],disabled=True))

        if Cache.get("days", 'numbers') == None:
            Cache.append("days", 'numbers', weekdays)
        else:
            Cache.remove("days", "numbers")
            Cache.append("days", 'numbers', weekdays)

        for day in weekdays:
            if day[1] in [5,6]:
                layout.add_widget(
                            Button(text='{j}'.format(j=day[0]), background_color=[0.0, 0.0, 0.0, 0.70],disabled=True))
            else:
                layout.add_widget(Button(on_press=self.on_release, text='{j}'.format(j=day[0]), color=[1, 1, 1, 1],
                                                 font_name="data/font/CaviarDreams_Bold.ttf",background_color = [0.0,0.0,0.0,0.70],id = '{j}'.format(j=day[0])))


def semester_weeks(Value,w_n):
    if Value in list(range(2,6,1)):
        Months = list(range(2,6,1))
    else:
        Months = [9,10,11,12,1]
    days = [day+(month,) for month in Months for day in CalendarObject.itermonthdays2(2019,month) if day[0] != 0]
    days = days[getIndex(days):]
    weeks = dict([((i/7)+1,days[i:i+7]) for i in range(0,len(days),7)][:-3])
    return weeks[w_n]

def getIndex(days):
    DAYS = days[:7]
    month = list(range(2,6,1))+ [9,10,11,12,1]
    for i in range(1,7,1):
        for m in month:
            try:
              return DAYS.index((i,0,m))
            except:
                continue

def find(days,number):
    return [day for day in days if day[0]== int(number)][0]



def NotePopUp(self,Day):
    popup_content = FloatLayout()
    """
        SQL, get all the attendence for the user for the chosen day and month
    """


    data = attendance_report(Cache.get('user', 'login'), find(Cache.get('days', 'numbers'), Day))


    if not data:
        data = []

    self.popup = Popup(title="Attendance Report",font_name = "data/font/CaviarDreams_Bold.ttf",title_size = 15,title_align = "center",
                    content=popup_content,separator_color=[0,0,0, 0.1], size_hint=(None, None),
                    size=(self.width / .12, self.height / .20), background="data/img/BACK.png",)

    self.list_quests = ListView(size_hint=(1, .9), pos_hint={"center_x": .5, "center_y": .53})

    args_converter = lambda row_index, x: {"text": "ID: {id} - Course: {C} - Title: {T} - Time: {t}".format(id=x[0],C=x[1],T = getcourseinfo(x[1]),t = x[-1]),
                                           "markup": True,"selected_color": (.0, .2, .2, 0.3),"deselected_color": (.0, .2, .2, 0.3),
                                           "font_name": "data/font/CaviarDreams_Bold.ttf", "font_size": self.height / 7,
                                           "size_hint_y": None, "size_hint_x":1, "height": self.height / 2, }


    self.list_quests.adapter = ListAdapter(data=data,
                                           selection_limit = 0,selection_mode='multiple', cls=ListItemButton, args_converter=args_converter,allow_empty_selection=True )

    popup_content.add_widget(self.list_quests)

    popup_content.add_widget(Button(text="Close", font_name="data/font/LibelSuit.ttf",
                                    font_size=self.height / 5,background_normal="data/img/but_red_down.png",
                                    background_down="data/img/but_red_down.png",size_hint_x=.15,
                                    size_hint_y=None,height=self.height / 3,pos_hint={"center_x": .5, "y": .0},
                                    on_release=self.popup.dismiss))


    self.popup.open()


def new_card_pop(self):
    popup_content = FloatLayout()
    def save(dt):
        if email_exist(self.Name.text.strip()):
            self.warn.opacity = 0
            Cache.append('id','email',self.Name.text)
            new_card(Cache.get('id','email'),Cache.get('id','user'))
            h = attendance(Cache.get('id','user'))
            value = card_exist(Cache.get('id', 'user'))

            self.ids['st_id'].text = str(value[0][3])
            self.ids['st_name'].text = value[0][0] + " "+ value[0][1]
            Clock.schedule_interval(self.scan,4)
            popup.dismiss()
            Cache.remove('id', 'user')
        else:
            self.warn.opacity = 1
    def cancel(dt):
        Clock.schedule_interval(self.scan, 4)
        popup.dismiss()
        Cache.remove('id', 'user')

    self.Name = txt_input("Email", 'user_name',  self.parent.parent.parent.height / 25, "data/img/widget_gray_75.png",
                          "data/img/widget_red_select.png", 1, .2,
                          {"center_x": .5, "center_y": .855})

    self.warn = Label(font_name="data/font/LibelSuit.ttf",id='warn',text='email does not exist, please try again with different one',pos_hint = {'center_x':.45,'center_y':.2},color=[0,0,0,1],opacity = 0)
    popup_content.add_widget(self.warn)
    popup_content.add_widget(self.Name)

    popup = Popup(title="New Card", title_color=[0, 0, 0, 1], title_align="center",
                  font_name="data/font/LibelSuit.ttf", title_size=19,
                  content=popup_content, separator_color=[0.0, 0.0, 0.0, 0.4], size_hint=(None, None),
                  size=(self.parent.parent.parent.width / 2, self.parent.parent.parent.height / 2),
                  background_color=[0.0, 0.0, 0.0, 0.4], background="T.png")

    popup_content.add_widget(btn('Cancel',self.height/30,"data/img/widget_red.png","data/img/widget_red.png",.45,.1,self.height/1.8,
                                 {"center_x": .75, "center_y": .085},cancel))

    popup_content.add_widget(btn('Update',self.height/30,"data/img/widget_red.png","data/img/widget_red_select.png",.45,.1,
                                 self.height/3.5,{"center_x": .25, "center_y": .085},save))



    popup.open()



def existbutton(self):

    self.add_widget(Button(text="Exit",size_hint = (.15,.09),pos_hint = {'center_x':.75,'center_y':.150},background_normal="data/img/but_red_down.png",background_active="data/img/but_red_down.png",
                           on_press = self.Exit,background_down="data/img/but_red_down.png"))

def add_course(self):
    self.parent.parent.dismiss()
    popup_content = FloatLayout()

    def Add(dt):
        Code = self.CourseCode.text.strip()
        Title = self.CourseTitle.text.strip()
        Credits = self.Credits.text.strip()
        classroom = self.All_Ins.adapter.selection
        days = self.days.text.strip()
        start = self.start.text.strip()
        end = self.end.text.strip()

        if not Code or not Title or not Credits or not classroom or not start or not end:
            self.warn.text = "Please Fill"
            self.warn.opacity = 1

        elif re.match("\w+\s\d+", Code) == None:
            self.warn.text = "Please Follow the convention in Course Codes 'Letters Numbers'"
            self.warn.opacity = 1

        else:
            reply = ""
            ins_id = find_ins_id(Cache.get('instructor','email'))[0][0]
            class_id = find_class_id(classroom[0].text.split()[-1])[0][0]
            course_reg = reg_course(Title,Credits,Code,ins_id)
            if course_reg:
                start_time = start.split(',')
                end_time = end.split(",")
                if len(days.split(',')) != 1:
                    index = 0
                    for day in days.split(','):
                        try:
                            if len(start_time) == 2 and len(end_time) == 1:
                                reply = course_schedule(start_time[index],end_time[0],day,int(class_id),Code)
                                index += 1
                            elif len(end_time) == 2 and len(start_time) == 1:
                                reply =course_schedule(start_time[0], end_time[index], day, int(class_id), Code)
                                index += 1
                            elif len(end_time) == 2 and len(start_time) == 2:
                                reply = course_schedule(start_time[index], end_time[index], day, int(class_id), Code)
                                index += 1
                        except:
                            self.warn.text = reply
                            self.warn.opacity = 1

                    self.warn.opacity = 0
                    popup.dismiss()

                elif len(days.split(",")) == 1:
                    try:
                        if len(start_time) == 2 and len(end_time) == 2:
                            reply =course_schedule(start_time[0],end_time[0],days,int(class_id),Code)
                            reply =course_schedule(start_time[1], end_time[1], days, int(class_id), Code)
                        elif len(start_time) == 1 and len(end_time) == 2:
                            reply =course_schedule(start_time[0], end_time[0], days, int(class_id), Code)
                            reply =course_schedule(start_time[0], end_time[1], days, int(class_id), Code)
                        elif len(end_time) == 1 and len(start_time) == 2:
                            reply =course_schedule(start_time[0], end_time[0], days, int(class_id), Code)
                            reply =course_schedule(start_time[1], end_time[0], days, int(class_id), Code)
                        else:
                            reply =course_schedule(start_time[0], end_time[0], days, int(class_id), Code)

                        self.warn.opacity = 0
                        popup.dismiss()
                    except:
                        self.warn.text = reply
                        self.warn.opacity = 1

            else:
                self.warn.text = "Duplicate Course code"
                self.warn.opacity = 1
    """
        SQL Commands to bring all courses, form a list of lists with course_code and name
    """
    Data = [[str(ins[2]) + str(ins[1])] for ins in all_rooms()]

    self.CourseCode = TextInput(hint_text="Course Code", id="CourseCode", multiline=False,
                               font_name="data/font/CaviarDreams_Bold.ttf", font_size=self.parent.parent.parent.height / 25,
                               background_normal="data/img/widget_gray_75.png", background_active="data/img/widget_red_select.png",
                                padding_y=[self.parent.parent.parent.height / 150, 0],
                               size_hint_x=.40, size_hint_y=.1,pos_hint={"center_x": .20, "center_y": .900}, write_tab=False)

    self.Credits = TextInput(hint_text="Credits", id="CourseCredits", write_tab=False, multiline=False,
                          font_name="data/font/CaviarDreams_Bold.ttf", font_size=self.parent.parent.parent.height / 25,
                          background_normal="data/img/widget_gray_75.png", background_active="data/img/widget_red_select.png",
                          padding_y=[self.height / 100, 0],
                          size_hint_x=.40, size_hint_y=.1, pos_hint={"center_x": .20, "center_y": .600})

    self.days = TextInput(hint_text="Days", id="course_days", write_tab=False, multiline=False,
                          font_name="data/font/CaviarDreams_Bold.ttf", font_size=self.parent.parent.parent.height / 25,
                          background_normal="data/img/widget_gray_75.png", background_active="data/img/widget_red_select.png",
                          padding_y=[self.height / 100, 0],
                          size_hint_x=.40, size_hint_y=.1, pos_hint={"center_x": .20, "center_y": .450})





    self.CourseTitle = TextInput(hint_text="Course Title", id="user_password", multiline=False,
                          font_name="data/font/CaviarDreams_Bold.ttf"
                          , font_size=self.parent.parent.parent.height / 25,
                          background_normal="data/img/widget_gray_75.png",
                          background_active="data/img/widget_red_select.png",

                          padding_y=[self.parent.parent.parent.height / 100, 0], size_hint_x=.40, size_hint_y=.1,
                          pos_hint={"center_x": .20, "center_y": .750}, write_tab=False)

    self.start = TextInput(hint_text="Start hour 12:00", id="user_password", multiline=False,
                          font_name="data/font/CaviarDreams_Bold.ttf"
                          , font_size=self.parent.parent.parent.height / 25,
                          background_normal="data/img/widget_gray_75.png",
                          background_active="data/img/widget_red_select.png",

                          padding_y=[self.parent.parent.parent.height / 100, 0], size_hint_x=.40, size_hint_y=.1,
                          pos_hint={"center_x": .20, "center_y": .300}, write_tab=False)

    self.end = TextInput(hint_text="End hour 14:00", id="user_password", multiline=False,
                          font_name="data/font/CaviarDreams_Bold.ttf"
                          , font_size=self.parent.parent.parent.height / 25,
                          background_normal="data/img/widget_gray_75.png",
                          background_active="data/img/widget_red_select.png",

                          padding_y=[self.parent.parent.parent.height / 100, 0], size_hint_x=.40, size_hint_y=.1,
                          pos_hint={"center_x": .75, "center_y": .300}, write_tab=False)


    popup_content.add_widget(self.start)
    popup_content.add_widget(self.end)



    """ All instructors in the uni"""
    self.All_Ins = ListView(size_hint=(.45, .30), pos_hint={"center_x": .75, "center_y": .80})

    Ins_Convertor = lambda row_index, x: {"text": "Room: {id}".format(id = x[0]), "markup": True,
                                              "selected_color": (.50, .50, .40, 0.6),"deselected_color": (.0, .2, .2, 0.3),
                                              "font_name": "data/font/CaviarDreams_Bold.ttf",  "font_size": self.height / 3.5, "size_hint_y": None,
                                              "size_hint_x": 1, "height": self.height / 1.2}

    """
        SQL all instructors in the university, list of lists [[Name, dept]
    """


    self.All_Ins.adapter = ListAdapter(data=Data,
                                          selection_limit=1,cls=ListItemButton, args_converter=Ins_Convertor,allow_empty_selection=True)


    popup = Popup(title="Course Details", title_color=[0, 0, 0, 1], title_align="center",
                  font_name="data/font/LibelSuit.ttf", title_size=19,
                  content=popup_content, separator_color=[0.0, 0.0, 0.0, 0.4], size_hint=(None, None),
                  size=(self.parent.parent.parent.width / 1.5, self.parent.parent.parent.height / 1.2),
                  background_color=[0.0, 0.0, 0.0, 0.4], background="T.png")

    popup_content.add_widget(
        Button(text="Cancel", font_name="data/font/LibelSuit.ttf", font_size=self.parent.parent.parent.height / 40,
               background_normal="data/img/widget_red.png", background_down="data/img/widget_red_select.png",
               size_hint_x=.45, size_hint_y=.1, height=self.parent.parent.parent.height / 25
               , pos_hint={"center_x": .750, "y": 0}, on_release=popup.dismiss))

    popup_content.add_widget(
        Button(text="Confirm", font_name="data/font/LibelSuit.ttf", font_size=self.parent.parent.parent.height / 40,
               background_normal="data/img/widget_red.png", background_down="data/img/widget_red_select.png",
               size_hint_x=.45, size_hint_y=.1, height=self.parent.parent.parent.height / 25,
               pos_hint={"center_x": .250, "y": 0}, on_release=Add))


    self.warn = Label(text="",pos_hint = {"center_x":.50,'center_y':.18},color = [0,0,0,1],opacity = 0)

    popup_content.add_widget(self.warn)

    popup_content.add_widget(self.CourseCode)
    popup_content.add_widget(self.CourseTitle)
    popup_content.add_widget(self.Credits)
    popup_content.add_widget(self.days)
    popup_content.add_widget(self.All_Ins)

    popup.open()


def delete_course(self):
    self.parent.parent.dismiss()

    def Delete(dt):
        Courses = self.Courses.adapter.selection

        if len(Courses) != 0:
            pattern = re.compile('[a-zA-Z]{0,5}\s\d{0,3}\s')
            Codes = [re.findall(pattern, r.text)[0].strip() for r in Courses]
            del_coures(Codes)
        else:
            pass
        self.popup.dismiss()
        delete_course(self)



    Data = [[course[2], course[0]] for course in get_ins_courses(find_ins_id(Cache.get('instructor','email'))[0][0])]

    popup_content = FloatLayout()


    self.popup = Popup(id="pop", title="Courses", font_name="data/font/CaviarDreams_Bold.ttf", title_size=23,
                       title_align="center",
                       content=popup_content, separator_color=[0, 0, 0, 0.1], size_hint=(None, None),
                       size=(self.width / .200, (float(self.parent.height) / .140) - 90)
                       , background="data/img/BACK.png", pos_hint={"center_x": .5, "center_y": .45})



    self.Courses = ListView(size_hint=(.8, .3), pos_hint={"center_x": .5, "center_y": .75})

    args_converter = lambda row_index, x: {"text": "Code: {id} - Name: {N} ".format(id=x[0], N=x[1]),
                                            "markup": True, "selected_color": (.50, .50, .40, 0.6), "deselected_color": (.0, .2, .2, 0.3),
                                            "font_name": "data/font/CaviarDreams_Bold.ttf", "font_size": self.height / 3.5,
                                            "size_hint_y": None, "size_hint_x": 1, "height": self.height / 1.2}

    """
        SQL get all the courses, list of lists [[courseCode, name]]
    """
    self.Courses.adapter = ListAdapter(data=Data,  selection_mode = "multiple",
                                        cls=ListItemButton,args_converter=args_converter, allow_empty_selection=True)


    popup_content.add_widget(Button(text="Delete", font_name="data/font/LibelSuit.ttf", font_size=self.height / 2.3,
                                    background_normal="data/img/widget_red.png",
                                    background_down="data/img/widget_red.png",
                                     size_hint_x=.25,
                                    size_hint_y=None,
                                    height=self.height / 1.8, pos_hint={"center_x": .35, "center_y": .47 - (
                len(self.Courses.adapter.data) * self.height / 1.5) / 1000},
                                    on_release=Delete))

    popup_content.add_widget(
        Button(text="Close", font_name="data/font/LibelSuit.ttf", id='CloseButton', font_size=self.height / 2.3,
               background_normal="data/img/widget_red.png", background_down="data/img/widget_red.png",
                size_hint_x=.25, size_hint_y=None,
               height=self.height / 1.8, pos_hint={"center_x": .65, "center_y": .47 - (
                        len(self.Courses.adapter.data) * self.height / 1.5) / 1000},
               on_release=self.popup.dismiss))

    popup_content.add_widget(self.Courses)
    self.popup.open()



def ChangePage(pages,screen):
    try:
        screen.switch_to(pages[1])
    except:
        screen.current_name = pages[1].name
    finally:
        del pages[1]