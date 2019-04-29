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
from kivy.modules import inspector
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
import re
from kivy.cache import Cache

def AddStudent(self): #add student drop button
    self.parent.parent.dismiss()
    popup_content = FloatLayout()
    def Add(dt):
        Name = self.Name.text.strip()
        Surname = self.Surname.text.strip()
        ID = self.StudentID.text.strip()
        Dept = self.Dept.text.strip()
        BankCardId = self.BankCardID.text.strip()
        Courses = self.AllCourses.adapter.selection
        if not Name or not Surname or not ID or not Dept or not BankCardId or len(Courses) == 0:
            print "Please Fill"
        else:
            print "adding"
            """
                Commands for adding a new student
            """
            popup.dismiss()


    """
        SQL Commands to bring all courses, form a list of lists with course_code and name
    """

    self.data_all_ids = {'Cs 240': "Data analysis", "Cs 350": "Database", "ENGR 102": "Programming Practice",
                         "ENGR 101": "Introduction to programming",'Cs 140': "Data analysis",'Cs 250': "Data analysis",'Cs 220': "Data analysis",'Cs 210': "Data analysis"
                         ,'Cs 141': "Data analysis",'Cs 270': "Data analysis",'Cs 280': "Data analysis",} # """Fake Data"""


    self.StudentID = TextInput(hint_text="Student ID", id="user_id", multiline=False,font_name="data/font/CaviarDreams_Bold.ttf"
                               , font_size=self.parent.parent.parent.height / 25, background_normal="data/img/widget_gray_75.png",
                               background_active="data/img/widget_red_select.png",
                               padding_y=[self.parent.parent.parent.height / 150, 0], size_hint_x=.30, size_hint_y=.1,
                               pos_hint={"center_x": .18, "center_y": .855}, write_tab=False)


    self.Dept = TextInput(hint_text="Dept", id="user_password", write_tab=False, multiline=False,
                          font_name="data/font/CaviarDreams_Bold.ttf", font_size=self.parent.parent.parent.height / 25,
                          background_normal="data/img/widget_gray_75.png",background_active="data/img/widget_red_select.png",
                           padding_y=[self.height / 100, 0],
                          size_hint_x=.30, size_hint_y=.1, pos_hint={"center_x": .18, "center_y": .400})


    self.Name = TextInput(hint_text="Name", id="user_password", multiline=False, font_name="data/font/CaviarDreams_Bold.ttf"
                          , font_size=self.parent.parent.parent.height / 25, background_normal="data/img/widget_gray_75.png",
                          background_active="data/img/widget_red_select.png",
                          padding_y=[self.parent.parent.parent.height / 100, 0],size_hint_x=.30, size_hint_y=.1,
                          pos_hint={"center_x": .18, "center_y": .700}, write_tab=False)

    self.Surname = TextInput(hint_text="Surname", id="user_password", write_tab=False, multiline=False, font_name="data/font/CaviarDreams_Bold.ttf"
                             , font_size=self.parent.parent.parent.height / 25, background_normal="data/img/widget_gray_75.png",
                             background_active="data/img/widget_red_select.png",
                             padding_y=[self.parent.parent.parent.height / 100, 0], size_hint_x=.30, size_hint_y=.1,
                             pos_hint={"center_x": .18, "center_y": .550})


    self.BankCardID = TextInput(hint_text="Bank Card ID", id="user_password", disable=True,font_name="data/font/CaviarDreams_Bold.ttf"
                                , font_size=self.parent.parent.parent.height / 25, background_normal="data/img/widget_gray_75.png",
                                background_active="data/img/widget_red_select.png",
                                padding_y=[self.parent.parent.parent.height / 100, 0], size_hint_x=.5, size_hint_y=.1,
                                pos_hint={"center_x": .280, "center_y": .250}, write_tab=False)


    popup_content.add_widget(Button(text="Scan",font_name="data/font/LibelSuit.ttf",font_size=self.parent.parent.parent.height / 40,
                                    background_normal="data/img/widget_red.png", background_down="data/img/widget_red_select.png",
                                    size_hint_x=.25, size_hint_y=.1, height=self.parent.parent.parent.height / 25,
                                    pos_hint={"center_x": .750, "center_y": .250}))

    """
        Courses List View
    """
    self.AllCourses = ListView(size_hint=(.45, .53), pos_hint={"center_x": .70, "center_y": .64})
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

    popup_content.add_widget(Button(text="Cancel",font_name="data/font/LibelSuit.ttf",font_size=self.parent.parent.parent.height / 40,
                                    background_normal="data/img/widget_red.png",background_down="data/img/widget_red_select.png",
                                    size_hint_x=.45,size_hint_y=.1, height=self.parent.parent.parent.height / 25
                                    ,pos_hint={"center_x": .750, "y": 0}, on_release=popup.dismiss) )



    popup_content.add_widget(Button(text="Confirm", font_name="data/font/LibelSuit.ttf", font_size=self.parent.parent.parent.height / 40,
                                    background_normal="data/img/widget_red.png",background_down="data/img/widget_red_select.png",
                                    size_hint_x=.45, size_hint_y=.1, height=self.parent.parent.parent.height / 25,
                                    pos_hint={"center_x": .250, "y": 0},on_release = Add ))

    popup_content.add_widget(self.StudentID)
    popup_content.add_widget(self.Dept)
    popup_content.add_widget(self.Name)
    popup_content.add_widget(self.Surname)
    popup_content.add_widget(self.BankCardID)
    popup_content.add_widget(self.AllCourses)


    popup.open()



