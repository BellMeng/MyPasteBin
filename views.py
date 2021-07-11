'''
@File    ：views.py
@Author  ：Bell_Meng
@Date    ：2021/7/10 9:44 
'''

from flask import Blueprint, render_template, request, url_for, session, redirect, Response
from models import db, PasteBin, Role, User, CodeType

import time

user_app = Blueprint('user_app', __name__)


def create_pastebin_id():
    return str(int(time.time()))[-8:]


def parse_post(form):
    paste_bin_objec_dict = {}
    paste_bin_objec_dict['paste_bin_id'] = create_pastebin_id()
    if form.get('user'):
        paste_bin_objec_dict['user'] = form.get('user')
    paste_bin_objec_dict['content'] = form.get('content')
    paste_bin_objec_dict['title'] = form.get('title')
    paste_bin_objec_dict['is_highlight'] = True if form.get('heighlight') else False
    paste_bin_objec_dict['access'] = form.get('access_right')
    paste_bin_objec_dict['access_password'] = form.get('access_passwd')
    paste_bin_objec_dict['pwd_enable'] = True if form.get('pwd_enable') else False
    paste_bin_objec_dict['expiration'] = form.get('expiration')
    return paste_bin_objec_dict


@user_app.route('/', endpoint='index', methods=['GET', 'POST'])
def index():
    user = None
    if session.get('is_login') and session.get('user_id'):
        user = User.query.filter_by(id=session.get('user_id')).first()
    if request.method == "POST":
        obj_dict = parse_post(request.form)
        try:
            pastebin = PasteBin()
            pastebin.set_attrs(obj_dict)
            db.session.add(pastebin)
            db.session.commit()
            return "提交成功"
        except Exception:
            return '提交失败'
    else:
        paste_bin_list = PasteBin.query.filter_by(access='Public').order_by(PasteBin.timestamp.desc()).all()
        return render_template('index.html', paste_bin_list=paste_bin_list, user=user, code_type=CodeType._member_names_)


def login_verify(form):
    username = form.get('username')
    password = form.get('password')
    if not username or not password:
        return {'status': 'error', 'msg': '用户名和密码不能为空！'}
    user = User.query.filter_by(username=username, password=password).first()
    if not user:
        return {'status': 'error', 'msg': '用户名不存在或密码错误！'}
    else:
        return {'status': 'successful', 'user': user}


@user_app.route('/login', endpoint='login', methods=['GET', 'POST'])
def login():
    if session.get('is_login') and session.get('user_id'):
        return redirect(url_for('user_app.index'))
    if request.method == "GET":
        return render_template('login.html')
    else:
        verify_result = login_verify(request.form)
        if verify_result['status'] == 'successful':
            session['is_login'] = True
            session['user_id'] = verify_result.get('user').id
        return render_template('login.html', verify_result=verify_result)


def signup_verify_form(form):
    """
    验证表单信息正确性
    :param form:
    :return:
    """
    username = form.get('username')
    email = form.get('email')
    password = form.get('password')
    password_confirm = form.get('password')
    user = User.query.filter_by(username=username).all()
    if user:
        return {'status': 'error', 'msg': '该用户名已被注册！'}
    user = User.query.filter_by(email=email).all()
    if user:
        return {'status': 'error', 'msg': '该用户名已被注册！'}
    if not username or not email:
        return {'status': 'error', 'msg': '用户名和邮箱不能为空！'}
    if not password:
        return {'status': 'error', 'msg': '密码不能为空！'}
    if password != password_confirm:
        return {'status': 'error', 'msg': '两次输入的密码不一致！'}
    return {
        'status': 'successful',
        'user_info': {
            'username': username,
            'email': email,
            'password': password,
            'avatar': 'https://pastebin.com/themes/pastebin/img/guest.png'
        }
    }


@user_app.route('/signup', endpoint='signup', methods=['GET', 'POST'])
def signup():
    if session.get('is_login') and session.get('user_id'):
        return redirect(url_for('user_app.index'))
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        normal_role = Role.query.filter_by(name='普通用户').first()
        if not normal_role:
            normal_role = Role(name='普通用户')
            db.session.add(normal_role)
            db.session.commit()
            normal_role = Role.query.filter_by(name='普通用户').first()

        verify_result = signup_verify_form(request.form)
        if verify_result['status'] == 'error':
            return render_template('signup.html', verify_result=verify_result)
        user_info = verify_result['user_info']
        user = User(username=user_info.get('username'), avatar=user_info.get('avatar'), email=user_info.get('email'),
                    password=user_info.get('password'), role_id=normal_role.id)
        db.session.add(user)
        db.session.commit()

        return render_template('signup.html', verify_result=verify_result)


@user_app.route('/view/<paste_id>', endpoint='view_paste')
def view_paste(paste_id):
    user = None
    if session.get('is_login') and session.get('user_id'):
        user = User.query.filter_by(id=session.get('user_id')).first()
    if paste_id:
        paste_bin = PasteBin.query.filter_by(id=str(paste_id)).all()
        if paste_bin:
            pub_user = paste_bin[0].user if not paste_bin[0].user else User.query.filter_by(id=paste_bin[0].user).first()
            return render_template('view-paste.html', paste_bin=paste_bin[0], user=user, pub_user=pub_user)
        else:
            return '不存在'
    else:
        return '您访问的页面不存在'


@user_app.route('/logout', endpoint='logout')
def logout():
    if session.get('is_login') and session.get('user_id'):
        session.pop('is_login')
        session.pop('user_id')
    return redirect(url_for('user_app.login'))


@user_app.route('/download/<paste_id>/<filename>', endpoint='download')
def view_paste(paste_id, filename='tmp.txt'):
    if paste_id:
        paste_bin = PasteBin.query.filter_by(id=str(paste_id)).all()
        if paste_bin:
            return Response(paste_bin[0].content, mimetype='application/js')
        else:
            return '您访问的资源不存在'
    else:
        return '您访问的资源不存在'