'''
@File    ：run.py
@Author  ：Bell_Meng
@Date    ：2021/7/10 7:34 
'''
from flask import Flask, render_template

app = Flask(__name__, static_url_path='/statics', static_folder='statics')
app.config['DEBUG'] = True


@app.route('/index', endpoint='index')
def index():
    cnt = [i for i in range(1000)]
    return render_template('index.html', cnt=cnt)


@app.route('/login', endpoint='login')
def login():
    return render_template('login.html')


@app.route('/signup', endpoint='singnup')
def signup():
    return render_template('signup.html')


if __name__ == '__main__':
    app.run()


