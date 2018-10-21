import json
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
    sql = 'select students.id,students.name,classes.id as class_id, classes.name as class_name from students left join classes on students.class_id=classes.id'
    args = []
    students_list = sqlhelper.get_list(sql, args)

    sql_class = 'select id, name from classes'
    args = []
    classes_list = sqlhelper.get_list(sql_class, args)
    return render(request, 'students.html', {
        'students_data': students_list,
        'classes_data': classes_list,
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
        if len(student_name) > 0:
            sql = 'insert into students(name,class_id) values(%s, %s)'
            args = [student_name, class_id, ]
            sqlhelper.insert(sql, args)
            return redirect('/students/')
        else:
            sql = 'select id, name from classes'
            args = []
            classes_data = sqlhelper.get_list(sql, args)
            return render(request, 'add_student.html', {'classes_data' : classes_data,
                                                        'error_msg' : '不能为空'})

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
            sqlhelper.update(sql, args)
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

def modal_add_class(request):
    name = request.POST.get('name')
    if len(name) > 0:
        sql = 'insert into classes(name) values(%s)'
        args = [name, ]
        sqlhelper.insert(sql, args)
        # return redirect('/classes/')
        return HttpResponse('ok')

    else:
        return HttpResponse('名称不能为空')
    # print(name)
    # import time
    # time.sleep(5)

def modal_add_student(request):
    ret = {'status': True, 'message': None}
    try:
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        if len(name) > 0:
            sql = 'insert into students(name, class_id) values(%s, %s)'
            args = [name, class_id, ]
            sqlhelper.insert(sql, args)
        else:
            ret['status'] = False
            ret['message'] = '学生名称不能为空'
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)

    return HttpResponse(json.dumps(ret))

def modal_edit_student(request):
    ret = {'status': True, 'message': None}
    try:
        student_id = request.POST.get('student_id')
        student_name = request.POST.get('student_name')
        class_id = request.POST.get('class_id')
        if len(student_name) > 0:
            sql = 'update students set name=%s, class_id=%s where id=%s'
            args = [student_name, class_id, student_id, ]
            sqlhelper.update(sql, args)
        else:
            ret['status'] = False
            ret['message'] = '学生名称不能为空'
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)

    return HttpResponse(json.dumps(ret))

def teachers(request):
    sql = '''SELECT test.teachers.id as t_id,test.teachers.name as t_name, test.teachers_classes.class_id as c_id, test.classes.name as c_name
            FROM test.teachers
            LEFT JOIN test.teachers_classes on test.teachers.id=test.teachers_classes.teacher_id
            LEFT JOIN test.classes on test.teachers_classes.class_id=test.classes.id;'''
    args = []
    teachers_list = sqlhelper.get_list(sql, args)
    ret = {}
    for row in teachers_list:
        tid = row['t_id']
        if tid in ret:
            ret[tid]['c_id'].append(row['c_id'])
            ret[tid]['c_name'].append(row['c_name'])
        else:
            c_id_list = []
            c_id_list.append(row['c_id'])
            c_name_list = []
            c_name_list.append(row['c_name'])
            ret[tid] = {'t_id': row['t_id'], 't_name': row['t_name'], 'c_id': c_id_list, 'c_name': c_name_list}

    return render(request, 'teachers.html', {
        'teachers_data': ret.values(),
    })

def add_teacher(request):
    ret = {'status': True, 'message': None}
    try:
        if request.method == 'GET':
            sql = 'select id,name from classes'
            args = []
            classes_list = sqlhelper.get_list(sql, args)
            return render(request, 'add_teacher.html', {
                'classes_data': classes_list,
            })
        else:
            teacher_name = request.POST.get('teacher_name')
            class_id_list = request.POST.getlist('class_id')
            print(teacher_name, class_id_list)
            if len(teacher_name) > 0 and class_id_list:
                obj_sql = sqlhelper.SqlHelper()
                sql = 'insert into teachers(name) values(%s)'
                args = [teacher_name, ]
                # teacher_id = sqlhelper.insert(sql, args)
                teacher_id = obj_sql.create(sql, args)
                sql1 = 'insert into teachers_classes(teacher_id, class_id) values(%s, %s)'
                # for class_id in class_id_list:
                #     args1 = [teacher_id, ]
                #     args1.append(class_id)
                #     sqlhelper.insert(sql1, args1)
                args1 = []
                for class_id in class_id_list:
                    temp = (teacher_id, class_id)
                    args1.append(temp)
                obj_sql.multiple_modify(sql1, args1)
                obj_sql.close()
                return redirect('/teachers/')
            else:
                raise Exception('老师姓名或班级ID不能为空')
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)

    return HttpResponse(ret['message'])

def edit_teacher(request):
    try:
        t_id = request.GET.get('nid')
        sql_obj = sqlhelper.SqlHelper()
        if request.method == 'GET':
            t_name_ret = sql_obj.get_one('select name from teachers where id=%s', t_id)
            t_name = t_name_ret.get('name')
            class_ids_ret = sql_obj.get_list('select class_id from teachers_classes where teacher_id=%s', t_id)
            class_ids = []
            for item in class_ids_ret:
                class_ids.append(item.get('class_id'))
            class_list = sql_obj.get_list('select id, name from classes', [])

            return render(request, 'edit_teacher.html', {
                't_id': t_id,
                't_name': t_name,
                'class_ids': class_ids,
                'class_list': class_list,
            })
        elif request.method == 'POST':
            t_name = request.POST.get('teacher_name')
            class_ids = request.POST.getlist('class_ids')
            if len(t_name) > 0 and class_ids:
                sql_obj.modify('update teachers set name=%s where id=%s', [t_name, t_id, ])
                sql_obj.modify('delete from teachers_classes where teacher_id=%s', [t_id, ])
                rel_list = []
                for class_id in class_ids:
                    rel_list.append((t_id, class_id))
                sql_obj.multiple_modify('insert into teachers_classes(teacher_id, class_id) values(%s, %s) ', rel_list)
                return redirect('/teachers/')
            else:
                raise Exception('老师姓名或班级ID不能为空')

        sql_obj.close()
    except Exception as e:
        return HttpResponse(str(e))


def test(request):
    return render(request, 'test.html')

def layout(request):
    return render(request, 'layout.html')