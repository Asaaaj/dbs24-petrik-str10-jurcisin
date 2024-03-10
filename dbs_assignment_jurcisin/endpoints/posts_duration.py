import psycopg2
from dbs_assignment_jurcisin.config import settings
from fastapi import APIRouter
router = APIRouter()

@router.get("/v2/posts/?duration={duration}&limit={limit}")
async def posts_duration(duration: int, limit: int):
    connection = psycopg2.connect(
        dbname=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT
    )

    cursor = connection.cursor()
    cursor.execute("""
        SELECT p.id, p.creationdate, p.viewcount, p.lasteditdate, p.lastactivitydate, p.title, p.closeddate,
            ROUND(EXTRACT(EPOCH FROM (p.closeddate - p.creationdate)) / 60.0, 2) AS duration
        FROM posts AS p
        WHERE ROUND(EXTRACT(EPOCH FROM (p.closeddate - p.creationdate)) / 60.0, 2) < {duration}
        ORDER BY p.closeddate DESC
        LIMIT {limit};
    """)
    db_data = cursor.fetchall()
    cursor.close()
    connection.close()
    return {"items": db_data}