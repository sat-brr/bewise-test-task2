import settings
import uvicorn
from fastapi import APIRouter, FastAPI

from app.api.record_handler import record_router
from app.api.user_handler import user_router

app = FastAPI()
main_router = APIRouter()

main_router.include_router(user_router, prefix='/user', tags=['user'])
main_router.include_router(record_router, prefix='/record', tags=['record'])

app.include_router(main_router)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=settings.APP_PORT)
