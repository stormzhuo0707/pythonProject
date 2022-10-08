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
