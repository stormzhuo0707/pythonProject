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


