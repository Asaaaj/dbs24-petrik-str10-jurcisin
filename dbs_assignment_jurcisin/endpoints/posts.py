import psycopg2
from dbs_assignment_jurcisin.config import settings
from fastapi import APIRouter
router = APIRouter()

@router.get("/v2/posts/{post_id}/users")
async def posts(post_id: int):
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
        JOIN comments AS c ON c.userid = u.id
        WHERE c.postid = {post_id}
        ORDER BY c.creationdate DESC
    """)    
    db_data = cursor.fetchall()
    cursor.close()
    connection.close()
    return {"items": db_data}