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