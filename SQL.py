import mysql.connector as sql
import datetime
import calendar

database = sql.connect(host='localhost',user='root',passwd="Fahed@1Karim",database = 'attendance_project')
c = database.cursor()


def prof_courses(prof_id):
    c.execute('select * from course where i_id={i}'.format(i=prof_id))
    allcourses = c.fetchall()
    return allcourses

def prof_students(prof_id):
    courses = prof_courses(prof_id)
    courses_students = {}
    for r in courses:
        code = str(r[2])
        c.execute("select * from takes where course_code='{CODE}'".format(CODE = code))
        results = c.fetchall()
        courses_students[code] = results
    return courses_students

def uni_students():
    c.execute("select * from student")
    return c.fetchall()

def uni_courses():
    c.execute("select * from course")
    return c.fetchall()

def delete_student_allcourses(ids): #delete a student from all courses
    for st_id in ids:
        c.execute("delete from takes where Id = {id}".format(id=st_id))
        database.commit()

def delete_student_course(ids,c_ids): #delete a student from some courses
    query = """delete from takes where Id={std_id} and course_code='{c_id}'"""
    for st_id in ids:
        for course_id in c_ids:
            c.execute(query.format(std_id = st_id, c_id = course_id))
        database.commit()

def delete_allstudent_course(c_id): #delete all students from a course
    for course in c_id:
        c.execute("delete from takes where course_code='{code}'".format(code = course))
        database.commit()

def coursesWIns():
    c.execute("""select * from course where i_id is null""")
    data = c.fetchall()
    return data

"""register a new student with courses or without"""
def register_student_w_courses(st_name,st_surname,dept,st_bank_card,st_id,email,courses=[]): # add a new student to some courses
    try:


        c.execute("""insert into student values ("{name}","{surname}","{dep}",'{card_id}',{id},'{email}')""".format(name = st_name,surname = st_surname,dep = dept,
                                                                                                      card_id = st_bank_card,id = st_id,email = email))
        query = """insert into takes values ({id},'{course_code}')"""
        for course in courses:
            c.execute(query.format(id=st_id, course_code=course))

        database.commit()
        return 1
    except Exception as E:
        return 0



"""Register already existed student to some courses, Admin"""

def register_student_2_courses(st_id,courses):  #add a student to some courses
    query = """insert into takes values ({id},'{course_code}')"""
    failed = []
    for course in courses:
        try:
            c.execute(query.format(id = st_id,course_code = course))
            database.commit()
        except:
            failed.append(course)
    if len(failed) == 0:
        return 0
    elif len(failed) != 0:
        return failed

"""New courses that could be the student registered to, To show new courses"""
def new_courses_students(st_id):  # register a student to courses he is not taking, admin
    query = """select * from course where course_code not in (select course_code from takes where Id={id})"""
    c.execute(query.format(id = st_id))
    takenCourses = c.fetchall()
    return takenCourses

def register_st_to_profC(st_id,prof_id):  #register a student to the courses that the prof is giving, inst
    profGive = prof_courses(prof_id)
    newcourse = new_courses_students(st_id)
    return [course for course in newcourse if course in profGive]

def course_taken_st(st_id):
    allcourses = uni_courses()
    c.execute("""select course_code from takes where Id = {id}""".format(id = st_id))
    taken = [c_title[0] for c_title in c.fetchall()]
    return [t for t in allcourses if t[2] in taken]


def courses_taken():
    c.execute("select * from course where course_code in (select distinct course_code from takes)")
    data = c.fetchall()
    return data

def students_taking_courses(c_id = None):
    if c_id == None:
        c.execute('select * from student where Id in (select distinct Id from takes)')
    else:
        c.execute(""" select * from student where Id in (select Id from takes where course_code='{code}')""".format(code = c_id))
    data = c.fetchall()
    return data


def getCommonCourses(ids):
    query = """select * from takes where Id={id}"""
    common = {}
    for id in ids:
        c.execute(query.format(id = id))
        common[id] = [r[1] for r in c.fetchall()]
    CommonCourse = list(reduce(set.intersection,(set(val) for val in common.values())))
    info = """select * from course where course_code='{code}'"""
    results = []
    for name in CommonCourse:
        c.execute(info.format(code = name))
        results.extend(c.fetchall())
    return results

