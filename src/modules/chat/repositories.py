from typing import Optional, List

from src.db import get_db_connection
from src.logger import log


def get_processed_class(class_id: str) -> (Optional[List[float]], Optional[str]):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Define the SQL query with a join
    query = """
        SELECT 
            p.summary_text,
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


def get_most_relevant_embeddings(embedded_query: list[float], class_id: str) -> List[str] | None:
    conn = get_db_connection()
    cursor = conn.cursor()

    # Define the SQL query with a join
    query = """
            SELECT 
                id,
                content,
                1 - (embedding <=> %s::vector) AS cosine_similarity
            FROM 
                embeddings
            WHERE 
                class_id = %s
            ORDER BY cosine_similarity DESC LIMIT 5;
        """

    try:
        # Execute the query
        cursor.execute(query, (embedded_query, class_id,))
        result = cursor.fetchone()

        # Not related query
        if result[2] < 0.5:
            log.info(f"The query is not relevant for class {result[2]}")
            return None
        return result[1].tobytes().decode('utf-8')

    except Exception as e:
        log.error(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