def on_delete(self): #delete student drop button
    self.parent.parent.dismiss()
    def StudentInCourse(self,dt):
        SelectedStudent = self.Students.adapter.selection
        if len(SelectedStudent) == 0:
            """
             SQL All Courses Back
            """
        else:
            Data = [["Course Code","Title"],["Course Code","Title"],["Course Code","Title"],["Course Code","Title"]]

            """
                get all the students who take the chosen class as list of lists [[id,[name,surname,dept]]
            """
            self.AllCourses.adapter.data = Data
            self.AllCourses.populate()
    def Delete(dt):
        Studentsselected = self.Students.adapter.selection
        Course = self.AllCourses.adapter.selection

        if len(Studentsselected) == 0 and len(Course) == 0: # did not chose any
             print "Chose a student first"

        elif len(Course) != 0 and len(Studentsselected) == 0: #chose a course but not a student
            """
                SQL delete all students from the chosen course
            """
            print "delete all students from the chosen course"
        elif len(Studentsselected) != 0 and len(Course) == 0: # chose a student but not a course,
            """
                delete the student from all courses
            """
            print "delete the student from all courses"
        elif len(Studentsselected) != 0 and len(Course) != 0:
            """
                delete the chosen students from the chosen courses
            """
            print "delete the chosen students from the chosen courses"


        # for line in selected:
        #     RowText = re.findall(r"\d{7,9}|\w+\s\d{3}",line.text)
        #     self.list_quests.adapter.data.remove(RowText)
        #     self.list_quests._trigger_reset_populate()

    self.IDs = {'21725241':["Cs 240","ENGR 102","ENGR 101","Cs 350"],'21725242':["Cs 240","ENGR 102","ENGR 101","Cs 350"],'21725243':["Cs 240","ENGR 102","ENGR 101","Cs 350"],'21725254':["Cs 240","ENGR 102","ENGR 101","Cs 350"]}
    Data = {"21725242": ["Fahed", "Sabellioglu", "Cs"], "21725244": ["Fahed", "Sabellioglu", "Cs"],
            "21725246": ["Fahed", "Sabellioglu", "Cs"], "21725248": ["Fahed", "Sabellioglu", "Cs"],
            "21725243": ["Fahed", "Sabellioglu", "Cs"],"21725245":["Fahed","Sabellioglu","Cs"],"21725247":["Fahed","Sabellioglu","Cs"],"21725249":["Fahed","Sabellioglu","Cs"]
            ,"21722247":["Fahed","Sabellioglu","Cs"],"21225249":["Fahed","Sabellioglu","Cs"],"21715247":["Fahed","Sabellioglu","Cs"],"11725249":["Fahed","Sabellioglu","Cs"]}

    self.data_all_ids = {'Cs 240':"Data analysis","Cs 350":"Database","ENGR 102":"Programming Practice","ENGR 101":"Introduction to programming"}

    popup_content = FloatLayout()
    popup_content.add_widget(Label(text="Stundets",pos_hint = {"center_x":.2,"center_y":.99}))
    popup_content.add_widget(Label(text="Courses",pos_hint = {"center_x":.75,"center_y":.99}))

    self.popup = Popup(id="pop",title="Report",font_name = "data/font/CaviarDreams_Bold.ttf",title_size = 23,title_align="center",
                       content=popup_content,separator_color=[0,0,0, 0.1],size_hint=(None, None),size=(self.width / .20, (float(self.parent.height)/.140)-90 )
                       ,background="data/img/BACK.png",pos_hint = {"center_x":.5,"center_y":.50})

    """
        SQL Commands for getting all the students in the university, list of lists as [[Id, name surname, dept]]
    """
    self.Students = ListView(size_hint=(.5, .75),pos_hint={"center_x": .2, "center_y": .58})

    args_converter = lambda row_index, x: {"text": "ID: {id} - Name: {N} - Dept: {D} ".format(id=x[0], N=" ".join(x[1][0:2]), D = x[1][2]),
                                           "markup": True,"selected_color": (.50, .50, .40, 0.6),"deselected_color": (.0, .2, .2, 0.3),
                                           "font_name": "data/font/CaviarDreams_Bold.ttf","font_size": self.height / 3.5,
                                           "size_hint_y": None,"size_hint_x":1,"height": self.height / 1.2,"on_release": partial(StudentInCourse,self)}

    self.Students.adapter = ListAdapter(data=[[Student, Data[Student]] for Student in Data ],selection_mode="multiple"
                                        ,cls=ListItemButton,args_converter=args_converter,allow_empty_selection=True)


    """
        SQL commands for getting all courses in the university, list of lists [[course_code, name]]
    """
    self.AllCourses = ListView(size_hint=(.45, .75),pos_hint={"center_x": .75, "center_y": .58})

    Courses_Convertor = lambda row_index, x: {"text": "ID: {id} - Name: {N} ".format(id=x[0], N=x[1]),"markup": True,
                                           "selected_color": (.50, .50, .40, 0.6),"deselected_color": (.0, .2, .2, 0.3),
                                           "font_name": "data/font/CaviarDreams_Bold.ttf","font_size": self.height / 3.5,"size_hint_y": None,
                                           "size_hint_x":1,"height": self.height / 1.2}

    self.AllCourses.adapter = ListAdapter(data=[[Student, self.data_all_ids[Student]] for Student in self.data_all_ids ],selection_limit=1,
                                          cls=ListItemButton,args_converter=Courses_Convertor,allow_empty_selection=True)

    popup_content.add_widget(Button(text="Delete",font_name="data/font/LibelSuit.ttf",font_size=self.height / 2.3,
                                    background_normal= "data/img/widget_red.png",background_down=  "data/img/widget_red.png",
                                    size_hint_x=.25,size_hint_y=None,
                                    height=self.height / 1.8,pos_hint={"center_x": .35, "center_y": .47 - (
                                                len(self.Students.adapter.data) * self.height / 1.5) / 1000},
                                    on_release = Delete))

    popup_content.add_widget(Button(text="Close",font_name="data/font/LibelSuit.ttf",id='CloseButton',font_size=self.height / 2.3,
                                    background_normal="data/img/widget_red.png",background_down="data/img/widget_red.png",
                                    size_hint_x=.25,size_hint_y=None,
                                    height=self.height / 1.8,pos_hint={"center_x": .65, "center_y": .47-(len(self.Students.adapter.data) * self.height/1.5)/1000},
                                    on_release=self.popup.dismiss))



    popup_content.add_widget(self.AllCourses)
    popup_content.add_widget(self.Students)

    self.popup.open()

