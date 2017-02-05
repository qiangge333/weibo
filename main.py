import flask
from flask import Flask
from flask import render_template

from user import main as user_routes
from weibo import main as weibo_routes
from comment import main as comment_routes

app = Flask(__name__)
# 设置 secret_key 来使用 flask 自带的 session
# 这个字符串随便你设置什么内容都可以
app.secret_key = 'random string'
# 这一行是套路
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


"""
在 flask 中，模块化路由的功能由 蓝图（Blueprints）提供
蓝图可以拥有自己的静态资源路径、模板路径（现在还没涉及）
用法如下
"""
# 注册蓝图
# 有一个 url_prefix 可以用来给蓝图中的每个路由加一个前缀
app.register_blueprint(comment_routes)
app.register_blueprint(user_routes)
app.register_blueprint(weibo_routes)


# cookie 设置
# @app.route('/cookie')
# def cookie_set():
#     """
#     使用 make_response 生成响应的东西
#     然后使用 set_cookie 函数来设置 cookie
#     """
#     page = render_template('cookie.html')
#     r = flask.make_response(page)
#     r.set_cookie('mark', 'foo')
#     r.set_cookie('name', 'gua')
#     return r
"""
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 182
Set-Cookie: mark=foo
Set-Cookie: name=gua
"""


"""
可以通过这样的方式自定义错误页面
比如很多网站都自定义 404 页面
就可以通过这样的方式来完成
"""
# @app.errorhandler(404)
# def error404(e):
#     return render_template('404.html')


# @app.errorhandler(501)
# def error501(e):
#     return "<h1>501 错误</h1>"


# @app.route('/error/<int:code>')
# def error_code(code):
#     # from flask import abort
#     if code == 402:
#         return '<h1>402 错误</h1>', 402
#     import flask
#     # abort 函数直接返回一个错误页面
#     # 参数是 状态码
#     flask.abort(code)


# 运行代码
# 默认端口是 5000
if __name__ == '__main__':
    app.run(debug=True)
