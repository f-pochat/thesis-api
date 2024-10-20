from typing import Optional, Dict, Any, List

from src.logger import log
from src.modules.classes import models
from datetime import datetime

from src.db import get_db_connection


def save_class(class_data: models.ClassData):
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL query with RETURNING clause to get the auto-generated 'id' and other columns
    insert_query = """
        INSERT INTO class (date, classroom, audio, status)
        VALUES (%s, %s, %s, %s)
        RETURNING id, date, classroom, audio, status
    """

    # Execute the query and fetch the returned values
    cursor.execute(insert_query, (
        class_data.date,
        class_data.classroom,
        class_data.audio,
        'running'
    ))

    # Fetch the result from the query
    result = cursor.fetchone()

    # Commit the transaction and close the connection
    conn.commit()
    cursor.close()
    conn.close()

    result_dict = {
        "id": result[0],
        "date": datetime.strptime(result[1], '%Y-%m-%d %H:%M:%S+00'),
        "classroom": result[2],
        "audio": result[3]
    }

    # Return the saved object as a ClassData instance
    return models.ClassData.parse_obj(result_dict)


def save_processed_class(processed_class_data: models.ProcessedClass):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Define the insert query for processed_class
    insert_query = """
        INSERT INTO processed_class (class_id, audio_text, summary_text, embeddings)
        VALUES (%s, %s, %s, %s)
        RETURNING id, class_id, audio_text, summary_text
    """

    try:
        embeddings_as_tuple = tuple(processed_class_data.embeddings)

        cursor.execute(insert_query, (
            processed_class_data.class_id,
            processed_class_data.audio_text,
            processed_class_data.summary_text,
            embeddings_as_tuple
        ))

        result = cursor.fetchone()
        conn.commit()

        # Create a result dictionary
        result_dict = {
            "id": result[0],
            "class_id": result[1],
            "audio_text": result[2],
            "summary_text": result[3]
        }

        # Update the status to 'completed'
        update_status_query = """
            UPDATE classes
            SET status = 'completed'
            WHERE id = %s
        """
        cursor.execute(update_status_query, (processed_class_data.class_id,))
        conn.commit()

        # Return the saved object as a ClassData instance
        return models.ClassData.parse_obj(result_dict)

    except Exception as e:
        # If there was an error, update the status to 'failed'
        update_status_query = """
            UPDATE classes
            SET status = 'failed'
            WHERE id = %s
        """
        cursor.execute(update_status_query, (processed_class_data.class_id,))
        conn.commit()

        # Optionally log the error
        print(f"Error occurred: {str(e)}")

        # Optionally, re-raise the error or return None
        raise

    finally:
        # Ensure the connection is closed
        cursor.close()
        conn.close()


def failed_processing_class(class_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        update_status_query = """
                    UPDATE class
                    SET status = 'failed'
                    WHERE id = %s
                """
        cursor.execute(update_status_query, (class_id,))
        conn.commit()
    except Exception as e:
        log.error(f"Error occurred: {str(e)}")
        raise
    finally:
        # Ensure the connection is closed
        cursor.close()
        conn.close()


def get_full_class_data(class_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()

    # Define the SQL query with a join
    query = """
        SELECT 
            c.id AS class_id,
            c.date,
            c.classroom,
            c.audio,
            p.audio_text,
            p.summary_text
        FROM 
            classes c
        LEFT JOIN 
            processed_class p ON c.id = p.class_id
        WHERE 
            c.id = %s;
    """

    try:
        # Execute the query
        cursor.execute(query, (class_id,))
        result = cursor.fetchone()

        # Check if a result was returned
        if result:
            # Map the result to a dictionary
            keys = ['class_id', 'date', 'classroom', 'audio', 'audio_text', 'summary_text']
            return dict(zip(keys, result))
        else:
            return None  # No class found with that ID

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_classes(class_id: str) -> Optional[List[models.ClassData]]:
    conn = get_db_connection()
    cursor = conn.cursor()

    # Define the SQL query with a join
    query = """
        SELECT 
            c.id AS class_id,
            c.date,
            c.classroom,
            c.audio,
        FROM 
            classes c
    """

    try:
        # Execute the query
        cursor.execute(query, (class_id,))
        results = cursor.fetchall()

        # Map the results to a list of ClassData objects
        class_data_list = []
        for row in results:
            class_data = models.ClassData(
                id=row[0],  # class_id
                date=row[1],
                classroom=row[2],
                audio=row[3]
            )
            class_data_list.append(class_data)

        return class_data_list if class_data_list else None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
        conn.close()