@[toc]
# 一、概述
使用==python==实现的聊天室的功能,主要功能是==群聊,私聊==两种聊天方式.实现的方式是使用==套接字编程==和==多线程treading==。

界面是用Python自带的==tkinter==模块写的，里面包含==三个界面==，分别是==登录<==，==注册==以及==聊天界面==。还有聊天界面==嵌套子窗口==，用与显示==聊天记录==。用户数据用==mysql==存储

# 二、mysql准备工作
**先在mysql中创建一个数据库，可直接使用下面的语句**
```mysql
CREATE DATABASE python_chat
```
**然后再执行下面的代码会自动创建一个表**(<font color=red size=3>注意:密码记得改</font>）
chat_create_mysql.py
```python
import pymysql
Connection = pymysql.connect(host="localhost", user="root", password="jin1687062650", db="python_chat")
cursor = Connection.cursor()
sql_create_table = '''

    create table user_information
     (
      user_name varchar (20),
      
      password varchar (20),
      
      data BLOB
    )

'''
cursor.execute(sql_create_table)
cursor.close()
```


#  三、数据库模块
**代码如下**
chat_mysql.py
```python
import pymysql
import sys
class LogInformation(object):
    @staticmethod  # 静态函数方便调用
    def login_check(user_name, password):  # 检查用户登录
        db = pymysql.connect(host="localhost", user="root", password="jin1687062650", db="python_chat")  # 关联数据库
        cursor = db.cursor()  # 取得数据库游标
        sql = "SELECT * FROM user_information where user_name = '%s' " % (user_name)  # 数据库语言，按id查找
        try:
            cursor.execute(sql)  # 游标执行数据库语言
            results = cursor.fetchone()  # 接受所有符合的对象
            db.close()  # 关闭数据库
            if password == results[1]:  # 如果密码相等则返回True
                return True
            else:
                return False
        except:
            return False

    @staticmethod  # 静态函数方便调用
    def create_new_user(user_name, password, file_name):  # 创建新用户
        db = pymysql.connect(host="localhost", user="root", password="jin1687062650", db="python_chat")  # 关联数据库
        cursor = db.cursor()  # 取得数据库游标
        fp = open(file_name, 'rb')  # 打开头像路径
        img = fp.read()  # 读取头像
        sql = "INSERT INTO user_information VALUES  (%s,%s,%s);"  # 数据库语言，插入用户数据
        args = (user_name, password, img)
        try:
            cursor.execute(sql, args)   # 游标执行数据库语言
            db.commit()  # 提交
            db.close()  # 关闭数据库连接
            print("插入成功")
            return "0"
        except:
            print("数据库出错")
            db.rollback()  # 发生错误时回滚
            db.close()  # 关闭数据库连接

    @staticmethod  # 静态函数方便调用
    def select_user_name(user_name):  # 检查用户名是否已存在
        db = pymysql.connect(host="localhost", user="root", password="jin1687062650", db="python_chat")  # 关联数据库
        cursor = db.cursor()  # 取得数据库游标
        sql = "SELECT * FROM user_information where user_name = '%s' " % (user_name)  # 数据库语言，按用户名查找
        try:
            cursor.execute(sql)  # 游标执行数据库语言
            results = cursor.fetchone()  # 接受所有符合的对象
            #  1代表已有用户， 0代表可以注册
            if results!=None:
                db.close()  # 关闭数据库
                return "1"
            else:
                db.close()  # 关闭数据库
                return "0"
        except:
            print("数据库出错")
            db.close()  # 关闭数据库

    @staticmethod # 静态函数方便调用
    def fing_face(user_name):  # 查找头像，用于聊天界面显示头像
        try:
            conn = pymysql.connect(host='localhost', user='root',
                               password='jin1687062650', db='python_chat')  # 关联数据库
            cursor = conn.cursor()  # 取得数据库游标
            sql = "SELECT * FROM user_information where user_name = '%s' " % (user_name)  # 数据库语言，按用户名查找
            cursor.execute(sql)   # 游标执行数据库语言
            fout = open('用户头像.png', 'wb')  # 打开存放用户头像的路径
            fout.write(cursor.fetchone()[2])  # 写头像数据
            fout.close()  # 关闭流
            cursor.close()  # 关闭游标
            conn.close()   # 关闭数据库
        except pymysql.Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit(1)
```
**代码解释如下**
用户登录，注册都会向服务器发送请求，服务器收到请求后，则会调用==chat_mysql==检查用户数据是不是和数据库中的是数据相同或者插入用户数据用于注册。

# 四、tkinter实现三个界面
**tkinter简介:** <font color="red" size=4>Tkinter</font>(也叫 Tk 接口)是 Tk 图形用户界面工具包标准 的 Python 接口。Tk 是一个轻量级的跨平台图形用户界面 (GUI)开发工具。 

## 登陆界面实现
**代码如下**
chat_login_panel.py
```python
from tkinter import *  # 导入模块，用户创建GUI界面

# 登陆界面类
class LoginPanel:

    # 构造方法，参数为按钮事件处理函数，从客户端main传进来，可以实现按钮回调
    def __init__(self, handle_login, handle_register, close_login_window):
        # 初始化参数实例变量
        self.handle_login = handle_login
        self.handle_register = handle_register
        self.close_login_window = close_login_window

    # 显示登录界面的实例方法
    def show_login_panel(self):
        # 声明全局变量方便，在静态函数重调用
        global login_frame
        global frames
        global imgLabel
        global numIdx

        self.login_frame = Tk()  # 创建主窗口
        # 设置背景颜色
        self.login_frame.configure(background="white")
        login_frame = self.login_frame  # 绑定全局变量

        # 设置窗口关闭按钮回调，用于退出时关闭socket连接
        self.login_frame.protocol("WM_DELETE_WINDOW", self.close_login_window)

        # 得到屏幕宽度，高度
        screen_width = self.login_frame.winfo_screenwidth()
        screen_height = self.login_frame.winfo_screenheight()
        # 声明宽度，高度变量
        width = 503
        height = 400
        # 设置窗口在屏幕局中变量
        gm_str = "%dx%d+%d+%d" % (width, height, (screen_width - width) / 2,
                                  (screen_height - 1.2 * height) / 2)
        self.login_frame.geometry(gm_str)  # 设置窗口局中
        self.login_frame.title("登录")   # 设置窗口标题
        # 设置窗口不能改变大小
        self.login_frame.resizable(width=False, height=False)

        numIdx = 10  # gif的帧数
        # 循环遍历动图的帧
        frames = [PhotoImage(file='login.gif', format='gif -index %i' % (i)) for i in range(numIdx)]
        # 创建存放gif的标签
        imgLabel = Label(self.login_frame, height=400, width=500)
        # 设置标签的位置
        imgLabel.place(x=-252, y=-200, relx=0.5, rely=0.5, relwidth=1, relheigh=0.5)

        # 设置文本标签和位置
        Label(login_frame, text="昵称：", font=("宋体", 12), bg="white", fg="grey") \
            .place(x=110, y=230)
        Label(login_frame, text="密码：", font=("宋体", 12), bg="white", fg="grey") \
            .place(x=110, y=260)

        # 声明用户名密码变量
        self.user_name = StringVar()
        self.password = StringVar()

        # 设置输入框及位置
        self.entry1=Entry(login_frame,  textvariable=self.user_name, fg="black", width=25)
        self.entry1.place(x=180, y=230)
        self.entry2=Entry(login_frame, textvariable=self.password, show='*', fg="black", width=25)
        self.entry2.place(x=180, y=260)

        # 设置注册按钮及位置，按钮事件为handle_register函数
        self.button_register = Button(login_frame, text="注册账号", relief=FLAT, bg='white', fg='grey',
                             font=('黑体', 15), command=self.handle_register).place(x=0, y=370)

        self.login_frame.bind('<Return>', self.handle_login)  # 绑定回车键
        # 设置登录按钮及位置，按钮事件为handle_login函数
        self.button_login = Button(login_frame, text="登录", bg="#00BFFF", fg="white", width=21, height=2,
                                font=('黑体', 15), command=lambda: self.handle_login(self))
        self.button_login.place(x=160, y=300)

    # 定时器函数，用于刷新gif的帧
    @staticmethod
    def update(idx):
        frame = frames[idx]
        idx += 1  # 下一张的序号
        imgLabel.configure(image=frame)
        login_frame.after(200, LoginPanel.update, idx % numIdx)  # 200毫秒之后继续执行定时器函数

    # 调用定时器函数，执行循环mainloop显示界面实例方法
    def load(self):
        LoginPanel.update(0)
        self.login_frame.mainloop()

    # 关闭登录界面实例方法
    def close_login_panel(self):
        if self.login_frame == None:
            print("未显示界面")
        else:
            # 关闭登录界面
            self.login_frame.destroy()

    # 获取输入的用户名密码实例方法
    def get_input(self):
        return self.user_name.get(), self.password.get()
```
> 
> <font color="red" size=3>注意：上面模块是给客户端调用的，单独运行没效果，后面会介绍启动方法。下面给出客户端调用登录模块显示的效果

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210422221038193.gif#pic_center)

**代码解释如下**
创建一个登陆界面模块==chat_login_panel==，里面包含一个登陆界面类==LoginPanel==，类的构造方法==init==是初始化从客户端传进来的函数，用与处理按钮事件，当用户点击按钮时便会回调给客户端处理的。

实例方法==show_login_panel==是把组件封装起来，这样用户就可以创建多个登陆界面且互不干扰，实现多人登陆，每一个实例对象都是不相同的。

实例方法==close_login_panel，get_input==分别是关闭登陆界面，获取用户输入的用户名和密码。

静态函数==update==是定时器，用于刷新gif动图。

实例方法==load==的作用是调用定时器函数==updata==和执行循环函数==login_frame.mainloop==显示在==login_show_panel==创建的界面==login_frame==

**客户端调用过程:** 当用户执行main模块时便会创建==LoginPanel==对象，创建对象过程会调用==init==构造方法把mian模块中的函数作为参数进行初始化变为实例变量，作为按钮的事件处理。创建完对象后就可以用对象调用对象的实例方法了。

首先调用<==ogin_show_panel==实例方法创建组件以及布局，然后调用==load==执行定时器函数刷新动图和==mainloop==循环函数显示界面。
> 客户端main模块后面会给出，注册界面和聊天界面跟登陆界面是一样的

## 注册界面实现
**代码如下**

chat_login_panel.py
```python
from tkinter import *  # 导入模块，用户创建GUI界面
from PIL import Image  # 导入处理图像模块

# 注册界面类
class RegisterPanel(object):

    # 构造方法，参数为按钮事件处理函数，从客户端main传进来，可以实现按钮回调
    def __init__(self, file_open_face, close_register_window, register_submit):
        # 初始化参数实例变量
        self.file_open_face = file_open_face
        self.close_register_window = close_register_window
        self.register_submit = register_submit
        self.file_name = ""  # 文件路径

    # 显示注册界面的实例方法
    def show_register_panel(self):
        # 声明全局变量方便，在静态函数重调用
        global register_frame
        global frames
        global imgLabel
        global numIdx

        # 创建主窗口
        self.register_frame = Tk()
        register_frame = self.register_frame  # 绑定全局变量
        # 设置背景颜色
        self.register_frame.configure(background="white")
        # 得到屏幕宽度，高度
        screen_width = self.register_frame.winfo_screenwidth()
        screen_height = self.register_frame.winfo_screenheight()
        # 声明宽度，高度变量
        width = 503
        height = 400
        # 设置窗口在屏幕局中变量
        gm_str = "%dx%d+%d+%d" % (width, height, (screen_width - width) / 2,
                                  (screen_height - 1.2 * height) / 2)
        # 设置窗口局中
        self.register_frame.geometry(gm_str)
        # 设置窗口标题
        self.register_frame.title("注册")
        # 设置窗口不能改变大小
        self.register_frame.resizable(width=False, height=False)

        self.p1 = PhotoImage(file='添加头像按钮.png')  # 把图片转化为PhotoImage类型

        numIdx = 9  # gif的帧数
        # 循环遍历动图的帧
        frames = [PhotoImage(file='register.gif', format='gif -index %i' % (i)) for i in range(numIdx)]
        # 创建存放gif的标签
        imgLabel = Label(self.register_frame, height=400, width=500)
        # 设置标签的位置
        imgLabel.place(x=-252, y=-200, relx=0.5, rely=0.5, relwidth=1, relheigh=0.5)

        # 设置文本框，用户存放头像
        self.face_show = Text(self.register_frame, bg="white", height=3.5, width=7,
                                 highlightcolor="white")
        # 设置文本框不可编辑
        self.face_show.config(state=DISABLED)
        # 设置文本框的位置
        self.face_show.place(x=370, y=230)

        # 声明宽度高度，用来设置图片大小
        self.width = 50
        self.height = 50
        # 打开图片，用在注册页面文本框中显示默认头像
        img = Image.open("默认头像.png")
        # 设置图片的大小
        out = img.resize((self.width, self.height), Image.ANTIALIAS)
        # 保存图片，类型为png
        out.save(r"头像.png", 'png')

        # 把头像转换为PhotoImage类型，用于在文本框显示
        self.p2 = PhotoImage(file='头像.png')
        # 设置文本框可编辑
        self.face_show.config(state=NORMAL)
        # 把头像图片插入文本框
        self.face_show.image_create(END, image=self.p2)
        # 设置文本框不可编辑
        self.face_show.config(state=DISABLED)
        # 设置文本框滑到最低
        self.face_show.see(END)

        # 设置文本标签及位置
        Label(self.register_frame, text="用户名：", font=("宋体", 12), bg="white", fg="grey") \
            .place(x=60, y=230)
        Label(self.register_frame, text="密  码：", font=("宋体", 12), bg="white", fg="grey") \
            .place(x=60, y=260)
        Label(self.register_frame, text="确认密码：", font=("宋体", 12), bg="white", fg="grey") \
            .place(x=60, y=290)

        # 声明用户名，密码，确认密码变量
        self.user_name = StringVar()
        self.password = StringVar()
        self.confirm_password = StringVar()

        # 设置输入文本框和位置，用于获取用户的输入
        Entry(self.register_frame, textvariable=self.user_name, fg="black", width=30) \
            .place(x=140, y=230)
        Entry(self.register_frame, textvariable=self.password, show="*", fg="black", width=30) \
            .place(x=140, y=260)
        Entry(self.register_frame, textvariable=self.confirm_password, show="*", fg="black", width=30) \
            .place(x=140, y=290)

        # 设置退出注册页面按钮及位置，按钮事件为close_register_window函数
        self.botton_quit = Button(self.register_frame, text="返回",  relief=FLAT, bg='white', fg="grey",
                               font=('黑体', 15), command=self.close_register_window).place(x=0, y=370)

        self.register_frame.bind('<Return>', self.register_submit)  # 绑定注册按钮回车事件
        # 设置注册按钮及位置，按钮事件为register.submit函数
        self.botton_register = Button(self.register_frame, text="立即注册", bg="#00BFFF", fg="white", width=27, height=2,
                              font=('黑体', 15), command=lambda: self.register_submit(self)).place(x=120, y=330)

        # 设置添加头像按钮及位置，事件处理为为file_open_face函数
        self.botton_file_open = Button(self.register_frame, image=self.p1, relief=FLAT, bd=0,
                                       command=self.file_open_face).place(x=430, y=230)

    # 定时器静态函数，用于刷新gif的帧
    @staticmethod
    def update(idx):
        frame = frames[idx]
        idx += 1  # 下一张的序号
        imgLabel.configure(image=frame)
        register_frame.after(200, RegisterPanel.update, idx % numIdx)  # 200毫秒之后继续执行定时器函数

    # 调用定时器函数，执行循环mainloop显示界面实例方法
    def load(self):
        RegisterPanel.update(0)
        self.register_frame.mainloop()

    # 添加头像实例方法
    def add_face(self, file_name):
        self.file_name = file_name
        # 打开图片
        img = Image.open(file_name)
        # 设置图片大小
        out = img.resize((self.width, self.height), Image.ANTIALIAS)
        # 保存图片，类型为png
        out.save(r"头像.png", 'png')
        # 把头像转化为PhotoImage
        self.p = PhotoImage(file='头像.png')
        # 设置文本框可编辑
        self.face_show.config(state=NORMAL)
        self.face_show.delete('0.0', END)
        # 把头像插入文本框
        self.face_show.image_create(END, image=self.p)
        # 设置文本不可编辑
        self.face_show.config(state=DISABLED)
        # 设置文本框滑到最低
        self.face_show.see(END)

    # 关闭注册界面实例方法
    def close_register_panel(self):
        if self.register_frame == None:
            print("未显示界面")
        else:
            # 关闭注册界面
            self.register_frame.destroy()

    # 获取输入的用户名、密码、确认密码实例方法
    def get_input(self):
        return self.user_name.get(), self.password.get(), self.confirm_password.get(), self.file_name
```
 
 **效果图**

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210422213231111.gif)
## 聊天界面实现
**代码如下**

