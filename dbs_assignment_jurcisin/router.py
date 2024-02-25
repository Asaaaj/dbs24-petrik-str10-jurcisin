from fastapi import APIRouter

from dbs_assignment_jurcisin.endpoints import version

router = APIRouter()
router.include_router(version.router, tags=["version"])