import psycopg2
from dbs_assignment_jurcisin.config import settings
from fastapi import APIRouter, Query
router = APIRouter()

@router.get("/v3/tags/{tagname}/comments/{position}")
async def get_tag_comments_by_position(tagname: str, position: int, limit: int = Query(None)):

    connection = psycopg2.connect(
        dbname=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, displayname, body, text, score, %s AS position
        FROM (
            SELECT commentcount, id, displayname, body, text, score, ROW_NUMBER() OVER(ORDER BY creationdate ASC) AS row_num
            FROM (
                SELECT DISTINCT p.creationdate, p.commentcount, c.id, u.displayname, p.body, c.text, c.score
                FROM comments AS c
                JOIN users AS u ON c.userid = u.id
                JOIN posts AS p ON c.postid = p.id
                JOIN post_tags AS pt ON p.id = pt.post_id
                JOIN tags AS t ON pt.tag_id = t.id
                WHERE t.tagname = %s AND p.commentcount >= %s
            ) AS distinct_comments
        ) AS subquery
        WHERE row_num %% %s = 0
        LIMIT %s
    """, (position, tagname, position, position, limit))

    items = []
    db_data = cursor.fetchall()
    cursor.close()
    connection.close()
    for row in db_data:
        item = {
            "id": row[0],
            "displayname": row[1],
            "body": row[2],
            "text": row[3],
            "score": row[4],
            "position": row[5]
        }
        items.append(item)

    return {"items": items}