def getStudentsfromCourses(codes):
    query = """select Id from takes where course_code = '{code}'"""
    common = {}
    for code in codes:
        c.execute(query.format(code = code))
        common[code] = c.fetchall()
    CommonStudents = [st[0] for st in reduce(set.intersection,(set(val) for val in common.values()))]
    info = """select * from student where id = {ID}"""
    results = []
    for student in CommonStudents:
        c.execute(info.format(ID = student))
        results.extend(c.fetchall())
    return results


def reg_ins(name,surname,email,dept,passwd,courses=[]):
    c.execute("""insert into instructor values ('{n}','{s}','{e}','{d}',0,'{p}')""".format(n = name,s = surname,e = email,
                                                                                          d = dept,p =passwd))
    database.commit()
    c.execute("""select id from instructor where email='{e}'""".format(e = email))
    id = c.fetchall()[0][0]
    for course in courses:
        c.execute("""update course set i_id = {ins_id} where course_code='{code}'""".format(ins_id = id,code =course ))
        database.commit()


def getInsWCourses():
    c.execute("""select * from instructor """)
    data = c.fetchall()
    return data


def reg_course(title,credits,code,ins):
    try:
        query = """insert into course values ('{t}',{cr},'{Code}',{i_id})"""
        c.execute(query.format(t= title,cr = credits,Code = code,i_id =ins))
        database.commit()
        return 1
    except:
        return 0


def inscourses(id):
    c.execute("""select * from course where i_id = {id}""".format(id= id))
    data = c.fetchall()
    return data


def coursesWithIns():
    c.execute("""select * from course where i_id is not null""")
    data = c.fetchall()
    return data

def del_ins_all_courses(i_id):
    c.execute("""update course set i_id={v} where i_id={n}""".format(v = "NULL",n = i_id))
    database.commit()

def del_ins_4_courses(c_ids):
    for c_id in c_ids:
        c.execute("""update course set i_id={n} wherer course_code='{c}'""".format(n ="NULL",c = c_id))
        database.commit()


def del_ins_2_course(i_id,c_ids):
    for c_id in c_ids:
        c.execute("""update course set i_id = {n} where course_code='{c}' and i_id = {v} """.format(n = "NULL",c = c_id,v = i_id))
        database.commit()


def get_ins_4_courses(c_ids):
    ins = {}
    for c_id in c_ids:
        c.execute("""select * from instructor where id in (select distinct i_id from course where course_code = '{c}')""".format(c = c_id))
        ins[c_id] = c.fetchall()
    CommonIns = [st for st in reduce(set.intersection, (set(val) for val in ins.values()))]
    return CommonIns


def del_coures(c_ids):
    for c_id in c_ids:
        c.execute("""delete from course where course_code='{code}'""".format(code =c_id))
        database.commit()

def get_ins_info(email):
    c.execute("select * from instructor where email='{e}'".format(e = email))
    data = c.fetchall()
    return data



def updatepass(old,new,email):
    c.execute("""select exists(select * from instructor where email='{e}' and password = '{p}')""".format(e = email,p = old))
    data =  c.fetchall()[0][0]
    if data:
        c.execute("""update instructor set password = '{p}' where email='{e}'""".format(p =new,e = email ))
        database.commit()
        return data
    else:
        return data


def add_students_w_courses(student_list,courses_list):
    query ="""insert into student (id,name,surname,dept,email) values (%s,%s,%s,%s,%s)"""
    coursequery = """insert into takes values ({id},'{course_code}')"""
    for course in courses_list:
        for student in student_list:
            try:
                c.executemany(query,[student])
                c.execute(coursequery.format(id=student[0], course_code=course))
                database.commit()
            except :
                c.execute(coursequery.format(id=student[0], course_code=course))
                database.commit()

def attendance_report(st_id,date):
    query = """select * from attendance where id={id} and Day(date) = {d} and Month(date) = {m}"""
    c.execute(query.format(id = st_id,d = date[0],m = date[2]))
    return c.fetchall()

def getcourseinfo(c_code):
    query = """select title from course where course_code = '{code}'"""
    c.execute(query.format(code = c_code))
    try:
        return c.fetchall()[0][0]
    except:
        return []

def card_exist(number):
    query = """select * from student where bank_card_id = '{card}'"""
    c.execute(query.format(card = number))
    try:
        return c.fetchall()
    except:
        return "Does not exist"

