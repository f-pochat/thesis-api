from typing import Optional, List

from src.db import get_db_connection
from src.logger import log


def get_embeddings(class_id: str) -> (Optional[List[float]], Optional[str]):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Define the SQL query with a join
    query = """
        SELECT 
            p.embeddings,
            p.audio_text
        FROM 
            class c
        LEFT JOIN 
            processed_class p ON c.id = p.class_id
        WHERE 
            c.id = %s;
    """

    try:
        # Execute the query
        cursor.execute(query, (class_id,))
        result = cursor.fetchone()

        return result

    except Exception as e:
        log.error(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
        conn.close()