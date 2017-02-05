from flask import request
from flask import redirect
from flask import url_for
from flask import Blueprint
from flask import session

from models import User
from models import Weibo
from models import Comment

from utils import log


# 创建一个 蓝图对象 并且路由定义在蓝图对象中
# 然后在 flask 主代码中「注册蓝图」来使用
# 第一个参数是蓝图的名字，第二个参数是套路
main = Blueprint('comment', __name__)


def current_user():
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(uid)
        return u


@main.route('/comment/add', methods=['POST'])
def add():
    u = current_user()
    form = request.form
    weibo_id = int(form.get('weibo_id'))
    log('form', form, weibo_id, type(weibo_id))
    if u is not None:
        c = Comment(form)
        c.username = u.username
        c.save()
        log('debug', Comment.query.get(weibo_id))
    return redirect('/weibo/{}'.format(weibo_id))


@main.route('/comment/delete/<int:comment_id>')
def deleted(comment_id):
    u = current_user()
    c = Comment.query.get(comment_id)
    w = Weibo.query.get(c.weibo_id)
    log('user, comment, weibo', u, c, w)
    if u.username == w.username:
        c.delete()
    return redirect(url_for('weibo.detail', weibo_id=w.id))
