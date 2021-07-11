'''
@File    ：views.py
@Author  ：Bell_Meng
@Date    ：2021/7/10 9:44 
'''

from flask import Blueprint, render_template, request, url_for
from models import db, PasteBin

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

        return render_template('index.html', paste_bin_list=paste_bin_list)


@user_app.route('/login', endpoint='login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":

        return render_template('login.html')
    else:
        return '登录成功'


@user_app.route('/signup', endpoint='signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        return '注册成功'


@user_app.route('/view/<paste_id>', endpoint='view_paste')
def view_paste(paste_id):
    if paste_id:
        paste_bin = PasteBin.query.filter_by(id=str(paste_id)).all()
        if paste_bin:
            return render_template('view-paste.html', paste_bin=paste_bin[0])
        else:
            return '不存在'
    else:
        return '您访问的页面不存在'
