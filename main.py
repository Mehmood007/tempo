import logging
from contextlib import asynccontextmanager

from decouple import config
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from database import init_database
from middlewares.measure_time import measure_time
from middlewares.rate_limit import rate_limit_middleware
from routes import auth, cities, friends, search, users

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS configuration
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],  # Allows all methods (GET, POST, etc.)
    allow_headers=['*'],  # Allows all headers
)


@app.middleware('http')
async def rate_limit(request: Request, call_next):  # pragma: no cover
    return await rate_limit_middleware(request, call_next)


@app.middleware('http')
async def log_time(request: Request, call_next):  # pragma: no cover
    return await measure_time(request, call_next)


@asynccontextmanager
async def lifespan(app: FastAPI):  # pragma: no cover
    await init_database(app)
    redis = aioredis.from_url(config('REDIS_URL'))
    FastAPICache.init(RedisBackend(redis), prefix='tempo-api-cache')

    yield


app = FastAPI(lifespan=lifespan)


@app.get('/', include_in_schema=False)
async def health_check():
    '''
    Root Route
    Description: This route is used to check if API is up and running
    '''
    return {
        'status': 'ok',
        'description': 'Health check API endpoint is working fine',
    }


# All routes need to be registered here
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(cities.router)
app.include_router(friends.router)
app.include_router(search.router)
