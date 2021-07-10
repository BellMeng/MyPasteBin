'''
@File    ：views.py
@Author  ：Bell_Meng
@Date    ：2021/7/10 9:44 
'''

from flask import Blueprint, render_template
user_app = Blueprint('user_app', __name__)



@user_app.route('/', endpoint='index')
def index():
    cnt = [i for i in range(1000)]
    return render_template('index.html', cnt=cnt)


@user_app.route('/login', endpoint='login')
def login():
    return render_template('login.html')


@user_app.route('/signup', endpoint='singnup')
def signup():
    return render_template('signup.html')
