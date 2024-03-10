import psycopg2
from dbs_assignment_jurcisin.config import settings
from fastapi import APIRouter
router = APIRouter()

@router.get("/v2/posts/?limit={limit}&query={query}")
async def posts_limit(limit: int, query: str):
    connection = psycopg2.connect(
        dbname=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT
    )

    cursor = connection.cursor()
    cursor.execute("""
        SELECT p.id, p.creationdate, p.viewcount, p.lasteditdate, p.title, p.body, p.answercount, p.closeddate,
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
            "title": row[4],
            "body": row[5],
            "answercount": row[6],
            "closeddate": row[7],
            "tags": row[8]
        }
        items.append(item)
    
    return {"items": items}