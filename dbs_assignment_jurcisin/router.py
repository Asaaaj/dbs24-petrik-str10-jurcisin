from fastapi import APIRouter

from dbs_assignment_jurcisin.endpoints.z1 import version

from dbs_assignment_jurcisin.endpoints.z2 import posts
from dbs_assignment_jurcisin.endpoints.z2 import tags
from dbs_assignment_jurcisin.endpoints.z2 import users
from dbs_assignment_jurcisin.endpoints.z2 import posts4_5

from dbs_assignment_jurcisin.endpoints.z3 import task_1
from dbs_assignment_jurcisin.endpoints.z3 import task_2
from dbs_assignment_jurcisin.endpoints.z3 import task_3
from dbs_assignment_jurcisin.endpoints.z3 import task_4


router = APIRouter()
router.include_router(version.router, tags=["version"])

router.include_router(posts.router, tags=["posts"])
router.include_router(users.router, tags=["users"])
router.include_router(tags.router, tags=["tags"])
router.include_router(posts4_5.router, tags=["get_posts"])

router.include_router(task_1.router)
router.include_router(task_2.router)
router.include_router(task_3.router)
router.include_router(task_4.router)
