from fastapi import FastAPI
import uvicorn
from utils.logger import logger
from fastapi.middleware.cors import CORSMiddleware
from routes.route import router
from routes.auth_route import router as auth_router
from routes.conversation_route import router as conversation_router
from routes.admin_route import router as admin_router
from routes.analytics_route import router as analytics_router
from slowapi.middleware import SlowAPIMiddleware
from secure import Secure
from limiter import limiter

app = FastAPI(title="AI Customer Support Chatbot")

secure_headers = Secure()

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://nlp-chatbot-frontend.vercel.app",
        "https://nlp-chatbot-tsdj.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info('Starting API...')

app.include_router(analytics_router)
app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(conversation_router)
app.include_router(router)


@app.get('/')
async def index() -> dict:
    return {'message': 'Hello'}


@app.get('/health')
async def health() -> dict:
    return {'message': 'Health'}


@app.middleware("http")
async def add_secure_headers(request, call_next):
    response = await call_next(request)
    await secure_headers.set_headers_async(response)
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
