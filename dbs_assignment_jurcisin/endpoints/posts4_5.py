import psycopg2
from dbs_assignment_jurcisin.config import settings
from fastapi import APIRouter, Query
router = APIRouter()

@router.get("/v2/posts/")
async def get_posts(limit: int = Query(None), query: str = Query(None), duration: int = Query(None)):
    connection = psycopg2.connect(
        dbname=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT
    )

    if query is not None:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT p.id, p.creationdate, p.viewcount, p.lasteditdate, p.title, p.body, p.answercount, p.closeddate, p.lastactivitydate
            (SELECT STRING_AGG(t.tagname, ', ') 
            FROM post_tags AS pt 
            JOIN tags AS t ON pt.tag_id = t.id 
            WHERE pt.post_id = p.id) AS tags
            FROM posts AS p
            WHERE p.title ILIKE %s OR p.body ILIKE %s 
            ORDER BY p.creationdate DESC
            LIMIT %s;
            """, ('%' + query + '%', '%' + query + '%', limit,))
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
            "lastactivitydate": row[8],
            "title": row[4],
            "body": row[5],
            "answercount": row[6],
            "closeddate": row[7],
            "tags": row[9]
            }
            items.append(item)
        return {"items": items}
    elif duration is not None:
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
    else: 
        return {"Null"}