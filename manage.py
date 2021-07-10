'''
@File    ：manage.py
@Author  ：Bell_Meng
@Date    ：2021/7/10 7:34 
'''

# 模块导入
from flask import Flask
from config import BaseConfig
from views import user_app
from models import db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__, static_url_path='/statics', static_folder='statics')
# app配置
app.config.from_object(BaseConfig)
# 配置数据库
db.init_app(app)
app.register_blueprint(user_app)

migrate = Migrate()
migrate.init_app(app=app, db=db)

manager = Manager(app)
manager.add_command("db", MigrateCommand)


# 注册蓝图


@app.errorhandler(404)
def handle_404_error(err):
    """自定义的处理错误方法"""
    return "出现了404错误"


if __name__ == '__main__':
    # 运行app
    manager.run()
