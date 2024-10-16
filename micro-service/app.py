import mysql.connector
import os
from datetime import datetime, timedelta

def cleanup_temporary_posts():
    # Connect to the database
    conn = mysql.connector.connect(
        host=os.environ['DB_HOST'],
        port=int(os.environ['DB_PORT']),
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        database=os.environ['DB_NAME']
    )
    cursor = conn.cursor()

    delete_query = """
        DELETE FROM posts;
    """
    cursor.execute(delete_query)

    conn.commit()
    cursor.close()
    conn.close()

    print(f"Cleanup completed at {datetime.now()}")

if __name__ == "__main__":
    cleanup_temporary_posts()
