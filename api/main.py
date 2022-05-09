import uvicorn
from fastapi import FastAPI

from api.utils import Const
from routers import user_router, upload_route

app = FastAPI()

# 将已写接口路由接入程序
app.include_router(user_router)
app.include_router(upload_route)

if __name__ == '__main__':
    uvicorn.run(app='main:app', host=Const.PUBLIC_HOST, port=Const.PORT, reload=True, debug=Const.debug)
