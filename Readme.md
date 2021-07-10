# MyPasteBin

## 1. 使用方式
1. 根据pipfile安装相应依赖
2. 在config.py中对数据库做相关配置
3. 执行如下命令进行数据库迁移
    ```shell
   python manage.py db init
   python manage.py db migrate
   python manage.py db upgrade
    ```
4. 运行项目
    ```shell
    python manage.py runserver
    ```