chat_main_panel.py
```python
from tkinter import *  # 导入模块，用户创建GUI界面
import tkinter.font as tf  # 处理字体样式和颜色的类
import time
import chat_mysql  # 导入处理mysql的模块
from PIL import Image  # 导入处理图像模块

# 主界面类
class MainPanel:
    # 构造方法，参数为按钮事件处理函数，从客户端main传进来，可以实现按钮回调
    def __init__(self, user_name, send_message, send_mark, refurbish_user, private_talk, close_main_window):
        # 初始化参数实例变量
        self.user_name = user_name
        self.send_message = send_message
        self.send_mark = send_mark
        self.refurbish_user = refurbish_user
        self.private_talk = private_talk
        self.close_main_window = close_main_window
        # 用字典将标记与表情图片一一对应, 用于后面接收标记判断表情贴图
        self.dic = {}
        self.ee = 0  # 判断表情面板开关的标志
        self.face = []  # 存储头像列表

    def show_main_panel(self):
        # 声明全局变量，方便在静态函数中调用用
        global main_frame
        global frames
        global imgLabel
        global numIdx

        # 创建主窗口
        main_frame = Tk()
        # 把全局变量绑定在实例变量上
        self.main_frame = main_frame
        # 设置主窗口标题
        self.main_frame.title("python聊天室")
        # 设置主窗口颜色
        self.main_frame.configure(background="white")
        # 设置关闭主窗口的回调函数
        self.main_frame.protocol("WM_DELETE_WINDOW", self.close_main_window)
        # 声明宽度，高度变量用于设置主窗口局中
        width = 1300
        height = 700
        # 获取屏幕的高度，宽度
        screen_width = self.main_frame.winfo_screenwidth()
        screen_height = self.main_frame.winfo_screenheight()
        # 设置主窗口局中的变量
        gm_str = "%dx%d+%d+%d" % (width, height, (screen_width - width) / 2,
                                  (screen_height - 1.2 * height) / 2)
        # 设置主窗口局中
        self.main_frame.geometry(gm_str)
        # 设置窗口不能改变大小
        self.main_frame.resizable(width=False, height=False)

        # 表情图片,把图片转换为PhotoImage,
        self.p1 = PhotoImage(file='微信表情1.png')
        self.p2 = PhotoImage(file='微信表情2.png')
        self.p3 = PhotoImage(file='微信表情3.png')
        self.p4 = PhotoImage(file='微信表情4.png')
        self.p5 = PhotoImage(file='微信表情5.png')
        self.p6 = PhotoImage(file='微信表情6.png')
        self.p7 = PhotoImage(file='微信表情7.png')
        self.p8 = PhotoImage(file='微信表情8.png')
        self.p9 = PhotoImage(file='微信表情9.png')
        self.p10 = PhotoImage(file='微信表情10.png')

        # 按钮图片，把图片转换为PhotoImage
        self.p11 = PhotoImage(file='表情按钮.png')
        self.p12 = PhotoImage(file='聊天记录按钮.png')

        # 表情包字典，每一个表情包对应一个标记
        self.dic = {'aa**': self.p1, 'bb**': self.p2, 'cc**': self.p3, 'dd**': self.p4, 'ee**': self.p5,
                    'ff**': self.p6, 'gg**': self.p7, 'hh**': self.p8, 'jj**': self.p9, 'kk**': self.p10}

        # 设置文本标签和位置
        self.label1 = Label(self.main_frame, text="    在线用户         python聊天室欢迎您：" + self.user_name + "   "
                                                                                                      "              "
                                                                                                      "      " +
                                                  "                           ", font=("黑体", 20), bg="#00BFFF", fg="white")
        self.label1.grid(row=0, column=0, ipady=0, padx=0, columnspan=3, sticky=E+W)

        # 在线用户列表框
        friend_list_var = StringVar()  # 声明列表框变量
        # 设置列表框及位置
        self.friend_list = Listbox(self.main_frame, selectmode=NO, listvariable=friend_list_var,
                                   bg="#F8F8FF", fg="#00BFFF", font=("宋体", 14),
                                   highlightcolor="white", selectbackground="#00BFFF")
        self.friend_list.grid(row=1, column=0, rowspan=3, sticky=N + S, padx=0, pady=(0, 0))
        self.friend_list.bind('<ButtonRelease-1>', self.private_talk)  # 绑定列表框点击事件
        # 设置列表框的缩放比例
        main_frame.rowconfigure(1, weight=1)  # 设置主窗口第一行的缩放比例，也就是列表框
        main_frame.columnconfigure(1, weight=1)  # 设置列的缩放比例

        sc_bar = Scrollbar(self.main_frame, activebackground='red')  # 设置列表框滚动条
        sc_bar.grid(row=1, column=0, sticky=N + S + E, rowspan=3, pady=(0, 3))  # 设置滚动条的位置

        # 列表框和滚动条的绑定
        sc_bar['command'] = self.friend_list.yview
        self.friend_list['yscrollcommand'] = sc_bar.set

        # 设置消息框的滚动条
        msg_sc_bar = Scrollbar(self.main_frame)  # 设置滚动条
        msg_sc_bar.grid(row=1, column=1, sticky=E + N + S, padx=(0, 1), pady=1)  # 设置滚动条的位置

        # 显示消息的文本框
        self.message_text = Text(self.main_frame, bg="white", height=1,
                            highlightcolor="white", highlightthickness=1)
        # 显示消息的文本框不可编辑，当需要修改内容时再修改版为可以编辑模式 NORMAL
        self.message_text.config(state=DISABLED)
        # 设置消息框的位置
        self.message_text.grid(row=1, column=1, sticky=W + E + N + S, padx=(0, 15), pady=(0, 27))

        numIdx = 6  # gif的帧数
        # 循环遍历动图的帧
        frames = [PhotoImage(file='main.gif', format='gif -index %i' % (i)) for i in range(numIdx)]
        # 创建存储gif的标签
        imgLabel = Label(self.main_frame, height=400, width=490)
        # 设置标签的位置
        imgLabel.grid(row=1, column=2, sticky=W + E + N + S, rowspan=100, padx=(0, 0), pady=(160, 175))

        # 绑定消息框和消息框滚动条
        msg_sc_bar["command"] = self.message_text.yview
        self.message_text["yscrollcommand"] = msg_sc_bar.set

        # 设置发送消息框滚动条
        send_sc_bar = Scrollbar(self.main_frame)  # 创建滚动条
        # 设置滚动条的位置
        send_sc_bar.grid(row=2, column=1, sticky=E + N + S, padx=(0, 1), pady=1)

        # 发送消息框
        self.send_text = Text(self.main_frame, bg="white", height=11, highlightcolor="white",
                         highlightbackground="#444444", highlightthickness=0)
        # 滚动到底部
        self.send_text.see(END)
        # 设置消息框的位置
        self.send_text.grid(row=2, column=1, sticky=W + E + N + S, padx=(0, 15), pady=0)

        # 绑定发送消息框和发送消息框滚动条
        send_sc_bar["command"] = self.send_text.yview
        self.send_text["yscrollcommand"] = send_sc_bar.set

        self.main_frame.bind('<Return>', self.send_message)  # 绑定发送按钮回车事件

        # 设置发送消息按钮及位置，事件处理函数为send_message
        button1 = Button(self.main_frame, command=lambda: self.send_message(self), text="发送", bg="#00BFFF",
                         fg="white", width=13, height=2, font=('黑体', 12),)
        button1.place(x=650, y=640)

        # 设置关闭窗口按钮及位置，事件处理函数为close_main_window
        button2 = Button(self.main_frame, text="关闭", bg="white", fg="black", width=13, height=2,
                              font=('黑体', 12), command=self.close_main_window)
        button2.place(x=530, y=640)

        # 设置表情包按钮及位置，事件处理为实例方法express
        botton4 = Button(self.main_frame, command=self.express, image=self.p11, relief=FLAT, bd=0)
        botton4.place(x=214, y=525)

        # 设置聊天记录按钮及位置，事件处理为create_window实例方法
        botton5 = Button(self.main_frame, command=self.create_window, image=self.p12, relief=FLAT, bd=0)
        botton5.place(x=250, y=525)

        # 设置刷新用户列表按钮及位置，事件处理为refurbish_user函数
        botton5 = Button(self.main_frame, command=self.refurbish_user, text="刷新在线用户", bg="#00BFFF", fg="white",
                         width=13, height=2, font=('黑体', 12),)
        botton5.place(x=40, y=650)

    # 定义器静态函数，用于刷新gif的帧
    @staticmethod
    def update(idx):
        frame = frames[idx]
        idx += 1  # 下一张的序号
        imgLabel.configure(image=frame)
        main_frame.after(100, MainPanel.update, idx % numIdx)  # 100毫秒之后继续执行定时器函数

    # 调用定时器函数，执行循环mainloop显示界面实例方法
    def load(self):
        MainPanel.update(0)
        self.main_frame.mainloop()

    # 聊天记录按钮处理事件实例方法
    def create_window(self):
        top1 = Toplevel()  # 创建子窗口
        top1.configure(background="#FFFAFA")  # 设置子窗口颜色
        # 得到屏幕宽度，高度
        screen_width = top1.winfo_screenwidth()
        screen_height = top1.winfo_screenheight()
        # 声明宽度，高度变量
        width = 600
        height = 650
        # 设置窗口在屏幕局中变量
        gm_str = "%dx%d+%d+%d" % (width, height, (screen_width - width) / 2,
                                  (screen_height - 1.2 * height) / 2)
        top1.geometry(gm_str)  # 设置窗口局中
        top1.title("聊天记录")  # 设置窗口标题
        # 设置窗口不能改变大小
        top1.resizable(width=False, height=False)

        # 设置文本标签
        title_lable = Label(top1, text="聊天记录", font=('粗斜体', 20, 'bold italic'),
                            fg="white", bg="#00BFFF")
        # 设置文本在窗口的位置
        title_lable.pack(ipady=10, fill=X)

        # 设置文本框，用户存放聊天记录信息
        self.chatting_records = Text(top1, bg="white", height=50, highlightcolor="white", highlightthickness=1)
        # 设置位置
        self.chatting_records.pack(ipady=10, fill=X)
        # 显示消息的文本框不可编辑，当需要修改内容时再修改版为可以编辑模式 NORMAL
        self.chatting_records.config(state=DISABLED)

        # 设置清除聊天记录按钮及位置，事件处理函数为clear_chatting_records实例方法
        botton = Button(top1,  text="清空聊天记录", command=self.clear_chatting_records, bg="#00BFFF",
                        fg="white", width=12, height=2, font=('黑体', 11))
        botton.place(x=490, y=600)

        # 调用实例方法显示聊天记录
        self.show_chatting_records()

    # 显示聊天记录的实例方法
    def show_chatting_records(self):
        # 设置文本框可编辑
        self.chatting_records.config(state=NORMAL)
        # 打开用户的存放聊天记录的本地文件
        f = open("C:/Program Files (x86)/pythonProject/chatting_records/" + self.user_name + ".txt", 'r')
        while True:
            content = f.readline()  # 每次读取一行
            ft = tf.Font(family='微软雅黑', size=13)  # 设置字体样式和大小变量
            # 设置颜色和字体样式及大小
            self.chatting_records.tag_config("tag_9", foreground="#00BFFF", font=ft)
            if content != "":  # 如果不为空则在文本框最后一行插入文本
                self.chatting_records.insert(END, content, 'tag_9')
            else:
                self.chatting_records.config(state=DISABLED)  #否则则设置文本框不可编辑
                return

    # 清除聊天记录按钮处理实例方法
    def clear_chatting_records(self):
        # 设置文本框可编辑
        self.chatting_records.config(state=NORMAL)
        self.chatting_records.delete('1.0', END)   # 删除文本框内容
        # 打开聊天记录文件，以覆盖的形式写入内容
        a = open("C:C:/Program Files (x86)/pythonProject/chatting_records/" + self.user_name + ".txt",
                 'w')
        a.write("")  # 插入空字符串，则聊天记录会被覆盖
        a.close()  # 关闭
        self.chatting_records.config(state=DISABLED)  # 设置文本不可编辑

    # 保存聊天记录实例方法
    def sava_chatting_records(self, content):
        # 打开聊天记录文件
        a = open("C:/Program Files (x86)/pythonProject/chatting_records/" + self.user_name + ".txt", 'a')
        a.write(content)   # 写入信息
        a.close()  # 关闭

    # 定义表情包按钮处理事件实例方法
    def express(self):
        # 如果ee标记为0，则弹出表情包，否则销毁表情包
        if self.ee == 0:
            self.ee = 1   # 把标记置为1，用于下次点击按钮时销毁表情
            # 设置表情图按钮及相应的事件处理实例方法
            self.b1 = Button(self.main_frame, command=self.bb1, image=self.p1, relief=FLAT, bd=0)
            self.b2 = Button(self.main_frame, command=self.bb2, image=self.p2, relief=FLAT, bd=0)
            self.b3 = Button(self.main_frame, command=self.bb3, image=self.p3, relief=FLAT, bd=0)
            self.b4 = Button(self.main_frame, command=self.bb4, image=self.p4, relief=FLAT, bd=0)
            self.b5 = Button(self.main_frame, command=self.bb5, image=self.p5, relief=FLAT, bd=0)
            self.b6 = Button(self.main_frame, command=self.bb6, image=self.p6, relief=FLAT, bd=0)
            self.b7 = Button(self.main_frame, command=self.bb7, image=self.p7, relief=FLAT, bd=0)
            self.b8 = Button(self.main_frame, command=self.bb8, image=self.p8, relief=FLAT, bd=0)
            self.b9 = Button(self.main_frame, command=self.bb9, image=self.p9, relief=FLAT, bd=0)
            self.b10 = Button(self.main_frame, command=self.bb10, image=self.p10, relief=FLAT, bd=0)
            # 设置表情包的位置
            self.b1.place(x=207, y=480)
            self.b2.place(x=255, y=480)
            self.b3.place(x=303, y=480)
            self.b4.place(x=351, y=480)
            self.b5.place(x=399, y=480)
            self.b6.place(x=207, y=430)
            self.b7.place(x=255, y=430)
            self.b8.place(x=303, y=430)
            self.b9.place(x=351, y=430)
            self.b10.place(x=399, y=430)
        else:
            # 标记ee为0则销毁所有表情按钮
            self.ee = 0
            self.b1.destroy()
            self.b2.destroy()
            self.b3.destroy()
            self.b4.destroy()
            self.b5.destroy()
            self.b6.destroy()
            self.b7.destroy()
            self.b8.destroy()
            self.b9.destroy()
            self.b10.destroy()

    # 所有表情按钮处理实例方法
    def bb1(self):
        self.mark('aa**')  # 调用实例方法，把参数传过去

    def bb2(self):
        self.mark('bb**')

    def bb3(self):
        self.mark('cc**')

    def bb4(self):
        self.mark('dd**')

    def bb5(self):
        self.mark('ee**')

    def bb6(self):
        self.mark('ff**')

    def bb7(self):
        self.mark('gg**')

    def bb8(self):
        self.mark('hh**')

    def bb9(self):
        self.mark('jj**')

    def bb10(self):
        self.mark('kk**')

    # 处理发送表情的实例方法
    def mark(self, exp):  # 参数是发的表情图标记, 发送后将按钮销毁
        self.send_mark(exp)  # 函数回调把标记作为参数
        # 发送完摧毁所有表情包
        self.b1.destroy()
        self.b2.destroy()
        self.b3.destroy()
        self.b4.destroy()
        self.b5.destroy()
        self.b6.destroy()
        self.b7.destroy()
        self.b8.destroy()
        self.b9.destroy()
        self.b10.destroy()
        self.ee = 0  # 把标记置为0

    # 刷新在线列表实例方法
    def refresh_friends(self, online_number, names):
        self.friend_list.delete(0, END)   # 先删除在线列表
        for name in names:  # 循环插入在线用户
            self.friend_list.insert(0, name)
        self.friend_list.insert(0, "【群聊】")  # 在第二行插入群聊
        self.friend_list.itemconfig(0, fg="#00BFFF")  # 设置群聊字体颜色
        self.friend_list.insert(0, '在线用户数: ' + str(online_number))  # 在第一行插入在线用户数
        self.friend_list.itemconfig(0, fg="#FF00FF")  # 设置在线用户数颜色

    # 在界面显示消息的实例方法
    # 接受到消息，在文本框中显示，自己的消息用蓝色，别人的消息用绿色
    def show_send_message(self, user_name, content, chat_flag):
        self.message_text.config(state=NORMAL)   # 设置消息框可编辑
        # 设置发送的消息的用户名和时间变量
        title = user_name + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n"
        if content == '* 系统提示: ' + user_name + ' 加入聊天室':  # 加入聊天室标记处理
            ft = tf.Font(family='微软雅黑', size=13)  # 设置字体样式和大小变量
            # 设置字体颜色样式及大小
            self.message_text.tag_config("tag_1", foreground="#FF00FF", font=ft)
            self.message_text.insert(END, content + "\n", 'tag_1')  # 在最后一行插入消息
            self.message_text.config(state=DISABLED)  # 设置不可编辑
        elif content == '* 系统提示: ' + user_name + ' 已离开群聊':  # 离开聊天室标记处理
            ft = tf.Font(family='微软雅黑', size=13)
            self.message_text.tag_config("tag_2", foreground="#DC143C", font=ft)
            self.message_text.insert(END, content + "\n", 'tag_2')
            self.message_text.config(state=DISABLED)
        elif user_name == self.user_name:  # 如果发送消息的用户是自己
            if chat_flag == "group_chat":  # 如果标记是群聊标记，则自己的消息用蓝色
                ft = tf.Font(family='微软雅黑', size=13)
                self.message_text.tag_config("tag_4", foreground="#00BFFF", font=ft)
                self.message_text.insert(END, title, 'tag_4')
                self.sava_chatting_records(title)   # 调用实例方法保存聊天记录
            elif chat_flag == "private_chat":  # 如果是标记是私聊，则消息用红色
                ft = tf.Font(family='微软雅黑', size=13)
                self.message_text.tag_config("tag_5", foreground="#DC143C", font=ft)
                self.message_text.insert(END, title, 'tag_5')
                self.sava_chatting_records(title)
        else:  #  如果发送消息的用户不是自己
            if chat_flag == "group_chat":  # 如果标记是群聊，则消息用绿色
                ft = tf.Font(family='微软雅黑', size=13)
                self.message_text.tag_config("tag_6", foreground="#008000", font=ft)
                self.message_text.insert(END, title, 'tag_6')
                self.sava_chatting_records(title)
            elif chat_flag == "private_chat":  # 标记是私聊，则消息用红色
                ft = tf.Font(family='微软雅黑', size=13)
                self.message_text.tag_config("tag_7", foreground="#DC143C", font=ft)
                self.message_text.insert(END, title, 'tag_7')
                self.sava_chatting_records(title)
        if content in self.dic:  # 判断消息是否为表情标记
            chat_mysql.LogInformation.fing_face(user_name)  # 去数据库中读取用户的头像
            time.sleep(0.5)   # 设置时间缓冲，给数据库读取用户头像以及保存到本地文件的时间缓冲
            # 打开图片
            self.img1 = Image.open("用户头像.png")  # 打开数据库保存的本地文件
            # 设置图片大小
            self.out1 = self.img1.resize((50, 50), Image.ANTIALIAS)
            # 保存图片，类型为png
            self.out1.save(r"用户头像1.png", 'png')
            time.sleep(0.5)  # 给修改图片大小以及保存修改后的图片留时间缓存
            # 把头像转化为PhotoImage
            self.face.append(PhotoImage(file='用户头像1.png'))  # 把头像图片加入到列表中
            self.message_text.image_create(END, image=self.face[-1])  # 插入列表最后一个头像
            self.message_text.insert(END, " : ")
            self.message_text.image_create(END, image=self.dic[content])   # 插入表情
            self.message_text.insert(END, "\n")
            self.message_text.config(state=DISABLED)
            # 滚动到最底部
            self.message_text.see(END)
        # 内容是消息的处理
        elif content != '* 系统提示: ' + user_name + ' 加入聊天室' and content != '* 系统提示: ' + user_name + ' 已离开群聊':
            chat_mysql.LogInformation.fing_face(user_name)
            time.sleep(0.5)
            # 打开图片
            self.img2 = Image.open("用户头像.png")
            # 设置图片大小
            self.out2 = self.img2.resize((50, 50), Image.ANTIALIAS)
            # 保存图片，类型为png
            self.out2.save(r"用户头像2.png", 'png')
            time.sleep(0.5)
            self.face.append(PhotoImage(file='用户头像2.png'))
            self.message_text.image_create(END, image=self.face[-1])
            self.message_text.insert(END, " : ")
            ft = tf.Font(family='微软雅黑', size=15)
            self.message_text.tag_config("tag_8", foreground="#000000", font=ft)
            self.message_text.insert(END, content, 'tag_8')  # 插入消息
            self.message_text.config(state=DISABLED)
            # 滚动到最底部
            self.message_text.see(END)
            # 保存聊天记录
            self.sava_chatting_records(content)
            self.sava_chatting_records("------------------------------------------------------------------------------\n")

    # 群聊私聊改变标签的实例方法
    def change_title(self, title):
        self.label1['text'] = title

    # 清空发送消息输入框的实例方法
    def clear_send_text(self):
        self.send_text.delete('0.0', END)

    # 获取消息输入框内容的实例方法
    def get_send_text(self):
        return self.send_text.get('0.0', END)
```

