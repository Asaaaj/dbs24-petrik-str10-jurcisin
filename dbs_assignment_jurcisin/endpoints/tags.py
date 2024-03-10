import psycopg2
from dbs_assignment_jurcisin.config import settings
from fastapi import APIRouter
router = APIRouter()

@router.get("/v2/tags/{tag_name}/stats")
async def tags(tag_name: str):
    connection = psycopg2.connect(
        dbname=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT
    )

    cursor = connection.cursor()
    cursor.execute("""
    SELECT 
        json_build_object(
            'monday', COALESCE(monday_percentage, 0),
            'tuesday', COALESCE(tuesday_percentage, 0),
            'wednesday', COALESCE(wednesday_percentage, 0),
            'thursday', COALESCE(thursday_percentage, 0),
            'friday', COALESCE(friday_percentage, 0),
            'saturday', COALESCE(saturday_percentage, 0),
            'sunday', COALESCE(sunday_percentage, 0)
        ) AS result
    FROM (
        SELECT 
            ROUND(monday_tag_count * 100.0 / NULLIF(monday_count, 0), 2) AS monday_percentage,
            ROUND(tuesday_tag_count * 100.0 / NULLIF(tuesday_count, 0), 2) AS tuesday_percentage,
            ROUND(wednesday_tag_count * 100.0 / NULLIF(wednesday_count, 0), 2) AS wednesday_percentage,
            ROUND(thursday_tag_count * 100.0 / NULLIF(thursday_count, 0), 2) AS thursday_percentage,
            ROUND(friday_tag_count * 100.0 / NULLIF(friday_count, 0), 2) AS friday_percentage,
            ROUND(saturday_tag_count * 100.0 / NULLIF(saturday_count, 0), 2) AS saturday_percentage,
            ROUND(sunday_tag_count * 100.0 / NULLIF(sunday_count, 0), 2) AS sunday_percentage
        FROM (
            SELECT 
                (SELECT COUNT(*) FROM posts AS p WHERE EXTRACT(DOW FROM p.creationdate) = 1) AS monday_count,
                (SELECT COUNT(*) FROM posts AS p WHERE EXTRACT(DOW FROM p.creationdate) = 1 AND p.id IN 
                    (SELECT pt.post_id FROM tags AS t JOIN post_tags AS pt ON t.id = pt.tag_id WHERE t.tagname = '{tag_name}')) AS monday_tag_count,
                (SELECT COUNT(*) FROM posts AS p WHERE EXTRACT(DOW FROM p.creationdate) = 2) AS tuesday_count,
                (SELECT COUNT(*) FROM posts AS p WHERE EXTRACT(DOW FROM p.creationdate) = 2 AND p.id IN 
                    (SELECT pt.post_id FROM tags AS t JOIN post_tags AS pt ON t.id = pt.tag_id WHERE t.tagname = '{tag_name}')) AS tuesday_tag_count,
                (SELECT COUNT(*) FROM posts AS p WHERE EXTRACT(DOW FROM p.creationdate) = 3) AS wednesday_count,
                (SELECT COUNT(*) FROM posts AS p WHERE EXTRACT(DOW FROM p.creationdate) = 3 AND p.id IN 
                    (SELECT pt.post_id FROM tags AS t JOIN post_tags AS pt ON t.id = pt.tag_id WHERE t.tagname = '{tag_name}')) AS wednesday_tag_count,
                (SELECT COUNT(*) FROM posts AS p WHERE EXTRACT(DOW FROM p.creationdate) = 4) AS thursday_count,
                (SELECT COUNT(*) FROM posts AS p WHERE EXTRACT(DOW FROM p.creationdate) = 4 AND p.id IN 
                    (SELECT pt.post_id FROM tags AS t JOIN post_tags AS pt ON t.id = pt.tag_id WHERE t.tagname = '{tag_name}')) AS thursday_tag_count,
                (SELECT COUNT(*) FROM posts AS p WHERE EXTRACT(DOW FROM p.creationdate) = 5) AS friday_count,
                (SELECT COUNT(*) FROM posts AS p WHERE EXTRACT(DOW FROM p.creationdate) = 5 AND p.id IN 
                    (SELECT pt.post_id FROM tags AS t JOIN post_tags AS pt ON t.id = pt.tag_id WHERE t.tagname = '{tag_name}')) AS friday_tag_count,
                (SELECT COUNT(*) FROM posts AS p WHERE EXTRACT(DOW FROM p.creationdate) = 6) AS saturday_count,
                (SELECT COUNT(*) FROM posts AS p WHERE EXTRACT(DOW FROM p.creationdate) = 6 AND p.id IN 
                    (SELECT pt.post_id FROM tags AS t JOIN post_tags AS pt ON t.id = pt.tag_id WHERE t.tagname = '{tag_name}')) AS saturday_tag_count,
                (SELECT COUNT(*) FROM posts AS p WHERE EXTRACT(DOW FROM p.creationdate) = 0) AS sunday_count,
                (SELECT COUNT(*) FROM posts AS p WHERE EXTRACT(DOW FROM p.creationdate) = 0 AND p.id IN 
                    (SELECT pt.post_id FROM tags AS t JOIN post_tags AS pt ON t.id = pt.tag_id WHERE t.tagname = '{tag_name}')) AS sunday_tag_count
        ) AS days_counts
    ) AS sql_result;
    """)

    db_data = cursor.fetchall()
    cursor.close()
    connection.close()
    return {db_data}