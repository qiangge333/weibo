from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import time

# 以下都是套路
app = Flask(__name__)
app.secret_key = 'secret key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 指定数据库的路径
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///files.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:cclab@localhost/file'

db = SQLAlchemy(app)


# 设置时间
def times():
    format = '%m/%d'
    value = time.localtime(int(time.time()))
    return time.strftime(format, value)


# ModelMixin
class ModelHelper(object):
    def __repr__(self):
        """
        __repr__ 是一个魔法方法
        简单来说, 它的作用是得到类的 字符串表达 形式
        比如 print(u) 实际上是 print(u.__repr__())
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

"""
CREATE TABLE todos (
    id INTEGER NOT NULL,
    task VARCHAR,
    created_time INTEGER,
    user_id INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY(user_id) REFERENCES users (id)
)

CREATE TABLE users (
    id INTEGER NOT NULL,
    username VARCHAR,
    password VARCHAR,
    created_time INTEGER,
    PRIMARY KEY (id)
)
"""


# 定义一个 Model，继承自 db.Model
class Weibo(db.Model, ModelHelper):
    __tablename__ = 'weibos'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text())
    created_time = db.Column(db.Text(), default=0)
    # 定义关系
    username = db.Column(db.Text())

    def comments(self):
        cs = Comment.query.filter_by(weibo_id=self.id).all()
        return cs

    def update(self, form):
        for k in form:
            if k == 'content':
                self.content = form[k]
        self.save()

    def __init__(self, form):
        self.content = form.get('content', '')
        self.created_time = times()


# 定义一个 Model，继承自 db.Model
class Comment(db.Model, ModelHelper):
    __tablename__ = 'comments'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text())
    created_time = db.Column(db.Text(), default=0)
    # 定义关系
    weibo_id = db.Column(db.Integer)
    username = db.Column(db.Text())

    def __init__(self, form):
        self.content = form.get('content', '')
        self.weibo_id = form.get('weibo_id', 0)
        self.created_time = times()


class User(db.Model, ModelHelper):
    __tablename__ = 'users'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text())
    password = db.Column(db.Text())
    created_time = db.Column(db.Text(), default=0)

    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.created_time = times()

    def weibos(self):
        ws = Weibo.query.filter_by(username=self.username).all()
        return ws

    def valid(self):
        return len(self.username) > 2 and len(self.password) > 2

    def validate_login(self, u):
        return u.username == self.username and u.password == self.password

    def change_password(self, password):
        if len(password) > 2:
            self.password = password
            self.save()
            return True
        else:
            return False


def init_db():
    # 先 drop_all 删除所有数据库中的表
    # 再 create_all 创建所有的表
    db.drop_all()
    db.create_all()
    print('rebuild database')


# def test():
#     # t1 = Todo({})
#     # t1.user_id = 1
#     # t1.save()
#     # t1 = Todo.query.get(1)
#     # print(t1.user)
#     # #
#     # t2 = Todo({'task': '吃瓜'})
#     # t2.user = t1.user
#     # t2.save()
#     u1 = User.query.get(1)
#     print('user.todos ', u1.todos.first())
#     print('user.todos ', u1.todos.all())
#     # ws = Weibo.query.filter_by(user_id=u1.id).all()
#     # print('user.weibos', u1.weibos())
#     pass
def test_user():
    form = {
        'username': 'xiao',
        'password': '123'
    }
    u = User(form)
    # log('user', u)
    if u.valid():
        u.save()
    print('users', User.query.all())
    # print('users', u)
    pass


def test_weibo():
    # form = {
    #     'content': 'good boy'
    # }
    # w = Weibo(form)
    # w.user_id = 2
    # # print('weibo', w)
    # w.save()
    # u = User.query.get(1)
    # print('user', u)
    # log('weibos', Weibo.query.all())
    # ws = Weibo.query.filter_by(user_id=u.id).all()
    # log('weibos', ws)
    # log('user.weibos', u.weibos())
    # w = Weibo.query.get(1)
    # w.delete()
    log('weibo', Weibo.query.all())
    log('weibo为空')
    pass


def test_comment():
    # form = {
    #     'content': 'good',
    # }
    # c = Comment(form)
    # c.user_id = 2
    # c.weibo_id= 1
    # c.save()
    # w = Weibo.query.get(1)
    # cs = w.comments()
    # log('weibo.comments', cs)
    c = Comment.query.get(1)
    c.delete()
    pass


if __name__ == '__main__':
    # init_db()
    # test_user()
    test_weibo()
    # test_comment()
    """
    select * from users where id=1

    update users set password='pwd' where id=1

    SELECT
        todos.id AS todos_id,
        todos.task AS todos_task,
        todos.created_time AS todos_created_time,
        todos.user_id AS todos_user_id
    FROM
        todos
    WHERE
        todos.user_id = :user_id_1
    """
    # u = User.query.get(1)
    # # u.password = 'pwd'
    # # u.save()
    # print('sql', Todo.query.filter_by(user_id=u.id))
    # ts = Todo.query.filter_by(user_id=u.id).all()
    # print('todos', ts)
