"""
此软件包存储各类路由
"""
from .users import user_router
from .images import upload_router
from .lands import land_router

routers = [
    user_router,
    upload_router,
    land_router
]
