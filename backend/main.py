from fastapi import FastAPI
import uvicorn
from utils.logger import logger
import os
from fastapi.middleware.cors import CORSMiddleware
from routes.route import router

app = FastAPI()
logger.info('Starting API...')

# add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)



#include routs

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




if __name__=="__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)