def on_pre_enter(self):
    self.StudentDropDown = DropDown(pos_hint = {"center_x":.295,"center_y":.715})
    student_add = Button(text="add student",size_hint_y = None,height = 40,background_normal = "data/img/but_red_down.png",background_active ="data/img/but_red_down.png",on_release = AddStudent)
    student_delete = Button(text="delete student",size_hint_y = None,height = 40,background_normal = "data/img/but_red_down.png",background_active ="data/img/but_red_down.png",on_release = on_delete)

    self.Ins_DropDown = DropDown(pos_hint = {"center_x":.52,"center_y":.715})
    Course_add = Button(text="add Instructor",size_hint_y = None,height = 40,background_normal = "data/img/but_red_down.png",background_active ="data/img/but_red_down.png",on_release = add_ins)
    Course_delete = Button(text="delete Instructor",size_hint_y = None,height = 40,background_normal = "data/img/but_red_down.png",background_active ="data/img/but_red_down.png",on_release = delete_ins)

    self.CourseDropDown = DropDown(pos_hint = {"center_x":.745,"center_y":.715})
    Ins_add = Button(text="add Course",size_hint_y = None,height = 40,background_normal = "data/img/but_red_down.png",background_active ="data/img/but_red_down.png",on_release = add_course)
    Ins_delete = Button(text="delete Course",size_hint_y = None,height = 40,background_normal = "data/img/but_red_down.png",background_active ="data/img/but_red_down.png",on_release = delete_course)


    self.StudentDropDown.add_widget(student_add)
    self.StudentDropDown.add_widget(student_delete)
    self.StudentDropDown.container.spacing = 5
    self.ids["St_btn"].bind(on_release = self.StudentDropDown.open)

    self.Ins_DropDown.add_widget(Course_add)
    self.Ins_DropDown.add_widget(Course_delete)
    self.Ins_DropDown.container.spacing = 5
    self.ids["Ins_btn"].bind(on_release = self.Ins_DropDown.open)

    self.CourseDropDown.add_widget(Ins_add)
    self.CourseDropDown.add_widget(Ins_delete)
    self.CourseDropDown.container.spacing = 5
    self.ids["Cl_btn"].bind(on_release = self.CourseDropDown.open)