**效果图**
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210422215843746.gif)
> 至此所有界面都实现了，这些界面被封装成类，划分成单独的模块，单独运行是没效果的，需要通过main模块也就是客户端来调用，然后通过用户的操作进行调用相应的对象实例方法

# 五、服务端实现
> 先讲一下模块的启动过程，在上面给出三个界面模块，这些都不需要运行的，运行的模块只有两个，分别是服务端和客户端，服务端要先运行，然后再运行客户端。
> 
**服务端的执行过程:** 当运行服务端模块时,会创建一个==socket==，然后绑定==本机ip地址==及==端口==进行监听客户端的请求连接，每接受一个socket的请求,就开启一个新的线程来接受请求消息的处理
**代码如下**
chat_server.py
```python
import socket  # 导入套接字socket模块
from threading import Thread  # 导入多线程模块
import math
import chat_mysql  # 导入自定义模块用于在mysql中处理用户数据

# 维护一个在线用户的连接列表，用于群发消息
online_connection = list()
# 存储socket连接和用户的对应关系
connection_user = dict()
join_user = ""   # 存储加入系统聊天室的用户
flag = 0  # 发送用户加入聊天室系统提示标记
chat_user = ""  # 存储聊天对象标记

# 发送带长度的字符串的函数
def send_string_with_length(_conn, content):
    # 先发送内容的长度
    _conn.sendall(bytes(content, encoding='utf-8').__len__().to_bytes(4, byteorder='big'))
    # 再发送内容
    _conn.sendall(bytes(content, encoding='utf-8'))

# 发送在线用户数的函数
def send_number(_conn, number):
    _conn.sendall(int(number).to_bytes(4, byteorder='big'))

# 获取变长字符串的函数
def recv_all_string(connection):
    # 获取消息长度
    length = int.from_bytes(connection.recv(4), byteorder='big')
    b_size = 3 * 1024  # 注意utf8编码中汉字占3字节，英文占1字节
    times = math.ceil(length / b_size)
    content = ''
    for i in range(times):
        if i == times - 1:
            seg_b = connection.recv(length % b_size)
        else:
            seg_b = connection.recv(b_size)
        content += str(seg_b, encoding='utf-8')
    return content

# 检查用户名密码是否正确函数
def check_user(user_name, password):
    # 调用数据库模块检查用户名和密码
    return chat_mysql.LogInformation.login_check(user_name, password)

# 添加用户函数
def add_user(user_name, password, file_name):
    # 调用数据库模块中的函数添加用户，成功返回1，已有用户返回0，其他错误返回2
    if chat_mysql.LogInformation.select_user_name(user_name) == "1":
        return "1"
    elif chat_mysql.LogInformation.create_new_user(user_name, password, file_name) == "0":
        return "0"
    else:
        return "2"

# 处理刷新列表的请求函数
def handle_online_list():
    for con in online_connection:  # 给所有在线用户发送消息
        send_string_with_length(con, "#!onlinelist#!")  # 发送刷新用户列表标记
        # 先发送列表人数
        send_number(con, online_connection.__len__())
        for c in online_connection:  # 发送用户名
            send_string_with_length(con, connection_user[c])
    return True

# 处理登录请求函数
def handle_login(connection, address):
    # 声明全局变量，方便可以在其他函数中使用
    global join_user  # 声明存储加入聊天室的用户
    global flag  # 声明用户加入聊天室的标记
    # 调用函数接受客户端发的用户名和密码
    user_name = recv_all_string(connection)
    password = recv_all_string(connection)
    # 调用函数检查用户名和密码
    check_result = check_user(user_name, password)
    # 如果检查结果为True,向客户端发送登录成标记
    if check_result:
        connection.sendall(bytes("1", "utf-8"))  # 向客户端发送登录通过标记
        connection_user[connection] = user_name  # 把用户和连接号加入字典，连接作为键，名作为值
        join_user = user_name   # 存储加入系统聊天室的用户
        flag = 1  # 设置标记为真，用与向所有客户端发送用户加入聊天的信息
        online_connection.append(connection)  # 把当前连接的用户添加到在线用户的连接列表，用于群发消息
        handle_online_list()  # 调用刷新在线用户列表的函数
        handle_message(connection, address)   # 调用发送用户加入聊天室的信息的函数
    else:
        connection.sendall(bytes("0", "utf-8"))  # 向客户端发送登录失败标记
    return True

# 处理注册请求函数
def handle_register(connection, address):
    # 调用函数依次获取用户名和密码
    user_name = recv_all_string(connection)
    password = recv_all_string(connection)
    file_name = recv_all_string(connection)
    # 调用添加用户函数add_user返回值作为发送给客户端的标记，0成功，1已有用户，2其他错误
    connection.sendall(bytes(add_user(user_name, password, file_name), "utf-8"))
    return True

# 处理消息发送请求函数
def handle_message(connection, address):
    global flag  # 发送用户加入聊天室的标记
    global chat_user  # 聊天对象
    if flag == 1:   # 如果等于1发送加入聊天信息给所有客户端
        for c in online_connection:
            send_string_with_length(c, "#!message#!")  # 发送消息标记
            send_string_with_length(c, "group_chat")   # 发送聊天对象标记，对象为群聊
            send_string_with_length(c, connection_user[connection])  # 发送加入聊天室的用户名
            content = '* 系统提示: ' + connection_user[connection] + ' 加入聊天室'
            send_string_with_length(c, content)  # 发送加入聊天室的信息
    else:  # 否则调用函数获取聊天对象，内容
        chat_user = recv_all_string(connection)
        content = recv_all_string(connection)
        if content == "exit":  # 如果内容是exit标记，则是有用户退出聊天室
            for c in online_connection:  # 给所有在线用户发送用户退出聊天室信息
                send_string_with_length(c, "#!message#!")  # 发送消息标记
                send_string_with_length(c, "group_chat")   # 发送聊天对象标记，对象为群聊
                send_string_with_length(c, connection_user[connection])  # 发送离开聊天室的用户名
                send_string_with_length(c, '* 系统提示: ' + connection_user[connection] + ' 已离开群聊')   # 发送离开聊天室的信息
        else:  # 否则查看聊天对象
             if chat_user == "【群聊】":  # 如果聊天对象室群聊
                # 发送给所有在线客户端
                for c in online_connection:
                    # 先发一个字符串告诉客户端接下来是消息
                    send_string_with_length(c, "#!message#!")  # 发送消息标记
                    send_string_with_length(c, "group_chat")  # 发送聊天对象标记，对象为群聊
                    send_string_with_length(c, connection_user[connection])   # 发送给客户端谁发送消息的用户名
                    send_string_with_length(c, content)  # 发送消息
             else:  # 否则聊天对象是一对一私聊
                 for c in online_connection:  # 寻找聊天对象
                     if connection_user[c] == chat_user:  # 从字典中查找对象，查到则执行下面语句
                         send_string_with_length(c, "#!message#!")  # 发送消息标记
                         send_string_with_length(c, "private_chat")  # 发送聊天对象标记，为私聊
                         send_string_with_length(c, connection_user[connection])  # 发送给客户端谁发送消息的用户名
                         send_string_with_length(c, content)  # 发送消息
                         # 给自己发送消息
                         send_string_with_length(connection, "#!message#!")
                         send_string_with_length(connection, "private_chat")
                         send_string_with_length(connection, connection_user[connection])
                         send_string_with_length(connection, content)
    flag = 0  # 把加入聊天标记改为0
    return True

# 处理请求线程的执行函数
def handle(connection, address):
    try:
        while True:
            # 接受客户端发送的请求类型
            request_type = str(connection.recv(1024).decode())
            # 是否继续处理标记
            no_go = True
            if request_type == "1":  # 登录请求
                print("开始处理登录请求")
                # 调用函数处理请求
                no_go = handle_login(connection, address)
            elif request_type == "2":  # 注册请求
                print("开始处理注册请求")
                no_go = handle_register(connection, address)
            elif request_type == "3":  # 发送消息请求
                print("开始处理发送消息请求")
                no_go = handle_message(connection, address)
            elif request_type == "4":  # 刷新用户列表请求
                print("开始处理刷新列表请求")
                no_go = handle_online_list()
            if not no_go:
                break
    except Exception as e:
        print(str(address) + " 连接异常，准备断开: " + str(e))
    finally:
        try:
            connection.close()
            online_connection.remove(connection)
            connection.pop(connection)
        except:
            print(str(address) + "连接关闭异常")

# 入口
if __name__ == "__main__":
    try:
        # 创建接受客户端连接的socket
        server = socket.socket()
        server.bind(('127.0.0.1', 5000))  # 绑定主机及端口号
        # 最大挂起数
        server.listen(10)
        print("服务器启动成功，开始监听...")
        while True:
            # 接受客户端的连接并创建子线程处理相应内容
            connection, address = server.accept()
            Thread(target=handle, args=(connection, address)).start()
    except Exception as e:
        print("服务器出错: " + str(e))
```
# 六、客户端实现
## chat_client模块
要实现多人聊天，首先要把==socket==封装类作为模块给客户端调用，这样可以实现把不同用户的信息封装起来互不干扰
**代码如下**
**chat_client**
```python
import math
import socket

class ChatSocket:
    # 构造方法
    def __init__(self):
        print("初始化tcp客户端")
        # 创建对象的同时，会创建连接服务器的socket
        self.client_socket = socket.socket()  # 创建socket
        self.client_socket.connect(('127.0.0.1', 5000))  # 请求连接服务器

    # 请求登录类型
    def login_type(self, user_name, password):
        # 发送请求登陆标记给服务器
        self.client_socket.sendall(bytes("1", "utf-8"))
        # 依次调用实例方法向服务器发送用户名和密码
        self.send_string_with_length(user_name)
        self.send_string_with_length(password)
        # 调用实例方法获取服务器的返回值，"1"代表通过，“0”代表不通过
        check_result = self.recv_string_by_length(1)  # 调用此对象的实例方法获取服务器的消息
        return check_result  # True代表登录请求通过，False代表登录请求失败

    # 请求注册类型
    def register_user(self, user_name, password, file_name):
        # 发送请求注册标记给服务器
        self.client_socket.sendall(bytes("2", "utf-8"))
        # 调用实例方法依次发送用户名密码头像路径给给服务器
        self.send_string_with_length(user_name)
        self.send_string_with_length(password)
        self.send_string_with_length(file_name)
        # 调用实例方法获取返回值
        # "0"代表通过，“1”代表已有用户名, "2"代表其他错误
        return self.recv_string_by_length(1)

    # 发送消息类型
    def send_message(self, message, chat_user):
        # 发送消息标记
        self.client_socket.sendall(bytes("3", "utf-8"))
        # 调用实例方法发送聊天对象，默认为群聊
        self.send_string_with_length(chat_user)
        # 调用此对象实例方法发送消息内容给服务器
        self.send_string_with_length(message)

    # 发送刷新用户列表类型
    def send_refurbish_mark(self):
        # 发送刷新用户列表标记给服务器
        self.client_socket.sendall(bytes("4", "utf-8"))

    # =============== 封装一些发送接受数据的方法 =================
    # 发送带长度的字符串
    def send_string_with_length(self, content):
        # 先发送内容的长度
        self.client_socket.sendall(bytes(content, encoding='utf-8').__len__().to_bytes(4, byteorder='big'))
        # 再发送内容
        self.client_socket.sendall(bytes(content, encoding='utf-8'))

    # 获取服务器传来的定长字符串
    def recv_string_by_length(self, len):
        return str(self.client_socket.recv(len), "utf-8")

    # 获取服务端传来的变长字符串，这种情况下服务器会先传一个长度值
    def recv_all_string(self):
        length = int.from_bytes(self.client_socket.recv(4), byteorder='big')  # 获取消息长度
        b_size = 3 * 1024  # 注意utf8编码中汉字占3字节，英文占1字节
        times = math.ceil(length / b_size)
        content = ''
        for i in range(times):
            if i == times - 1:
                seg_b = self.client_socket.recv(length % b_size)
            else:
                seg_b = self.client_socket.recv(b_size)
            content += str(seg_b, encoding='utf-8')
        return content

    # 获取服务器发的在线用户人数
    def recv_number(self):
        return int.from_bytes(self.client_socket.recv(4), byteorder='big')
```
**上面代码解释如下**:
在==chat_client==模块构造方法创建了==socket,还有一些向服务器发送不同类型请求的实例方法，比如登陆，注册请求，这些实例只是做相应的处理请求，并没有直接向服务器发送消息和接受消息，而是单独调用被封装的发送消息和接受消息实例方法，好处就是是可以实现可重用代码，不用再每一个请求中都重复输入这代码，这样我们再每一个处理实例中只需输入一句调用语句即可
> <font color="red" size=3>注意：上面代码是给客户端main调用的,单独运行没效果</font>

