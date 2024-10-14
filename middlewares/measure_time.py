import logging
import time

from fastapi import Request

logger = logging.getLogger(__name__)


async def measure_time(request: Request, call_next):  # pragma: no cover
    '''
    This middleware measures and logs time taken by a request
    '''
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(
        f'Request: {request.url.path} - Time taken: {duration:.4f} seconds'
    )
    return response