def new_card(email,cardnumber):
    query = """update student set bank_card_id = '{card}' where email='{e}'"""
    c.execute(query.format(card = cardnumber,e = email))
    database.commit()

def email_exist(email):
    query = """select * from student where email = '{e}'"""
    c.execute(query.format(e = email))
    if len(c.fetchall()) != 0:
        return True
    else:
        return False


def attendance(card_id):
    query = """select id from student where bank_card_id = '{i}'"""
    now = datetime.datetime.now()
    c.execute(query.format(i=card_id))
    studentdata = c.fetchall()[0]
    day = calendar.day_name[now.weekday()]
    Hour = now.hour
    coursesquery = """select * from schedule where course_code in (select course_code from takes where id = {id}) and day = '{d}' and hour(start_hour) <= {t} and hour(end_hour) > {t} """
    try:
        c.execute(coursesquery.format(id=studentdata[0], d=day,t = Hour))
        courses = c.fetchall()
        time = datetime.datetime.now().time().strftime("%H:%M:%S")
        check = """select id from attendance where course_code = '{c}' and date = '{d}' and hour(Hour) = '{h}'"""
        c.execute(check.format(c = courses[0][-1],d = now.date(),h = now.hour))
        checkedattendance = c.fetchall()
        if len(checkedattendance) == 0:
            attendancequery = """insert into attendance values ({id},'{code}','{d}','{h}')"""
            c.execute(attendancequery.format(id = studentdata[0],code = courses[0][-1],d = datetime.datetime.now().date(),h =time))
            database.commit()
            print 'taken'
            return 1
        else:
            print 'already'
            return -1
    except Exception as e:
        return 0

def studentlogin(id):


    query = """select * from student where id ={d}"""
    try:
        c.execute(query.format(d = int(id)))
        data = c.fetchone()
        return data
    except:
        return None


def ins_login(email,password):
    query = """select * from instructor where email = '{e}' and password = '{p}'"""
    c.execute(query.format(e = email,p = password))
    data = c.fetchone()
    if data == None:
        return data
    else:
        return data


def student_info(st_id):
    query = """select * from student where id = {d}"""
    c.execute(query.format(d = st_id))
    return c.fetchall()

def ins_info(ins_email):
    query = """select * from instructor where email = '{e}'"""
    c.execute(query.format(e = ins_email))
    return c.fetchall()


def all_rooms():
    query = """select * from classroom"""
    c.execute(query)
    return c.fetchall()


def find_ins_id(email):
    query = """select id from instructor where email = '{e}'"""
    c.execute(query.format(e = email))
    data = c.fetchall()
    if len(data) == 0:
        return None
    else:
        return data



def course_schedule(start,end,day,classroom_id,course_code):

    coursecheck = """select course_code from course where course_code = '{course_code}'"""
    c.execute(coursecheck.format(course_code = course_code,id = classroom_id))
    check = c.fetchall()
    if len(check) != 0:
        courses  = """select * from schedule where day = '{d}' and classroom_id = '{id}'"""
        c.execute(courses.format(d = day,id = classroom_id))
        data = c.fetchall()
        try:
            start_object = datetime.datetime.strptime(start, '%H:%M').time()
            end_object =  datetime.datetime.strptime(end, '%H:%M').time()
        except:
            start_object = datetime.datetime.strptime(start+":00", '%H:%M').time()
            end_object = datetime.datetime.strptime(end+":00", '%H:%M').time()
        for sch in data:
            sch_start = (datetime.datetime.min + sch[0]).time()
            sch_end = (datetime.datetime.min + sch[1]).time()

            if sch_start < start_object < sch_end or sch_start < end_object < sch_end:
                return "overlap with " + sch[4] + " on " + sch[2]
        try:
            query = """insert into schedule values ( '{start}','{end}','{day}',{c_id},'{c_code}') """
            c.execute(query.format(start = start, end = end,day = day.title(), c_id = classroom_id,c_code = course_code.upper()))
            database.commit()
            return "Saved"
        except:
            return "Course Code Duplicate"

    else:
        return "No Such Course"



def find_class_id(number):
    query = """select id from classroom  where room_number = {r} and building = '{d}'"""
    c.execute(query.format(d = int(number[0]),r = int(number[1:])))
    return c.fetchall()



def get_ins_courses(ins_id):
    query = """select * from course where i_id = {d} """
    c.execute(query.format(d = int(ins_id)))
    return c.fetchall()