from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import Blueprint
from flask import session

import time

from models import User
from models import Weibo
from models import Comment

# 创建一个 蓝图对象 并且路由定义在蓝图对象中
# 然后在 flask 主代码中「注册蓝图」来使用
# 第一个参数是蓝图的名字，第二个参数是套路
main = Blueprint('weibo', __name__)


def log(*args, **kwargs):
    f = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(f, value)
    # 中文 windows 平台默认打开的文件编码是 gbk 所以需要指定一下
    with open('log.gua.txt', 'a', encoding='utf-8') as f:
        # 通过 file 参数可以把输出写入到文件 f 中
        # 需要注意的是 **kwargs 必须是最后一个参数
        print(dt, *args, file=f, **kwargs)


def current_user():
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(uid)
        return u


@main.route('/weibo')
def index():
    u = current_user()
    ws = Weibo.query.all()
    # log('debug')
    # log('weibo', ws)
    return render_template('weibo_index.html', weibos=ws)


@main.route('/weibo/<int:weibo_id>')
def detail(weibo_id):
    w = Weibo.query.get(weibo_id)
    cs = Comment.query.filter_by(weibo_id=w.id).all()
    log('weibo and comments', w, cs)
    return render_template('weibo_detail.html', weibo=w, comments=cs)


@main.route('/weibo/<int:user_id>')
def user_weibo(user_id):
    u = User.query.get(user_id).first()
    user = current_user()
    if user == u:
        ws = u.weibos()
        return render_template('user_weibo.html', weibos=ws)
    else:
        return url_for(".index")


@main.route('/weibo/edit/<int:weibo_id>')
def edit(weibo_id):
    u = current_user()
    w = Weibo.query.get(weibo_id)
    # log('user and weibo', u, w)
    if u is not None and u.username == w.username:
        return render_template('weibo_edit.html', weibo=w)
    else:
        return redirect(url_for('weibo.detail', weibo_id=weibo_id))


@main.route('/weibo/add', methods=['POST'])
def add():
    u = current_user()
    if u is not None:
        form = request.form
        w = Weibo(form)
        w.username = u.username
        w.save()
    return redirect(url_for('weibo.index'))


@main.route('/weibo/delete/<int:weibo_id>')
def deleted(weibo_id):
    # log('debug')
    u = current_user()
    w = Weibo.query.get(weibo_id)
    # log('weibo', w)
    if u.username == w.username:
        w.delete()
        # log('debug')
        return redirect(url_for('weibo.index'))
    else:
        return redirect(url_for('weibo.detail', weibo_id=weibo_id))


@main.route('/weibo/update', methods=['POST'])
def update():
    form = request.form
    weibo_id = int(form.get('weibo_id'))
    # log('form and weibo_id', form, weibo_id, type(weibo_id))
    w = Weibo.query.get(weibo_id)
    # log('debug weibo', w)
    w.update(form)
    return redirect(url_for('weibo.detail', weibo_id=weibo_id))

