
# -*- code:utf-8 -*-
# 
# 定位到lib目录
# -------------------------------------------------------------
import time, os, sys, platform,ctypes,socket,threading,jwt,datetime
path = sys.path[0]
if path.find("net") >= 0:
    if platform.uname()[0].find("Windows") >= 0:sys.path.append(path + "\\..\\..\\..")
    elif platform.uname()[0].find("Linux") >= 0:sys.path.append(path + "/../..")
else:sys.path.append(path + "/lib")

def create_token_by_data(sub='', data={}, secret='', exp_time=60 * 60 * 24):
    """
    生成对应的JWT的token值
    :param sub:    参数名称
    :param data:     参与签名的参数信息
    :param secret:   是否要求进行空检测，True必须检测
    :param exp_time:  token过期时间，按秒来计算
    :return:        返回处理后的参数
    """

    # 签名密钥的判断
    if not secret:return False, {'access_token': '', 'meg': '密匙不能为空'}
    if not data:return False, {'access_token': '', 'meg': '需要签名信息不能为空'}

    payload = {
        "iss": "xiaozhong.com",  # iss: 该JWT的签发者，是否使用是可选的；
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=exp_time),  # 什么时候过期，这里是一个Unix时间戳，是否使用是可选的；
        "iat": datetime.datetime.utcnow(),  # 在什么时候签发的(UNIX时间)，是否使用是可选的；
        "aud": "www.xiaozhong.com",  # 接收该JWT的一方，是否使用是可选的；#  如果在生成token的时候使用了aud参数，那么校验的时候也需要添加此参数
        "sub": sub,  # sub: 该JWT所面向的用户，是否使用是可选的；
        "scopes": ['open'],  # 用户授权的作用域，使用逗号（,）分隔
        "data": data
    }
    # 不参与进行签名计算
    if not sub:payload.pop('sub')
    # token生成处理
    token = jwt.encode(payload, 'secret', algorithm='HS256')
    # 返回授权token
    back_result = {
        'access_token': str(token, 'utf-8'),
        'data': data
    }
    return True, back_result
def verify_bearer_token(ischecck_sub=False, sub_in='', token=''):
    #  如果在生成token的时候使用了aud参数，那么校验的时候也需要添加此参数
    try:
        payload = jwt.decode(token, 'secret', audience='www.xiaozhong.com', algorithms=['HS256'])
        if ischecck_sub and sub_in != '':
            sub = payload['sub']
            if sub != sub_in:return False, "无效的Token"
        if payload and ('data' in payload):
            # 验证通过返回对应的参与签名的字段信息
            return True, payload['data']
        else:raise jwt.InvalidTokenError
    except jwt.ExpiredSignatureError:
        return False, "Token过期"
    except jwt.InvalidTokenError:
        return False, "无效的Token"
    except:
        return False, "无效的Token"
    return False, token