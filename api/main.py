import uvicorn
from fastapi import FastAPI

from api.utils import Const
from routers import routers

app = FastAPI()

# 将已写接口路由接入程序
for router in routers:
    app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(app='main:app', host=Const.PUBLIC_HOST, port=Const.PORT, reload=True, debug=Const.debug)
