import logging

from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)


async def rate_limit_middleware(
    request: Request, call_next
):  # pragma: no cover
    '''
    Rate limit middleware
    '''
    await limiter.limit('120/minute')(request)
    return await call_next(request)
