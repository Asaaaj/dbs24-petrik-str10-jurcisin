import psycopg2
from dbs_assignment_jurcisin.config import settings
from fastapi import APIRouter, Query
router = APIRouter()

@router.get("/v3/posts/{postid}")
async def get_post(postid: int, limit: int = Query(None)):

    connection = psycopg2.connect(
        dbname=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT
    )

    cursor = connection.cursor()
    cursor.execute("""
        SELECT u.displayname, p.body, p.creationdate AT TIME ZONE 'UTC' AS created_at 
        FROM posts AS p 
        JOIN users AS u ON u.id = p.owneruserid
        WHERE p.id = %s OR p.parentid = %s 
        ORDER BY p.creationdate ASC 
        LIMIT %s
    """, (postid, postid, limit))

    items = []
    db_data = cursor.fetchall()
    cursor.close()
    connection.close()
    for row in db_data:
        item = {
            "displayname": row[0],
            "body": row[1],
            "created_at": row[2]
        }
        items.append(item)

    return {"items": items}
