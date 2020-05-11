import datetime
import pickle
from core.assist_functions import *


class School:
    """
    学校类，包括学校的具体信息，以及一个为调用学校具体信息做的接口
    """
    def __init__(self, course, origin_price, start_date, period, location):
        """
        学校类具体信息
        :param course: 课程
        :param origin_price: 课程价格
        :param start_date: 开课日期
        :param period: 时长（以天为单位）
        :param location: 上课地点
        """
        self.course = course
        self.price = origin_price
        year, month, day = map(int, start_date.split(','))
        self.start_date = datetime.date(year, month, day)
        self.period = period
        self.end_date = self.start_date + datetime.timedelta(period)
        self.teacher_list = []
        self.student_list = []
        self.location = location
        self.school = "Roger's %s" % location

    def subject_info_show(self):
        """
        为调用学校的课程信息做的接口
        :return: 返回信息
        """
        info = ("""校区: %s\n课程名称: %s\n课程价格: %s\n开始日期: %s\n结束日期: %s\n指导老师: %s"""
                % (self.school, self.course, self.price, self.start_date, self.end_date, self.teacher_list))
        return info


class Character:
    """
    一些共有类的调用，如展示课程以及课程选择
    """
    def show_courses(self, *args):  # Studnet/Mamager
        """
        展示课程具体信息并返回课程信息列表以及具体课程信息
        :return: 返回课程信息列表以及课程信息
        """
        count = 0
        course_info_list = []
        for course_name in course_info:
            count += 1
            obj = course_info[course_name]
            print(count, obj.subject_info_show())
            course_info_list.append((obj.subject_info_show(), obj))
        return course_info_list, course_info

    def course_selection(self, *args):  # Teacher/Student
        """
        选课信息的筛选过程
        :return: 若选择成功，返回课程对象，否则返回None
        """
        course_info_list, course_info = self.show_courses()
        func = input_for_list(course_info_list)
        if func.course in self.course:
            print('已选该课程，请重新选择')
            return None
        else:
            if self.school is None:
                confirmation = input('注意：所选为%s校区，是否确认（请输入Y或者N）' % func.location)
                if confirmation.upper() == 'N':
                    return None
            elif func.school != self.school:
                print('所选校区为<%s>,与绑定校区<%s>不符，请重新选择！' % (func.school, self.school))
                return None
        return func


class Student(Character):
    """
    学生类窗口信息，继承Character(共有类)
    """
    operator_list = [('查看可选课程', 'show_courses'),
                     ('选择课程', 'pick_course'),
                     ('显示所选课程', 'view_course'),
                     ('查看成绩', 'view_grade'),
                     ('交学费', 'pay_tuition'),
                     ('退出', 'exit')]

    def __init__(self, name, password):
        """
        学生具体信息
        :param name: 用户名
        :param password: 密码
        """
        self.name = name
        self.password = password
        self.course = []  # 学生的课程列表
        self.school = None  # 学校锁定，不可以跨学校选课
        self.tuition = 0
        self.tuition_remaining = 0
        self.grade = []  # 成及列表

    def pick_course(self, *args):
        """
        选择课程，并打印结果
        :return:
        """
        func = self.course_selection()
        if course_info is None:
            print('暂无课程')
            return
        elif func is None:
            return
        else:
            self.course.append(func.course)
            self.school = func.school
            course_info[func.course].student_list.append(self.name)
            self.tuition += func.price
            self.tuition_remaining += func.price
            print('<%s>课程选择成功, 校区<%s>' % (func.course, func.school))

    def view_course(self, *args):
        """
        显示可选课程
        """
        count = 0
        for info in self.course:
            count += 1
            print(count, course_info[info].subject_info_show())

    def view_grade(self, *args):
        if len(self.grade) < 1:
            print('尚无成绩录入')
        else:
            for grade_info in self.grade:
                print('课程: %s 成绩: %s' % (grade_info[0],grade_info[1]))

    def pay_tuition(self, *args):
        if self.tuition_remaining == 0:
            print('您的学费已交齐～')
        else:
            print('还有¥%s待支付' % self.tuition_remaining)
            payment = int(input('请输入您想支付的金额：'))
            pss = input('请输入密码：')
            if pss == self.password:
                self.tuition_remaining -= payment
                print('支付成功，剩余学费¥%s待交' % self.tuition_remaining)
            else:
                print('密码错误，支付失败')

    def exit(self, *args):
        """
        将改变信息写入对一个文档并退出程序
        """
        with open('data/Student_info.pickle', 'wb') as f:
            pickle.dump(args[0], f)
        with open('data/course_info.pickle', 'wb') as f:
            pickle.dump(course_info, f)
        exit()


