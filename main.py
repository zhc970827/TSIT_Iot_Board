# coding=utf-8
# !/usr/bin/python -u
import codecs
import sys
import time

import uvicorn
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from appapi import api
from common.config import app_config

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

app = FastAPI(title='workapp',
              description='',
              version='1.0')


async def get_token_header(x_token: str = Header(...)):
    # 做权限鉴定
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# 静态文件指定目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 模板目录
templates = Jinja2Templates(directory="templates")

# 配置router
app.include_router(api, prefix='/api',
                   responses={404: {'description': "NOT FOUND"}})

# CORS跨域
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"], )

if __name__ == '__main__':
    uvicorn.run(main='app', reload=app_config.DEBUG,
                host="0.0.0.0", port=app_config.PORT)
