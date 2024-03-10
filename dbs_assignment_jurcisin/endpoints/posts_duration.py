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
        WHERE ROUND(EXTRACT(EPOCH FROM (p.closeddate - p.creationdate)) / 60.0, 2) < %s
        ORDER BY p.closeddate DESC
        LIMIT %s;
    """, (duration, limit,))
    db_data = cursor.fetchall()
    cursor.close()
    connection.close()
    items = []
    for row in db_data:
        item = {
        "id": row[0],
        "creationdate": row[1],
        "viewcount": row[2],
        "lasteditdate": row[3],
        "lastactivitydate": row[4],
        "title": row[5],
        "closeddate": row[6],
        "duration": row[7]
        }
        items.append(item)

    return {"items": items}