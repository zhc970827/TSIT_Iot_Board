import time

from fastapi import Form, Depends, HTTPException
from starlette.requests import Request

from common import Func, Utils, Redis
from model.WAModel import WaUser, WaUserMembership
from . import api


async def verifyToken(user_token: str = Form(...)):
    """ 验证token并返回 """
    # 创建redis对象
    redis = Redis.getRedis()
    cache_key = "user_auth_token_" + user_token
    user_dict = redis.hgetall(cache_key)
    new_data = {key.decode('utf-8'): value.decode('utf-8') for (key, value) in user_dict.items()}
    if new_data == {}:
        raise HTTPException(status_code=401, detail='verify token failed',
                            headers={'X-Error': "There goes my error"})
    else:
        return new_data


# summary是简介直接显示在目录上，description是详细介绍
@api.post('/user/register', tags=['用户'], description='用户注册或重设密码', summary='注册或修改密码')
async def userRegister(u_phone: str = Form(...), u_password: str = Form(...),
                       verify_code: str = Form(...)):
    user = WaUser.get_or_none(u_phone=u_phone)
    # redis对象
    redis = Redis.getRedis()
    # 手机验证码
    cache_key = '%s_verify_code' % u_phone
    redis_verify_code = redis.get(cache_key)
    if not redis_verify_code:
        return Func.jsonResult({'verify_code': verify_code}, '验证码已过期，请重新请求', 200000500)
    if redis.get(cache_key).decode('utf-8') != verify_code:
        return Func.jsonResult({'verify_code': verify_code}, '验证码不正确', 200000500)
    salt = Func.md5(Func.randomStr(20))
    # MD5加盐加密
    enctyped_password = Func.md5(u_password + salt)
    if user:
        # 修改密码
        user.u_password = enctyped_password
        user.u_password_salt = salt
        user.save()
    else:
        # 新用户创建
        user = WaUser.create(u_phone=u_phone, u_password=enctyped_password,
                             u_password_salt=salt)
    # 这个是自定义的返回格式
    return Func.jsonResult({'u_id': user.u_id},)


@api.post('/sign_in', tags=['用户'], summary='登录获取token', description='登录获取token')
async def signIn(*, request: Request, u_phone: str = Form(...), u_password: str = Form(...)):
    try:
        wa_user = WaUser.get(WaUser.u_phone == u_phone)
        if wa_user.u_password != Func.md5(u_password + wa_user.u_password_salt):
            # jsonResult这个函数是公司通用定义的response格式，这里写成自己的即可
            return Func.jsonResult({}, '密码错误', 200000500)
        token_expire_at = int(time.time()) + 86400 * 30
        token = "USER:" + Func.md5((wa_user.u_phone + wa_user.u_password + str(token_expire_at)))
        dt = {
            "user_id": wa_user.u_id,
            "user_nickname": wa_user.u_phone,
            "user_token": token,
            "user_token_expired_at": token_expire_at,
        }
        # 修改
        wa_user.u_token = token
        wa_user.u_token_expire_time = token_expire_at
        wa_user.u_login_time = int(time.time())
        client_ip = request.client.host
        wa_user.u_login_ip = Utils.ip2long(client_ip)
        wa_user.save()
        # token存入redis
        rds = Redis.getRedis()
        cache_key = "user_auth_token_" + token
        rds.hmset(cache_key, dt)
        rds.expire(cache_key, 30 * 86400)
        return Func.jsonResult({"user": dt})
    except Exception as e:
        print(e)
        return Func.jsonResult({}, '用户不存在', 200000500)


@api.post('/user/info', tags=['用户'], description='用户信息', summary='用户信息')
async def userInfo(*, sign_in_user: dict = Depends(verifyToken)):
    """ 用token用户信息 """
    user_id = sign_in_user.get('user_id')
    _where = (WaUser.u_id == user_id)
    user_info = WaUser.select(WaUser.u_id,
                              WaUser.u_avatar, WaUser.u_phone,
                              WaUser.u_reg_time,
                              WaUserMembership.um_grade,
                              WaUserMembership.um_total_num,
                              WaUserMembership.um_rest_num,
                              WaUserMembership.um_expire_time).join(WaUserMembership,
                                                                    on=(WaUser.u_id == WaUserMembership.um_u_id)).where(
        _where).dicts()
    user_info = user_info[0]

    return Func.jsonResult(user_info)
