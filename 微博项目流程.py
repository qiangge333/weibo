"""
2016/11/25

web 17


本节课用
微博
作为例子来讲写网站的套路步骤(如下)

1, 准备 model(weibo)
    user(model)
    id
    username
    password
    created_time
    weibo(model)
    id
    content
    user_id
    created_time
    comment(model)
    id
    content
    created_time
    user_id
    weibo_id

2, 写出操作场景的文档(你要对这些数据做什么操作, 这是最重要的一步)
有一个主页可以用来显示所有微博
     点击进入个人页
    可以用来来用户登录（有注册链接）登录后转到主页
    可以发表新微博
    有所有的微博内容
有一个页面可以用来注册
    注册后转到主页
有一个微博页，显示微博和所属的的所有评论
    作者， 时间， 内容
    有表单可以发表新评论
    列出所有评论
    微博作者可以删除评论
有一个页面用来显示个人微博
    可以发表新微博
    我的所有微博  可以删除
    可以查看微博

3, 根据文档, 写好 CURD 和其他操作(比如验证用户注册合法性的函数)
        User.add()
        user.redilte_login()
        user.redilte_resiget()
        weibo.all()
        weobo.query.find(user_id).all
        wweibo.add()
        weibo.delete()
        weibo.update()
        comment.query.find(weibo_id).all
        comment.add()
        comment.delete()


4, 画 html 页面
5, 写路由函数来连接整个功能
6, 美化页面


请参考这个链接(班上同学做的)
http://45.32.110.118/
"""