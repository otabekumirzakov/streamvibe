from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from database import Base, engine
from routers.films import film_router
from routers.users import user_router
from routers.wishlist import wishlist_router
from utils.slowapi_configuration import limiter

app = FastAPI(docs_url='/')

Base.metadata.create_all(bind=engine)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(user_router, tags=['Auth'], prefix='/auth')
app.include_router(film_router, tags=['Films'], prefix='/film')
app.include_router(wishlist_router, tags=['Wishlist'], prefix='/wishlist')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)