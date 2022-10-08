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
