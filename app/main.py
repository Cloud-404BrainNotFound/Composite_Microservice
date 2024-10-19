from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models
from app.database import engine, get_db
from app.models import review, user, order, payment, notification  # 导入所有模型
from app.routers.user_service import user_router  # 导入用户相关的 router
from app.dependecies.log import setup_logger
from app.dependecies.logging_middleware import logging_dependency

# 创建数据库表
review.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)
order.Base.metadata.create_all(bind=engine)
payment.Base.metadata.create_all(bind=engine)
notification.Base.metadata.create_all(bind=engine)

logger = setup_logger()

app = FastAPI()

app.middleware("http")(logging_dependency)


# 这是一个router的示例
app.include_router(user_router, prefix="/users", tags=["users"])

@app.get("/")
def read_root():
    return {"Hello": "World"}