def add_ins(self):
    self.parent.parent.dismiss()
    popup_content = FloatLayout()

    def Add(dt):
        Name = self.Ins_Name.text.strip()
        Surname = self.surname.text.strip()
        Dept = self.Ins_dept.text.strip()
        Courses = self.AllCourses.adapter.selection

        if not Name or not Surname or not Dept  or len(Courses) == 0:
            print "Please Fill"
        else:
            print "adding"
            """
                SQL Commands for adding a new instructor, increment id
            """
            popup.dismiss()


    self.data_all_ids = {'Cs 240': "Data analysis", "Cs 350": "Database", "ENGR 102": "Programming Practice",
                         "ENGR 101": "Introduction to programming",'Cs 140': "Data analysis",'Cs 250': "Data analysis",'Cs 220': "Data analysis",'Cs 210': "Data analysis"
                         ,'Cs 141': "Data analysis",'Cs 270': "Data analysis",'Cs 280': "Data analysis",}


    self.Ins_Name = TextInput(hint_text="Name", id="user_name", multiline=False,font_name="data/font/CaviarDreams_Bold.ttf"
                               , font_size=self.parent.parent.parent.height / 25, background_normal="data/img/widget_gray_75.png",
                               background_active="data/img/widget_red_select.png",
                               padding_y=[self.parent.parent.parent.height / 150, 0], size_hint_x=.30, size_hint_y=.1,
                               pos_hint={"center_x": .18, "center_y": .855}, write_tab=False)


    self.Ins_dept = TextInput(hint_text="Dept", id="user_surname", write_tab=False, multiline=False,
                          font_name="data/font/CaviarDreams_Bold.ttf", font_size=self.parent.parent.parent.height / 25,
                          background_normal="data/img/widget_gray_75.png", background_active="data/img/widget_red_select.png",
                           padding_y=[self.height / 100, 0],
                          size_hint_x=.30, size_hint_y=.1, pos_hint={"center_x": .18, "center_y": .400})


    self.surname = TextInput(hint_text="Surname", id="user_password", multiline=False, font_name="data/font/CaviarDreams_Bold.ttf"
                          , font_size=self.parent.parent.parent.height / 25, background_normal="data/img/widget_gray_75.png",
                          background_active="data/img/widget_red_select.png",
                          padding_y=[self.parent.parent.parent.height / 100, 0],size_hint_x=.30, size_hint_y=.1,
                          pos_hint={"center_x": .18, "center_y": .700}, write_tab=False)


    self.password = TextInput(hint_text="Password", id="user_password", write_tab=False, multiline=False,
                             font_name="data/font/CaviarDreams_Bold.ttf" , font_size=self.parent.parent.parent.height / 25,
                             background_normal="data/img/widget_gray_75.png", background_active="data/img/widget_red_select.png",
                              padding_y=[self.parent.parent.parent.height / 100, 0],
                             size_hint_x=.30, size_hint_y=.1, pos_hint={"center_x": .18, "center_y": .550})


    """ 
        SQL for all courses in the university, list of lists [course_code,name]
    """

    self.AllCourses = ListView(size_hint=(.45, .53), pos_hint={"center_x": .70, "center_y": .64})

    Courses_Convertor = lambda row_index, x: {"text": "ID: {id} - Name: {N} ".format(id=x[0], N=x[1]), "markup": True,
                                              "selected_color": (.50, .50, .40, 0.6),"deselected_color": (.0, .2, .2, 0.3),
                                              "font_name": "data/font/CaviarDreams_Bold.ttf", "font_size": self.height / 3.5, "size_hint_y": None,
                                              "size_hint_x": 1, "height": self.height / 1.2}

    self.AllCourses.adapter = ListAdapter(data=[[Student, self.data_all_ids[Student]] for Student in self.data_all_ids],
                                          selection_limit=-1, cls=ListItemButton, args_converter=Courses_Convertor,allow_empty_selection=False)


    popup = Popup(title="Instructor Details",title_color = [0,0,0,1],title_align="center",font_name = "data/font/LibelSuit.ttf",title_size=19,
                  content=popup_content, separator_color=[0.0, 0.0, 0.0, 0.4],size_hint=(None, None), background="T.png",
                  size = (self.parent.parent.parent.width /1.2 , self.parent.parent.parent.height/1.2 ), background_color=[0.0, 0.0, 0.0, 0.4])

    popup_content.add_widget(Button(text="Cancel", font_name="data/font/LibelSuit.ttf", font_size=self.parent.parent.parent.height / 40,
                                    background_normal="data/img/widget_red.png", background_down="data/img/widget_red_select.png",
                                    size_hint_x=.45, size_hint_y=.1,height=self.parent.parent.parent.height / 25,
                                    pos_hint={"center_x": .750, "y": 0},on_release=popup.dismiss) )

    popup_content.add_widget(Button(text="Confirm", font_name="data/font/LibelSuit.ttf", font_size=self.parent.parent.parent.height / 40,
                                    background_normal="data/img/widget_red.png", background_down="data/img/widget_red_select.png",
                                    size_hint_x=.45,size_hint_y=.1, height=self.parent.parent.parent.height / 25,
                                    pos_hint={"center_x": .250, "y": 0}, on_release= Add ))


    popup_content.add_widget(self.AllCourses)
    popup_content.add_widget(self.password)
    popup_content.add_widget(self.surname)
    popup_content.add_widget(self.Ins_Name)
    popup_content.add_widget(self.Ins_dept)
    popup.open()


