from fastapi import APIRouter

from dbs_assignment_jurcisin.endpoints import version
from dbs_assignment_jurcisin.endpoints import posts
from dbs_assignment_jurcisin.endpoints import tags
from dbs_assignment_jurcisin.endpoints import users
from dbs_assignment_jurcisin.endpoints import posts4_5


router = APIRouter()
router.include_router(version.router, tags=["version"])
router.include_router(posts.router, tags=["posts"])
router.include_router(users.router, tags=["users"])
router.include_router(tags.router, tags=["tags"])
router.include_router(posts4_5.router, tags=["get_posts"])