## 客户端main模块
客户端main模块功能主要是创建相应界面对象，处理用户按钮事件。
**main.py**
```python
from tkinter import messagebox  # 导入提示框
import threading
import time
import tkinter.filedialog   # 导入文件选择对话框模块
# 导入自定义模块
import chat_register_panel
import chat_main_panel
import chat_login_panel
import chat_client

chat_user = "【群聊】"  # 生命全局变量默认为群聊

# 关闭socket函数
def close_socket():
    print("尝试断开socket连接")
    # 对象调用实例方法关闭socoket
    client.client_socket.close()

# 关闭登陆界面函数
def close_login_window():
    close_socket()  # 关闭前先调用关闭socket函数
    login_frame.login_frame.destroy()  # 对象调用实例方法关闭登陆界面

# 关闭聊天界面函数
def close_main_window():
    # 关闭前先用对象调用实例方法给服务器发送用户退出聊天室标记
    client.send_message("exit", chat_user)
    close_socket()  # 调用关闭socket函数
    main_frame.main_frame.destroy()  # # 对象调用实例方法关闭登陆界面

# 打开文件对话框函数，用于添加头像
def file_open_face():
    # 打开文件对话框
    file_name = tkinter.filedialog.askopenfilename()
    # 路径不为空则读取图片并在头像中显示
    if file_name != '':
        # 对象调用实例方法添加头像
        register_frame.add_face(file_name)
    else:
        messagebox.showwarning(title="提示", message="你还没有选择文件！")

# 处理私聊功能函数
def private_talk(self):
    global chat_user  # 生命全局变量，方便再其他函数中使用
    # 对象使用实例变量，也就是列表组件获取点击的索引
    indexs = main_frame.friend_list.curselection()
    index = indexs[0]
    if index > 0:
        chat_user = main_frame.friend_list.get(index)  # 获取点击的用户名
        # 修改标题名称
        if chat_user == '【群聊】':  # 如果聊天对象为群聊，设置如下标题
            title = "    在线用户         python聊天室欢迎您：" + main_frame.user_name + "                       " + \
            "                           "
            main_frame.change_title(title)
        elif chat_user == main_frame.user_name:  # 如果用户选择了自己则提示如下对话框
            messagebox.showwarning(title="提示", message="自己不能和自己进行对话!")
            chat_user = '【群聊】'  # 把聊天对象改为群聊
        else:  # 否则改为下面标题
            title = "                                " + main_frame.user_name + "  私聊 -> " + chat_user + \
                    "                                                    "
            main_frame.change_title(title)

# 登录按钮处理事件函数
def handding_login(self):
    # 调用chat_login_pannel模块的对象实例方法获取输入的用户名和密码
    user_name, password = login_frame.get_input()
    # 判断用户名和密码不能为空
    if user_name == "":
        messagebox.showwarning(title="提示", message="用户名不能为空")
        return
    if password == "":
        messagebox.showwarning(title="提示", message="密码不能为空")
        return
    # 调用在此类创建的chat_client模块的对象的实例方法，如何返回True，则登录成功
    if client.login_type(user_name, password) == "1":
        go_to_main_panel(user_name)  # 调用此类的前往聊天主界面函数，参数为用户名
    else:
        messagebox.showwarning(title="提示", message="用户名或密码错误！")

# 登陆界面注册按钮处理事件函数
def handding_register():
    login_frame.close_login_panel()  # 调用在此类创建的login_frame对象的实例方法关闭登录界面
    global register_frame  # 声明全局变量，方便在其他函数使用
    # 创建chat_register_panel模块的注册界面的对象，把此类关闭注册页面前往登录界面的函数close_register_window,
    # 注册按钮事件函数register_submi,打开文件对话框添加头像函数作为参数
    # 可以把chat_login_pannel模块的事件绑定在这几个函数上
    register_frame = chat_register_panel.RegisterPanel(file_open_face, close_register_window, register_submit)
    # 调用对象的实例方法显示注册界面
    register_frame.show_register_panel()
    register_frame.load()

# 关闭注册界面函数
def close_register_window():
    register_frame.close_register_panel()  # 调用在此类创建的register_frame对象的实例方法关闭注册界面
    global login_frame  # 使用全局变量,可以在其他函数使用
    # 创建chat_login_panel模块的登录界面的对象，把此类登录处理函数handding_login,
    # 注册处理函数作handding_register，关闭登录界面客户端的socket的close_login_window作为参数
    # 可以把chat_login_pannel模块的事件绑定在这几个函数上
    login_frame = chat_login_panel.LoginPanel(handding_login, handding_register, close_login_window)
    login_frame.show_login_panel()  # 对象调用聊天主界面对象的实例方法
    login_frame.load()  # 调用对象实例方法加载动图，以及显示界面

# 注册界面注册按钮处理事件函数
def register_submit(self):
    # 调用在此类创建的对象实例方法获取用户名，密码，确认密码，头像文件路径
    user_name, password, confirm_password, file_name = register_frame.get_input()
    # 判断用户名，密码，确认密码是否为空
    if user_name == "" or password == "" or confirm_password == "":
        messagebox.showwarning("不能为空", "请完成注册表单")
        return
    # 判断密码和确认密码是否一致
    if not password == confirm_password:
        messagebox.showwarning("错误", "两次密码输入不一致")
        return
    if register_frame.file_name == "":
        messagebox.showwarning("错误", "请选择头像！")
        return
    # 对象调用实例方法发送消息给服务器
    result = client.register_user(user_name, password, file_name)
    if result == "0":
        # 注册成功，跳往登陆界面
        messagebox.showinfo("成功", "注册成功")
        close_register_window()  # 调用函数关闭注册页面前往登录界面函数
    # 返回1则用户名重复
    elif result == "1":
        # 用户名重复
        messagebox.showerror("错误", "该用户名已被注册")
    # 其他错误
    elif result == "2":
        # 未知错误
        messagebox.showerror("错误", "发生未知错误")

# 发送消息按钮处理事件函数
def send_message(self):
    global chat_user
    print("send message:")
    # 调用调用在此类创建的chat_main_panel模块的对象的实例方法获取发送内容
    content = main_frame.get_send_text()
    # 判断内容是不是为空
    if content == "" or content == "\n":
        messagebox.showwarning(title="提示", message="空消息，拒绝发送")
        return
    print(content)
    # 调用调用在此类创建的chat_main_panel模块的对象的实例方法清空输入框的内容
    main_frame.clear_send_text()
    # 调用在此类创建的chat_client模块的对象的实例方法发送聊天内容给服务器
    client.send_message(content, chat_user)

# 发送表情标记函数
def send_mark(exp):
    global chat_user # 声明全局变量
    # 调用在此类创建的chat_client模块的对象的实例方法发送表情标记给服务器
    client.send_message(exp, chat_user)

# 刷新用户列表按钮处理事件函数
def refurbish_user():
    client.send_refurbish_mark()  # 发送刷新用户列表标记给服务器

# 关闭登陆界面前往主界面
def go_to_main_panel(user_name):
    login_frame.close_login_panel()  # 调用login_frame对象的实例方法关闭窗口
    global main_frame  # # 声明全局变量，可以在类中的其他函数使用
    # 创建chat_main_panel模块的对象，把用户名，此类的发送消息函数，发送表情包标记函数，
    # 私聊功能函数，关闭聊天界面函数作为参数
    # 可以把chat_main_panel模块的事件绑定在这几个函数上
    main_frame = chat_main_panel.MainPanel(user_name, send_message, send_mark, refurbish_user, private_talk, close_main_window)
    # 创建子线程专门负责接收并处理数据
    threading.Thread(target=recv_data).start()
    main_frame.show_main_panel()  # 对象调用聊天主界面对象的实例方法创建组件布局
    main_frame.load()  # 调用对象实例方法加载动图，并显示登陆界面

# 处理消息接收的线程方法
def recv_data():
    # 暂停1秒，等主界面渲染完毕
    time.sleep(1)
    while True:
        try:
            # 首先获取处理数据类型，然后做相应处理
            data_type = client.recv_all_string()  # 调用对象实例方法获取服务器发的消息
            print("recv type: " + data_type)
            # 获取当前在线用户列表
            if data_type == "#!onlinelist#!":
                print("获取在线列表数据")
                online_list = list()  # 创建列表存储用户
                online_number = client.recv_number()   # 对象调用实例方法获取在线用户数
                for n in range(online_number):
                    # 对象每次调用实例方法获取服务器发的用户名，然后添加到列表中
                    online_list.append(client.recv_all_string())
                # 对象调用实例方法刷新聊天界面用户在线列表
                main_frame.refresh_friends(online_number, online_list)
                print(online_list)
            elif data_type == "#!message#!":
                print("获取新消息")
                # 调用对象实例方法获取服务器发送的聊天对象，以及用户名
                chat_flag = client.recv_all_string()
                user = client.recv_all_string()
                print("user: " + user)
                # 调用对象实例方法获取服务器发送的内容
                content = client.recv_all_string()
                print("message: " + content)
                # 对象调用实例方法显示消息
                main_frame.show_send_message(user, content, chat_flag)
        except Exception as e:
            print("接受服务器消息出错，消息接受子线程结束。" + str(e))
            break

#  前往登录界面，同时开启客户端口连接连接服务器的函数
def go_to_login_panel():
    global client  # 声明全局变量，可以在其他函数使用
    client = chat_client.ChatSocket()  # 创建chat_client模块中的客户端连接服务器的socket对象
    global login_frame # 声明全局变量，可以在其他函数使用
    # 创建chat_login_panel模块的登录界面的对象，把此类登录处理函数handding_login,
    # 注册处理函数作handding_register，关闭登录界面客户端的socket中close_login_window函数作为参数
    # 可以把chat_login_pannel模块的事件绑定在这几个函数上
    login_frame = chat_login_panel.LoginPanel(handding_login, handding_register, close_login_window)
    login_frame.show_login_panel()  # 对象调用聊天主界面对象的实例方法创建组件以及布局
    login_frame.load()  # 调用对象实例方法加载动图并显示界面

# 入口
if __name__ == "__main__":
    go_to_login_panel()   # 调用此类的前往登录界面函数
```

> 至此所以模块已给出，上面的==main==模块就是主程序，运行main就行了，前提是服务器==chat_server==要先运行否则会报错。

 **简单介绍下main模块的执行过程**:
 当运行main模块时会先从程序入口开始运行，也就是先执行go_to_login_panel函数，这个函数首先创建chat_client模块的ChatSocket对象，创建对象的同时创建的socket连接服务器，之后再创建了chat_login_panel模块的对象显示界面，参数为这个界面的两个按钮处理事件以及关闭界面函数，其他界面也是类似的。