class Teacher(Character):
    """
    教师类（继承character）
    """
    operator_list = [('课程选择', 'teach_courses'),
                     ('显示所教课程详细信息', 'view_courser_details'),
                     ('查看班级学生', 'view_students'),
                     ('移除学生', 'remove_student'),
                     ('登入及修改学生成绩','student_grade_adjustment'),
                     ('退出', 'exit')]


    def __init__(self, name, password):
        """
        教师信息
        :param name: 姓名
        :param password: 密码
        """
        self.name = name
        self.password = password
        self.course = []  # 任课课程列表（后规定只能唯一）
        self.school = None

    def teach_courses(self, *args):
        """
        所择任课（规定只可任一节课的老师）
        """
        if len(self.course) > 0:
            print('已选课程，无需添加')
        else:
            func = self.course_selection()
            if course_info is None:
                print('暂无课程')
                return
            elif func is None:
                return
            else:
                if len(func.teacher_list) > 0:
                    print('任课老师已满，请选择剩余课程！')
                else:
                    self.course.append(func.course)
                    self.school = func.school
                    course_info[func.course].teacher_list.append(self.name)  # 添加到课程的任课老师信息中
                    print('<%s>课程选择成功, 校区<%s>' % (func.course, func.school))

    def view_courser_details(self, *args):
        """
        看任课课程详细信息
        """
        count = 0
        for info in self.course:
            count += 1
            print(count, course_info[info].subject_info_show())

    def view_students(self, *args):
        """
        看任课课程的学生信息，包括学号姓名以及成绩
        :return: 若存在学生，返回学生列表已经，任课信息，不存在返回None，None
        """
        if len(self.course) > 0:
            subject = self.course[0]
            student_list = course_info[subject].student_list
            for sequence, stu in enumerate(student_list, 1):
                grade = student_info[stu].grade
                print('No.%s  name: %s  grade: %s' % (sequence, stu, grade))
            return student_list, course_info
        else:
            print('暂无学生')
            return None,None

    def remove_student(self, *args):
        """
        移除任教课程的学生，并提供确认判断
        """
        student_list, course_info = self.view_students()
        remove_num = input('请输入需要移除的学生序号或输入B返回菜单：')
        if remove_num.upper() == 'B':
            return
        else:
            remove_num = int(remove_num) - 1
            remove_stu = student_list[remove_num]
            confirmation = input('你确定要删除%s?（请输入Y or N）' % remove_stu)
        if confirmation.upper() == 'Y':
            student_list.remove(remove_stu)
            student_info[remove_stu].course.remove(self.course[0])
        else:
            return

    def student_grade_adjustment(self,*args):
        """
        学生成绩录入，不选择退出持续循环，可更改信息
        """
        while True:
            stu_list, course_info = self.view_students()
            stu_num = input('请输入学生学号(或输入B返回菜单)：')
            if stu_num.upper() != 'B':
                stu_num = int(stu_num)-1
                stu_name = stu_list[stu_num]
                grade = int(input('成绩为：'))
                student_info[stu_name].grade.append((self.course[0],grade))
            else:
                break

    def exit(self, *args):
        """
        将改变信息写入对一个文档并退出程序
        """
        with open('data/Teacher_info.pickle', 'wb') as f:
            pickle.dump(args[0], f)
        with open('data/course_info.pickle', 'wb') as f:
            pickle.dump(course_info, f)
        with open('data/Student_info.pickle', 'wb') as f:
            pickle.dump(student_info, f)
        exit()


class Manager(Character):
    """
    管理员类（继承Character)
    """
    operator_list = [('创建新账号', 'manager_build'),
                     ('创建课程', 'course_build'),
                     ('查看所有课程信息', 'show_courses'),
                     ('查看所有学生选课信息', 'show_student_courses'),
                     ('查看所有教师任课信息', 'show_teacher_courses'),
                     ('教师调配', 'teacher_allocation'),
                     ('退出', 'exit')]


    def __init__(self, name, password):
        """
        管理员信息
        :param name: 用户名
        :param password: 密码
        """
        self.name = name
        self.password = password

    def manager_build(self, *args):
        """
        创建账户，可创建三方账户，但创建的账户只能在重启后使用，进入创建账户窗口不可返回
        """
        manager_build_list = [('管理员账号', 'Manager'),
                              ('教师账号', 'Teacher'),
                              ('学生账号', 'Student')]
        while True:
            for sequence, message in enumerate(manager_build_list, 1):
                print(sequence, message[0])
            corresponding_info = input_for_list(manager_build_list)
            user_info, user_name, password = register_check(corresponding_info)
            obj = eval(corresponding_info)(user_name, password)
            user_info[user_name] = obj
            with open('data/%s_info.pickle' % corresponding_info, 'wb') as dic_dump:
                pickle.dump(user_info, dic_dump)
            print('%s<%s>创建成功' % (corresponding_info, user_name))
            user_choice = input('输入B重启或输入C继续创建账号，所创建账号在下一次程序启动后生效：')
            if user_choice.upper() == 'B':
                self.exit()
            else:
                continue

    def course_build(self, *args):
        """
        创建课程
        """
        while True:
            course_name = input('课程名称：')
            if course_name in course_info.keys():
                print('课程已存在')
            else:
                break
        course_price = int(input('课程价格：'))
        start_date = input('课程开始日期（请以2020，10，20）的结构书写：')
        period = int(input('课程程度（以天为单位）：'))
        location = input('校区所在城市：')
        course_obj = School(course_name, course_price, start_date, period, location)
        course_info[course_name] = course_obj
        with open('data/course_info.pickle', 'wb') as f:
            pickle.dump(course_info, f)
        print('课程<%s>创建成功' % course_name)

    def show_student_courses(self, *args):
        """
        显示学生以及其所选课程，学费缴纳情况
        """
        for member in student_info.keys():
            print('Student: %s; 所选课程: %s; 所欠费用: %s'
                  % (member, student_info[member].course, student_info[member].tuition_remaining))

    def show_teacher_courses(self, *args):
        """
        显示教师任课课程
        """
        for member in teacher_info.keys():
            print('Teacher: %s; 所选课程: %s'% (member, teacher_info[member].course))

    def teacher_allocation(self, *args):
        """
        任课教师的调配，管理员有绝对话语权
        """
        subject = input('请输入需要调配的课程：')
        obj = input('请输入需要分配的对象：')

        try:
            if len(course_info[subject].teacher_list) > 0:
                origin_teacher = course_info[subject].teacher_list[0]  # 存储原教师姓名
                teacher_info[origin_teacher].course = []  # 清空任课教师列表

            course_info[subject].teacher_list = [obj]  # 分配导师
            teacher_info[obj].course = [subject]  # 在课程信息中加入教师名称

            with open('data/Teacher_info.pickle', 'wb') as f:
                pickle.dump(teacher_info,f)
            with open('data/course_info.pickle','wb') as f:
                pickle.dump(course_info,f)
            print('课程调配成功！')
        except KeyError:
            # 若输入内容不符合规范，报错并返回菜单
            print('输入错误')

    def exit(self, *args):
        """
        退出程序
        """
        exit()


