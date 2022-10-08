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









