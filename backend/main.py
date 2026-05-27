from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get('/')
async def index() -> dict:
    return{'message':'Hello'   }

@app.get('/health')
async def index() -> dict:
    return{'message':'Health'   }

@app.get('/api/chat')
async def index() -> dict:
    return{'message':'Chat'   }

if __name__=="__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)