def delete_ins(self):
    self.parent.parent.dismiss()

    def CoursesByinstructor(self, dt):
        Ins_Selected = self.All_Ins.adapter.selection
        print Ins_Selected
        """
            SQL, courses give the by the instructor. list of lists [[id, [name, surname, dept]]
        """


        if len(Ins_Selected) == 0:
            """
             SQL get all the courses, list of lists [[courseCode, name]]
            """
            Data = [["21725245", ["Fahe", "Saellioglu", "Cs"]], ["21715245", ["Fahe", "Saellioglu", "Cs"]],["21725245", ["Fahed", "Sabellioglu", "Cs"]]]
            self.Courses.adapter.data = Data
            self.Courses.populate()

        else:
            Data = [["21725245", ["Fahe", "Saellioglu", "Cs"]], ["21725245", ["Fahed", "Sabellioglu", "Cs"]]]
            self.Courses.adapter.data = Data
            self.Courses.populate()


    def Delete(dt):
        Ins_Selected = self.All_Ins.adapter.selection
        Course = self.Courses.adapter.selection
        # print Ins_Selected
        if len(Ins_Selected) == 0 and len(Course) == 0:
            print "Please Choose"
        elif len(Course) == 0 and len(Ins_Selected) != 0:
            """
                SQl, delete the instructor from all his courses
            """
            print "delete the instructor from all his courses"
        elif len(Ins_Selected) == 0 and len(Course) != 0:
            """
                SQL, delete the instructor for the chosen courses
            """
            print "delete the instructor for the chosen courses"

        elif len(Ins_Selected) != 0 and len(Course) != 0:
            """
                SQL, delete the chosen instructor from the chosen coruses.
            """
            print "delete the chosen instructor from the chosen coruses"
        # elif len()
        # for line in selected:
        #     RowText = re.findall(r"\d{7,9}|\w+\s\d{3}",line.text)
        #     self.list_quests.adapter.data.remove(RowText)
        #     self.list_quests._trigger_reset_populate()

    self.IDs = {'21725241': ["Cs 240", "ENGR 102", "ENGR 101", "Cs 350"],
                '21725242': ["Cs 240", "ENGR 102", "ENGR 101", "Cs 350"],
                '21725243': ["Cs 240", "ENGR 102", "ENGR 101", "Cs 350"],
                '21725254': ["Cs 240", "ENGR 102", "ENGR 101", "Cs 350"]}
    Data = {"21725242": ["Fahed", "Sabellioglu", "Cs"], "21725244": ["Fahed", "Sabellioglu", "Cs"],
            "21725246": ["Fahed", "Sabellioglu", "Cs"], "21725248": ["Fahed", "Sabellioglu", "Cs"],
            "21725243": ["Fahed", "Sabellioglu", "Cs"], "21725245": ["Fahed", "Sabellioglu", "Cs"],
            "21725247": ["Fahed", "Sabellioglu", "Cs"], "21725249": ["Fahed", "Sabellioglu", "Cs"]
        , "21722247": ["Fahed", "Sabellioglu", "Cs"], "21225249": ["Fahed", "Sabellioglu", "Cs"],
            "21715247": ["Fahed", "Sabellioglu", "Cs"], "11725249": ["Fahed", "Sabellioglu", "Cs"]}


    self.data_all_ids = {'Cs 240': "Data analysis", "Cs 350": "Database", "ENGR 102": "Programming Practice",
                         "ENGR 101": "Introduction to programming"}

    popup_content = FloatLayout()
    popup_content.add_widget(Label(text="Instructors", pos_hint={"center_x": .2, "center_y": .99}))
    popup_content.add_widget(Label(text="Courses", pos_hint={"center_x": .75, "center_y": .99}))

    self.popup = Popup(id="pop", title="Report", font_name="data/font/CaviarDreams_Bold.ttf", title_size=23,
                       title_align="center",content=popup_content, separator_color=[0, 0, 0, 0.1], size_hint=(None, None),
                       size=(self.width / .20, (float(self.parent.height) / .140) - 90), background="data/img/BACK.png",
                       pos_hint={"center_x": .5, "center_y": .50})

    """All course in the uni"""

    self.Courses = ListView(size_hint=(.5, .75), pos_hint={"center_x": .75, "center_y": .58})

    args_converter = lambda row_index, x: {"text": "Code: {id} - Name: {N} ".format(id=x[0], N=" ".join(x[1][0:2])),
                                            "markup": True, "selected_color": (.50, .50, .40, 0.6), "deselected_color": (.0, .2, .2, 0.3),
                                            "font_name": "data/font/CaviarDreams_Bold.ttf", "font_size": self.height / 3.5,
                                            "size_hint_y": None, "size_hint_x": 1, "height": self.height / 1.2}

    """
        SQL get all the courses, list of lists [[courseCode, name]]
    """

    self.Courses.adapter = ListAdapter(data=[[Course, self.data_all_ids[Course]] for Course in self.data_all_ids], selection_limit=-1,
                                        cls=ListItemButton,args_converter=args_converter, allow_empty_selection=True)



    """All instructors in the uni"""


    self.All_Ins = ListView(size_hint=(.45, .75), pos_hint={"center_x": .2, "center_y": .58})

    Ins_Convertor = lambda row_index, x: {"text": "Name: {N} - Dept: {D} ".format(N=" ".join(x[1][0:-1]), D=x[1][-1]), "markup": True,
                                              "selected_color": (.50, .50, .40, 0.6),"deselected_color": (.0, .2, .2, 0.3),
                                              "font_name": "data/font/CaviarDreams_Bold.ttf",  "font_size": self.height / 3.5, "size_hint_y": None,
                                              "size_hint_x": 1, "height": self.height / 1.2, "on_release": partial(CoursesByinstructor, self)}

    """
        SQL all instructors in the university, list of lists [[Name, dept]
    """


    self.All_Ins.adapter = ListAdapter(data=[[Ins, Data[Ins]] for Ins in Data],
                                          selection_limit=-1,cls=ListItemButton, args_converter=Ins_Convertor,allow_empty_selection=True)


    popup_content.add_widget(Button(text="Delete", font_name="data/font/LibelSuit.ttf", font_size=self.height / 2.3,
                                    background_normal="data/img/widget_red.png", background_down="data/img/widget_red.png",
                                     size_hint_x=.25,
                                    size_hint_y=None, height=self.height / 1.8, on_release=Delete,
                                    pos_hint={"center_x": .35, "center_y": .47 - ( len(self.All_Ins.adapter.data) * self.height / 1.5) / 1000}))

    popup_content.add_widget(Button(text="Close", font_name="data/font/LibelSuit.ttf", id='CloseButton', font_size=self.height / 2.3,
                                     background_normal="data/img/widget_red.png", background_down="data/img/widget_red.png",
                                      size_hint_x=.25, size_hint_y=None,
                                     height=self.height / 1.8, pos_hint={"center_x": .65, "center_y": .47 - (
                                                    len(self.All_Ins.adapter.data) * self.height / 1.5) / 1000},
                                     on_release=self.popup.dismiss))

    self.popup.open()
    popup_content.add_widget(self.Courses)
    popup_content.add_widget(self.All_Ins)




