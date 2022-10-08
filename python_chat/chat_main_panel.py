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
