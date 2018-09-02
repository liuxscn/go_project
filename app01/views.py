from utils import sqlhelper
from django.shortcuts import HttpResponse, render, redirect
import pymysql

def login(request):

    # return HttpResponse(request.method + ' hey there')
    # return render(request, 'login.html')
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        u = request.POST.get('user')
        p = request.POST.get('pwd')
        print(u, p)
        if u == 'root' and p == 'root':
            return redirect('/index/')
            # return redirect('https://github.com')
        else:
            return render(request, 'login.html', {'error_msg' : '用户名或密码错误'})

def index(request):

    return render(
        request,
        'index.html',
        {
            'name' : 'alex',
            'users' : ['立志', '理解'],
            'user_dict': {'k1' : 'v1', 'k2' : 'v2'},
            'user_list_dict' : [
                {'id':'1', 'name':'alex', 'email':'alex@qq.com'},
                {'id':'2', 'name':'bran', 'email':'bran@qq.com'},
                {'id':'3', 'name':'chan', 'email':'chan@qq.com'},
            ]
        }
    )
    # return HttpResponse(request.method + ' Index')


def classes(request):
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='test', port=3306, charset='utf8')
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    #cur = conn.cursor()
    cur.execute('select * from classes')
    db_data = cur.fetchall()
    cur.close()
    conn.close()

    return render(
        request,
        'classes.html',
        {'classes_data': db_data}
    )

def del_class(request):
    del_id = request.GET.get('nid')

    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='test', port=3306, charset='utf8')
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # cur = conn.cursor()
    flag = cur.execute('delete from classes where id=%s', [del_id,])
    # db_data = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()

    return redirect('/classes/')


def add_class(request):
    class_name = request.POST.get('name')

    if class_name != '':
        conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='test', port=3306, charset='utf8')
        cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # cur = conn.cursor()
        flag = cur.execute('insert into classes (name) values (%s)', [class_name, ])
        # db_data = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return redirect('/classes/')

    else:
        conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='test', port=3306, charset='utf8')
        cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # cur = conn.cursor()
        cur.execute('select * from classes')
        db_data = cur.fetchall()
        cur.close()
        conn.close()

        return render(request, 'classes.html',
                      {'classes_data': db_data,
                        'error_msg' : '添加名称不能为空'})

def edit_class(request):
        if request.method == 'GET':
            edit_id = request.GET.get('nid')
            conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='test', port=3306, charset='utf8')
            cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
            # cur = conn.cursor()
            cur.execute('select * from classes where id=%s', [edit_id, ])
            db_data = cur.fetchone()
            cur.close()
            conn.close()
            edit_error_msg = ''
            if not db_data.get('id') or db_data.get('id') == '':
                edit_error_msg = '未从数据库中检索到数据'
            return render(request, 'edit_class.html', {
                'classes_id': db_data.get('id'),
                'classes_name': db_data.get('name'),
                'edit_error_msg': edit_error_msg
            })

        elif request.method == 'POST':
            edit_id = request.GET.get('nid')
            edit_name = request.POST.get('class_name')

            #if edit_id

            if not edit_name or edit_name == '':
                conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='test', port=3306,
                                       charset='utf8')
                cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
                # cur = conn.cursor()
                cur.execute('select * from classes where id=%s', [edit_id, ])
                db_data = cur.fetchone()
                cur.close()
                conn.close()

                edit_error_msg = '名称不能为空'
                return render(request, 'edit_class.html', {
                'classes_id': db_data.get('id'),
                'classes_name': db_data.get('name'),
                'edit_error_msg': edit_error_msg
                })

            else:
                print('edit_id: ', edit_id)
                print('edit_name: ', edit_name)
                conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='test', port=3306,
                                       charset='utf8')
                # cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
                cur = conn.cursor()
                cur.execute('update classes set name=%s where id=%s', [edit_name, edit_id, ])
                conn.commit()
                cur.close()
                conn.close()

                return redirect('/classes/')

def students(request):
    sql = 'select students.id,students.name,classes.name as class_name from students left join classes on students.class_id=classes.id'
    args = []
    students_list = sqlhelper.get_list(sql, args)
    return render(request, 'students.html', {
        'students_data': students_list
    })

def add_student(request):
    if request.method == 'GET':
        sql = 'select id, name from classes'
        args = []
        classes_data = sqlhelper.get_list(sql, args)

        return render(request, 'add_student.html', {'classes_data' : classes_data})

    elif request.method == 'POST':
        class_id = request.POST.get('class_id')
        student_name = request.POST.get('student_name')
        sql = 'insert into students(name,class_id) values(%s, %s)'
        args = [student_name, class_id, ]
        sqlhelper.insert(sql, args)
        return redirect('/students/')

    else:
        return HttpResponse('error in add_student')

def del_student(request):
    nid = request.GET.get('nid')
    sql = 'delete from students where id=%s'
    args = [nid, ]
    sqlhelper.delete(sql, args)
    return redirect('/students/')

def edit_student(request):
    if request.method == 'GET':
        nid = request.GET.get('nid')
        sql = 'select id,name, class_id from students where id=%s'
        args = [nid, ]
        current_student_data = sqlhelper.get_one(sql, args)
        sql_class = 'select * from classes'
        classes_data = sqlhelper.get_list(sql_class, [])

        return render(request, 'edit_student.html', {'classes_data' : classes_data,
                                                     'current_student_data': current_student_data})

    elif request.method == 'POST':
        nid = request.GET.get('nid')
        name = request.POST.get('student_name')
        class_id = request.POST.get('class_id')
        if len(name) > 0:
            sql = 'update students set name=%s, class_id=%s where id=%s'
            args = [name, class_id, nid, ]
            sqlhelper(sql, args)
            return redirect('/students/')
        else:
            print('nid: ', nid)
            sql = 'select id,name,class_id from students where students.id=%s'
            args = [nid, ]
            current_student_data = sqlhelper.get_one(sql, args)
            sql_class = 'select * from classes'
            classes_data = sqlhelper.get_list(sql_class, [])

            print('current_student_data.id: ', str(current_student_data))

            return render(request, 'edit_student.html', {
                'classes_data' : classes_data,
                'current_student_data': current_student_data,
                'error_msg' : '学生姓名不能为空'
            })

    else:
        return HttpResponse('error in edit_student')