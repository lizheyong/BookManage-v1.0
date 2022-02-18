from rest_framework.authentication import  BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from jwt import exceptions
from django.conf import settings

"""jwt认证"""
class JwtQueryParamsAuthentication(BaseAuthentication):

    def authenticate(self, request):
        #这个可以灵活修改，token传在请求头，其他地方，可以改
        token = request.query_params.get("token")  # 从url中获取token
        # token = request._request.get("token")   #从上一个request中获取token

        # 1.切割
        # 2.解密第二段/判断过期
        # 3.验证第三段合法性
        salt = settings.SECRET_KEY
        payload = None
        try:
            payload = jwt.decode(token, salt, True)  # True表示校验（时间，第三段合法性）
        except exceptions.ExpiredSignatureError:
            raise AuthenticationFailed({'code':1003,'error':"token已失效，请登录！"})
        except jwt.DecodeError:
            raise AuthenticationFailed({'code':1003,'error':"token认证失败，请登录！"})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed({'code':1003,'error':"非法的token，请登录！"})

        # 三种操作
        # 1、抛出异常，后续不再执行
        # 2、return一个元组 （1，2），认证通过，在视图中如果调用request.user就是元组的第一个值，request.auth就是元组的第二个值
        # 3、None
        return (payload, token)

"""jwt + 管理员认证"""
class AdminAuthentication(BaseAuthentication):

    def authenticate(self, request):

        token = request.query_params.get("token")
        salt = settings.SECRET_KEY
        try:
            payload = jwt.decode(token, salt, True)  # True表示校验（时间，第三段合法性）
        except exceptions.ExpiredSignatureError:
            raise AuthenticationFailed({'code': 1003, 'error': "token已失效，请登录！"})
        except jwt.DecodeError:
            raise AuthenticationFailed({'code': 1003, 'error': "token认证失败，请登录！"})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed({'code': 1003, 'error': "非法的token，请登录！"})

        if  payload.get('is_admin') == False:
            raise AuthenticationFailed({'code': 1003, 'error': "您不是管理员，无权访问！"})
        return (payload, token)

"""jwt + 管理员认证，get请求时不进行管理员认证"""
class NoGetAdminAuthentication(BaseAuthentication):

    def authenticate(self, request):

        token = request.query_params.get("token")
        salt = settings.SECRET_KEY
        try:
            payload = jwt.decode(token, salt, True)  # True表示校验（时间，第三段合法性）
        except exceptions.ExpiredSignatureError:
            raise AuthenticationFailed({'code': 1003, 'error': "token已失效，请登录！"})
        except jwt.DecodeError:
            raise AuthenticationFailed({'code': 1003, 'error': "token认证失败，请登录！"})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed({'code': 1003, 'error': "非法的token，请登录！"})

        if  (payload.get('is_admin') == False) & (request.method!='GET'):
            raise AuthenticationFailed({'code': 1003, 'error': "您不是管理员，无权访问！"})

        return (payload, token)

"""jwt + 管理员认证，post请求时不进行管理员认证"""
class NoPostAdminAuthentication(BaseAuthentication):

    def authenticate(self, request):
        # 如果不是POST请求(注册),执行jwt认证
        if request.method != 'POST':
            token = request.query_params.get("token")
            salt = settings.SECRET_KEY
            try:
                payload = jwt.decode(token, salt, True)  # True表示校验（时间，第三段合法性）
            except exceptions.ExpiredSignatureError:
                raise AuthenticationFailed({'code': 1003, 'error': "token已失效，请登录！"})
            except jwt.DecodeError:
                raise AuthenticationFailed({'code': 1003, 'error': "token认证失败，请登录！"})
            except jwt.InvalidTokenError:
                raise AuthenticationFailed({'code': 1003, 'error': "非法的token，请登录！"})
            # 如果是PUT请求(更改用户信息),不进行管理员认证
            if request.method == 'PUT':
                return(payload,token)

            if payload.get('is_admin') == False:
                raise AuthenticationFailed({'code': 1003, 'error': "您不是管理员，无权访问！"})

        return(payload,token)