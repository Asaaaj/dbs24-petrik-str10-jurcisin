import psycopg2
from dbs_assignment_jurcisin.config import settings
from fastapi import APIRouter, Query
router = APIRouter()

@router.get("/v3/tags/{tag}/comments")
async def get_tag_comments(tag: str, count: int = Query(None)):
    connection = psycopg2.connect(
        dbname=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT
    )

    cursor = connection.cursor()
    cursor.execute("""
        SELECT post_id, title, displayname, text, post_created_at, created_at, diff,
            AVG(CASE WHEN diff IS NOT NULL THEN diff END) OVER (PARTITION BY post_id ORDER BY created_at ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS avg
        FROM(
            SELECT post_id, title, displayname, text, post_created_at, created_at,
                CASE 
                    WHEN diff IS NULL THEN (created_at - post_created_at)
                    ELSE diff 
                    END AS diff
            FROM(
                SELECT post_id, title, displayname, text, post_created_at, created_at,
                (created_at - LAG(created_at) OVER (PARTITION BY post_id ORDER BY created_at)) AS diff
                FROM (
                    SELECT DISTINCT p.id AS post_id, p.title, u.displayname, c.text, 
                        to_timestamp(to_char(p.creationdate AT TIME ZONE 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'), 'YYYY-MM-DD"T"HH24:MI:SS.US"Z"') AS post_created_at,
                        to_timestamp(to_char(c.creationdate AT TIME ZONE 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'), 'YYYY-MM-DD"T"HH24:MI:SS.US"Z"') AS created_at
                    FROM comments AS c
                    JOIN users AS u ON c.userid = u.id
                    JOIN posts AS p ON c.postid = p.id
                    JOIN post_tags AS pt ON p.id = pt.post_id
                    JOIN tags AS t ON pt.tag_id = t.id
                    WHERE t.tagname = %s AND p.commentcount > %s
                    ORDER BY created_at ASC
                ) AS subquery
            ) AS subquery2
        ) AS subquery3
    """, (tag, count))

    items = []
    db_data = cursor.fetchall()
    cursor.close()
    connection.close()
    for row in db_data:
        item = {
            "post_id": row[0],
            "title": row[1],
            "displayname": row[2],
            "text": row[3],
            "post_created_at": row[4],
            "created_at": row[5],
            "diff": row[6],
            "avg": row[7]
        }
        items.append(item)

    return {"items": items}