def add_course(self):
    print "add course"
    self.parent.parent.dismiss()
    popup_content = FloatLayout()

    def Add(dt):
        Code = self.CourseCode.text.strip()
        Title = self.CourseTitle.text.strip()
        Credits = self.Credits.text.strip()
        Ins = self.All_Ins.adapter.selection
        if not Code or not Title or not Credits:
            print "Please Fill"
        else:
            print "adding"
            """
                Commands for adding a new Course
            """
            popup.dismiss()

    """
        SQL Commands to bring all courses, form a list of lists with course_code and name
    """

    self.data_all_ids = {'Cs 240': "Data analysis", "Cs 350": "Database", "ENGR 102": "Programming Practice",
                         "ENGR 101": "Introduction to programming", 'Cs 140': "Data analysis",
                         'Cs 250': "Data analysis", 'Cs 220': "Data analysis", 'Cs 210': "Data analysis"
        , 'Cs 141': "Data analysis", 'Cs 270': "Data analysis", 'Cs 280': "Data analysis", }  # """Fake Data"""

    Data = {"21725242": ["Fahed", "Sabellioglu", "Cs"], "21725244": ["Fahed", "Sabellioglu", "Cs"],
            "21725246": ["Fahed", "Sabellioglu", "Cs"], "21725248": ["Fahed", "Sabellioglu", "Cs"],
            "21725243": ["Fahed", "Sabellioglu", "Cs"], "21725245": ["Fahed", "Sabellioglu", "Cs"],
            "21725247": ["Fahed", "Sabellioglu", "Cs"], "21725249": ["Fahed", "Sabellioglu", "Cs"]
        , "21722247": ["Fahed", "Sabellioglu", "Cs"], "21225249": ["Fahed", "Sabellioglu", "Cs"],
            "21715247": ["Fahed", "Sabellioglu", "Cs"], "11725249": ["Fahed", "Sabellioglu", "Cs"]}

    self.CourseCode = TextInput(hint_text="Course Code", id="CourseCode", multiline=False,
                               font_name="data/font/CaviarDreams_Bold.ttf", font_size=self.parent.parent.parent.height / 25,
                               background_normal="data/img/widget_gray_75.png", background_active="data/img/widget_red_select.png",
                                padding_y=[self.parent.parent.parent.height / 150, 0],
                               size_hint_x=.30, size_hint_y=.1,pos_hint={"center_x": .18, "center_y": .855}, write_tab=False)

    self.Credits = TextInput(hint_text="Credits", id="CourseCredits", write_tab=False, multiline=False,
                          font_name="data/font/CaviarDreams_Bold.ttf", font_size=self.parent.parent.parent.height / 25,
                          background_normal="data/img/widget_gray_75.png", background_active="data/img/widget_red_select.png",
                          padding_y=[self.height / 100, 0],
                          size_hint_x=.30, size_hint_y=.1, pos_hint={"center_x": .18, "center_y": .550})

    self.CourseTitle = TextInput(hint_text="Course Title", id="user_password", multiline=False,
                          font_name="data/font/CaviarDreams_Bold.ttf"
                          , font_size=self.parent.parent.parent.height / 25,
                          background_normal="data/img/widget_gray_75.png",
                          background_active="data/img/widget_red_select.png",

                          padding_y=[self.parent.parent.parent.height / 100, 0], size_hint_x=.30, size_hint_y=.1,
                          pos_hint={"center_x": .18, "center_y": .700}, write_tab=False)



    """ All instructors in the uni"""
    self.All_Ins = ListView(size_hint=(.45, .75), pos_hint={"center_x": .75, "center_y": .58})

    Ins_Convertor = lambda row_index, x: {"text": "Name: {N} - Dept: {D} ".format(N=" ".join(x[1][0:-1]), D=x[1][-1]), "markup": True,
                                              "selected_color": (.50, .50, .40, 0.6),"deselected_color": (.0, .2, .2, 0.3),
                                              "font_name": "data/font/CaviarDreams_Bold.ttf",  "font_size": self.height / 3.5, "size_hint_y": None,
                                              "size_hint_x": 1, "height": self.height / 1.2}

    """
        SQL all instructors in the university, list of lists [[Name, dept]
    """


    self.All_Ins.adapter = ListAdapter(data=[[Ins, Data[Ins]] for Ins in Data],
                                          selection_limit=1,cls=ListItemButton, args_converter=Ins_Convertor,allow_empty_selection=True)


    popup = Popup(title="Course Details", title_color=[0, 0, 0, 1], title_align="center",
                  font_name="data/font/LibelSuit.ttf", title_size=19,
                  content=popup_content, separator_color=[0.0, 0.0, 0.0, 0.4], size_hint=(None, None),
                  size=(self.parent.parent.parent.width / 1.2, self.parent.parent.parent.height / 1.2),
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

    popup_content.add_widget(self.CourseCode)
    popup_content.add_widget(self.CourseTitle)
    popup_content.add_widget(self.Credits)
    popup_content.add_widget(self.All_Ins)

    popup.open()






def delete_course(self):
    self.parent.parent.dismiss()

    def StudentInCourse(self, dt):
        Data = [["21725245", ["Fahe", "Saellioglu", "Cs"]], ["21725245", ["Fahed", "Sabellioglu", "Cs"]]]

        """
            get all the students who take the chosen class as list of lists [[id,[name,surname,dept]]
        """
        self.AllCourses.adapter.data = Data
        self.AllCourses.populate()

    def Delete(dt):
        Courses = self.Courses.adapter.selection
        print "in"

        if len(Courses) == 0:  # did not chose any
            print "Chose a Course first"

        elif len(Courses) != 0:  # chose a course but not a student
            """
                SQL delete courses 
            """
            print "Delete course"
        # for line in selected:
        #     RowText = re.findall(r"\d{7,9}|\w+\s\d{3}",line.text)
        #     self.list_quests.adapter.data.remove(RowText)
        #     self.list_quests._trigger_reset_populate()


    self.data_all_ids = {'Cs 240': "Data analysis", "Cs 350": "Database", "ENGR 102": "Programming Practice",
                         "ENGR 101": "Introduction to programming"}

    popup_content = FloatLayout()
    # popup_content.add_widget(Label(text="Courses", pos_hint={"center_x": .2, "center_y": .99}))
    # popup_content.add_widget(Label(text="Students", pos_hint={"center_x": .75, "center_y": .99}))

    self.popup = Popup(id="pop", title="Report", font_name="data/font/CaviarDreams_Bold.ttf", title_size=23,
                       title_align="center",
                       content=popup_content, separator_color=[0, 0, 0, 0.1], size_hint=(None, None),
                       size=(self.width / .200, (float(self.parent.height) / .140) - 90)
                       , background="data/img/BACK.png", pos_hint={"center_x": .5, "center_y": .45})



    self.Courses = ListView(size_hint=(.8, .5), pos_hint={"center_x": .5, "center_y": .68})

    args_converter = lambda row_index, x: {"text": "Code: {id} - Name: {N} ".format(id=x[0], N=x[1]),
                                            "markup": True, "selected_color": (.50, .50, .40, 0.6), "deselected_color": (.0, .2, .2, 0.3),
                                            "font_name": "data/font/CaviarDreams_Bold.ttf", "font_size": self.height / 3.5,
                                            "size_hint_y": None, "size_hint_x": 1, "height": self.height / 1.2}

    """
        SQL get all the courses, list of lists [[courseCode, name]]
    """
    self.Courses.adapter = ListAdapter(data=[[Course, self.data_all_ids[Course]] for Course in self.data_all_ids],  selection_mode = "multiple",
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


def load_string(File):

    with open("{FileName}.RA".format(FileName = File),"r") as KivyFile:
        Builder.load_string(KivyFile.read())


def AttendanceLogin(self):
    if self.ids["CheckLogin"].active == False:
        if len(self.ids["input_userid"].text.strip()) == 0 :
            self.ids["warning"].opacity = 1
            return False
        else:
            self.ids['warning'].opacity = 0
            return True
    elif self.ids['CheckLogin'].active == True:
        if len(self.ids["input_userid"].text.strip()) == 0 or  len(self.ids["input_password"].text.strip()) == 0:
            self.ids["warning"].opacity = 1
            return False
        else:
            self.ids["warning"].opacity = 0
            return True
def Calendar(self,Value):
        layout = self.ids['BOX']
        self.cols = 7
        self.c = calendar.monthcalendar(2019,Value)
        Days = ["Mo","Tu",'We',"Th","Fr","Sa","Su"]
        for Day in Days:
            layout.add_widget(Button(text=Day,color=[ 1,1,1,1],font_name= "data/font/CaviarDreams_Bold.ttf",background_color = [0.0,0.0,0.0,0.76],disabled=True))
        for i in self.c:
            for j in i:
                if j == 0:
                    layout.add_widget(Button(on_release=self.on_release, text='{j}'.format(j=''),background_color = [0.0,0.0,0.0,0.76]))
                else:
                    layout.add_widget(Button(on_press=self.on_release, text='{j}'.format(j=j),color=[ 1,1,1,1],font_name= "data/font/CaviarDreams_Bold.ttf",background_color = [0.0,0.0,0.0,0.76],id = '{j}'.format(j=j)))


def NotePopUp(self,Day):
    def Call(obj,value):
        print self.list_quests.adapter.selection
        print obj, value
    popup_content = FloatLayout()
    UserId = Cache.get("User","username")
    if  Cache.get("counter",'value') == None:
        Month = 1
    else:
        Month = Cache.get("counter",'value')

    """
        SQL, get all the attendence for the user for the chosen day and month
    """

    self.data_all_ids = {'Cs240':"Data analysis","Cs350":"Database","ENGR 102":"Programming Practice","ENGR 101":"Introduction to programming"}
    self.IDs = {'217252543':["Cs240","ENGR 102","ENGR 101","Cs350"]}

    self.popup = Popup(title="Report",font_name = "data/font/CaviarDreams_Bold.ttf",title_size = 19,title_align = "center",
                    content=popup_content,separator_color=[0,0,0, 0.1], size_hint=(None, None),
                    size=(self.width / .110, self.height / .138), background="data/img/BACK.png",)

    self.list_quests = ListView(size_hint=(1, .9), pos_hint={"center_x": .5, "center_y": .55})

    args_converter = lambda row_index, x: {"text": "ID: {id} - Course: {C} - Title: {T}".format(id=x[0],C=x[1],T = x[2]),
                                           "markup": True,"selected_color": (.50, .50, .40, 0.6),"deselected_color": (.0, .2, .2, 0.3),
                                           "font_name": "data/font/CaviarDreams_Bold.ttf", "font_size": self.height / 4,
                                           "size_hint_y": None, "size_hint_x":1, "height": self.height / 1.5, }


    self.list_quests.adapter = ListAdapter(data=[[Student,course,self.data_all_ids[course]] for Student in self.IDs for course in self.IDs[Student]],
                                           selection_mode = "multiple", cls=ListItemButton, args_converter=args_converter,allow_empty_selection=False )

    popup_content.add_widget(self.list_quests)

    popup_content.add_widget(Button(text="Close", font_name="data/font/LibelSuit.ttf",
                                    font_size=self.height / 3,background_normal="data/img/but_red_down.png",
                                    background_down="data/img/but_red_down.png",size_hint_x=.15,
                                    size_hint_y=None,height=self.height / 2,pos_hint={"center_x": .5, "y": .0},
                                    on_release=self.popup.dismiss))


    self.popup.open()


def ChangePage(pages,screen):
    try:
        screen.switch_to(pages[1])
    except:
        screen.current_name = pages[1].name
    finally:
        del pages[1]