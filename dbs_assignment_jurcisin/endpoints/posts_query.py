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
        WHERE p.title ILIKE '%{query}%' OR p.body ILIKE '%{query}%' 
        ORDER BY p.creationdate DESC
        LIMIT {limit};
    """)
    db_data = cursor.fetchall()
    cursor.close()
    connection.close()
    return {"items": db_data}