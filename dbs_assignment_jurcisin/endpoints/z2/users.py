import psycopg2
from dbs_assignment_jurcisin.config import settings
from fastapi import APIRouter
router = APIRouter()

@router.get("/v2/users/{user_id}/friends")
async def users(user_id: int):
    connection = psycopg2.connect(
        dbname=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT
    )

    cursor = connection.cursor()
    cursor.execute("""
        SELECT u.id, u.reputation, u.creationdate, u.displayname, u.lastaccessdate,
           u.websiteurl, u.location, u.aboutme, u.views, u.upvotes, u.downvotes,
           u.profileimageurl, u.age, u.accountid
        FROM users AS u
        JOIN posts AS p ON p.owneruserid = %s
        JOIN comments AS c ON c.postid = p.id AND u.id = c.userid
        UNION
        SELECT u.id, u.reputation, u.creationdate, u.displayname, u.lastaccessdate,
           u.websiteurl, u.location, u.aboutme, u.views, u.upvotes, u.downvotes,
           u.profileimageurl, u.age, u.accountid
        FROM users AS u
        JOIN comments AS c ON c.userid = u.id
        WHERE c.postid IN (
            SELECT postid
            FROM comments
            WHERE userid = %s
        )
        ORDER BY creationdate ASC;
    """, (user_id, user_id,))
    db_data = cursor.fetchall()
    cursor.close()
    connection.close()
    items = []
    for row in db_data:
        item = {
                "id": row[0],
                "reputation": row[1],
                "creationdate": row[2].isoformat() if row[2] else None,
                "displayname": row[3],
                "lastaccessdate": row[4].isoformat() if row[4] else None,
                "websiteurl": row[5],
                "location": row[6],
                "aboutme": row[7],
                "views": row[8],
                "upvotes": row[9],
                "downvotes": row[10],
                "profileimageurl": row[11],
                "age": row[12],
                "accountid": row[13]
            }
        items.append(item)

    return {"items": items}