def homepage():
    """
    首页
    """
    while True:
        print("Welcome to Roger's School".center(40, '-'))
        homepage_list = [('注册', 'student_register'), ('登陆', 'login'), ('退出', 'exit')]

        for sequence, message in enumerate(homepage_list, 1):
            print(sequence, message[0])
        eval(input_for_list(homepage_list))()  # 功能化字符串为相应函数


def student_register():
    """
    学生注册，只有学生可以通过自主注册信息，教师和管理员需要通过管理员账号进行注册
    """
    corresponding_info = 'Student'
    user_info, user_name, password = register_check(corresponding_info)
    obj = Student(user_name, password)
    user_info[user_name] = obj
    with open('data/Student_info.pickle', 'wb') as dic_dump:
        pickle.dump(user_info, dic_dump)


def login():
    """
    选择登陆类型后登陆
    """
    register_list = [('学生账号登陆', 'Student'),
                     ('教师账号登陆', 'Teacher'),
                     ('管理员账号登陆', 'Manager')]

    for sequence, message in enumerate(register_list, 1):
        print(sequence, message[0])
    corresponding_info = input_for_list(register_list)
    with open('data/%s_info.pickle' % corresponding_info, 'rb') as f:
        user_info = pickle.load(f)

    while True:
        user_name = input('请输入用户名：')
        if user_name not in user_info.keys():
            print('用户名不存在，请重新输入！')
        else:
            break

    while True:
        print('用户名:', user_name)
        password = input('请输入密码：')
        if user_info[user_name].password == password:
            obj = user_info[user_name]
            print('登陆成功！')
            operator(obj, user_info)
        else:
            print('密码错误，请重新输入！')


def operator(obj, user_info):
    """
    操作对应函数
    :param obj:
    :param user_info:
    :return:
    """
    with open('data/course_info.pickle', 'rb') as f:
        # 打开文件并放入全局变量
        global course_info
        course_info = pickle.load(f)
    with open('data/Student_info.pickle', 'rb') as f:
        # 打开文件并放入全局变量
        global student_info
        student_info = pickle.load(f)
    with open('data/Teacher_info.pickle','rb') as f:
        # 打开文件并放入全局变量
        global teacher_info
        teacher_info = pickle.load(f)
    while True:
        print(('Welcome %s!' % obj.name).center(40, '-'))  # 美观分割线
        for sequence, message in enumerate(obj.operator_list, 1):
            print(sequence, message[0])
        func_str = input_for_list(obj.operator_list)
        getattr(obj, func_str)(user_info)

if __name__ == '__main__':
    homepage()

# dic = {}
# a = Student('Jiang','qwe123')
# dic['Jiang'] = a
#
# with open('../data/Student_info.pickle', 'wb') as f:
#     pickle.dump(dic,f)
#
# dic = {}
# a = Teacher('Alex','qwe123')
# dic['Alex'] = a
#
# with open('../data/Teacher_info.pickle', 'wb') as f:
#     pickle.dump(dic,f)
#
# python = School('Python',8999,'2020,10,20',180,'北京')
# dic = {}
# dic['Python'] = python
# with open('../data/course_info.pickle', 'wb') as f:
#     pickle.dump(dic,f)