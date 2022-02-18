import jwt
import datetime
from django.conf import settings

def creat_token(payload,timeout=1):

    salt = settings.SECRET_KEY
    # 构造header,如果不写，默认下面这个
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    # 构造payload
    payload['exp']: datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)  # 超时时间
    token = jwt.encode(payload=payload, key=salt, algorithm="HS256", headers=headers)

    return token
