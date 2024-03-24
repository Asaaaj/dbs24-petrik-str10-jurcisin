import psycopg2
from dbs_assignment_jurcisin.config import settings
from fastapi import APIRouter
router = APIRouter()

@router.get("/v3/users/{user_id}/badge_history")
async def posts(user_id: int):
    connection = psycopg2.connect(
        dbname=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, type, date, ROW_NUMBER() OVER (PARTITION BY type ORDER by date) AS position
        FROM (
            SELECT id, title, type, date,
                LEAD(type) OVER (ORDER BY date) AS next_type,
		        LAG(type) OVER (ORDER BY date) AS prev_type
            FROM (
                SELECT b.id, b.name AS title, 'badge' AS type, to_timestamp(to_char(b.date AT TIME ZONE 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'), 'YYYY-MM-DD"T"HH24:MI:SS.US"Z"') AS date
                FROM badges AS b
                WHERE b.userid = %s
                UNION
                SELECT p.id, p.title AS title, 'post' AS type, to_timestamp(to_char(p.creationdate AT TIME ZONE 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'), 'YYYY-MM-DD"T"HH24:MI:SS.US"Z"') AS date
                FROM posts AS p
                WHERE p.owneruserid = %s
		        ORDER BY date, id
            ) AS subquery
        ) AS subquery2
        WHERE type = 'post' AND next_type = 'badge' OR type = 'badge' AND prev_type = 'post'
        ORDER BY position, type DESC
    """, (user_id, user_id))

    items = []
    db_data = cursor.fetchall()
    cursor.close()
    connection.close()
    for row in db_data:
        item = {
            "id": row[0],
            "title": row[1],
            "type": row[2],
            "date": row[3],
            "position": row[4]
        }
        items.append(item)

    return {"items": items}
