from fastapi import APIRouter

from dbs_assignment_jurcisin.endpoints import version
from dbs_assignment_jurcisin.endpoints import posts
from dbs_assignment_jurcisin.endpoints import tags
from dbs_assignment_jurcisin.endpoints import posts_duration
from dbs_assignment_jurcisin.endpoints import posts_query


router = APIRouter()
router.include_router(version.router, tags=["version"])
router.include_router(posts.router, tags=["posts"])
router.include_router(tags.router, tags=["tags"])
router.include_router(posts_duration.router, tags=["posts_duration"])
router.include_router(posts_query.router, tags=["posts_query"])