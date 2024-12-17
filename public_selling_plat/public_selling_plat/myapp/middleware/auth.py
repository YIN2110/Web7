from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect
import re
class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 如果用户访问的是 www.baidu.com，直接允许
        if (request.path_info == "/myapp/visitor_index"
                or request.path_info == "/myapp/login"
                or request.path_info == "/myapp/regist"
                or request.path_info == "/myapp/reset_password"
        ):
            # 将session中的info设为空
            request.session["info"] = None
            return

        # 检查URL是否以/myapp/change_password/开始
        if re.match(r'^/myapp/change_password/\d+$', request.path_info):
            request.session["info"] = None
            return

        # 读取浏览器中的session信息 如果能读到 说明已经登陆
        info_dict = request.session.get('info')
        if info_dict:
            return

        # 如果没有登陆过，可以选择弹出提示框或者跳转到登录页面
        # 使用HttpResponse返回一个JavaScript弹窗提示
        return HttpResponse('<script>alert("请先注册或登录!"); window.location.href="/myapp/login";</script>')


