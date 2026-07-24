from fastapi import FastAPI
import uvicorn
from utils.logger import logger
import os
from fastapi.middleware.cors import CORSMiddleware
from routes.route import router
from routes.auth_route import router as auth_router
from routes.conversation_route import router as conversation_router
from routes.admin_route import router as admin_router
from routes.analytics_route import router as analytics_router
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from secure import Secure


app = FastAPI()

secure_headers = Secure()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


logger.info('Starting API...')

app.include_router(
    analytics_router
)

app.include_router(admin_router)
app.include_router(auth_router)

# add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)



#include routs

app.include_router(
    conversation_router
)

app.include_router(router)

@app.get('/')
async def index() -> dict:
    return{
        'message':'Hello'   
        }
                 
@app.get('/health')
async def health() -> dict:
    return{
        'message':'Health'  
          }


@app.middleware("http")
async def add_secure_headers(request, call_next):

    response = await call_next(request)

    secure_headers.framework.fastapi(response)

    return response



if __name__=="__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)