For this task, I would break down the task into these steps. First I'll use Python and Kubernetes' CronJob to schedule the cleanup operation, as Python is straightforward for such tasks and Kubernetes provides built-in mechanisms for periodic jobs. Here is the breakdown:


1. Microservice:

This Python script connects to a MySQL database and deletes all the records from the posts table.

How it works:

It connects to the MySQL database using credentials provided as environment variables.
The script executes a DELETE query to remove all records from the posts table.
After deleting the data, it closes the database connection.

Here is the code:

```python
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
```

2. Dockerfile:

```Dockerfile
FROM python:3.9-slim

ENV DB_HOST="localhost"        
ENV DB_PORT=3306
ENV DB_USER="username"            
ENV DB_PASSWORD="password"        
ENV DB_NAME="mydatabase"          

WORKDIR /app

COPY . /app

RUN pip install mysql-connector-python

CMD ["python", "app.py"]
```

3. Kubernetes CronJob

Goal: Schedule the Python microservice to run automatically every hour in a Kubernetes cluster.

How it works:
A Kubernetes CronJob schedules and runs a job at a specified interval (in this case, every hour).
It pulls the Docker image of the Python microservice and runs the script inside a container.
The CronJob specifies the environment variables (DB_HOST, DB_PORT, etc.) for the MySQL connection.

Here is the YAML for the CronJob:

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: cleanup-temp-posts
spec:
  schedule: "0 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: cleanup-temp-posts
            image: konami98/micro:latest
            env:
            - name: DB_HOST
              value: "mysql"
            - name: DB_PORT
              value: "3306"
            - name: DB_USER
              value: "username"
            - name: DB_PASSWORD
              value: "password"
            - name: DB_NAME
              value: "mydatabase"
          restartPolicy: OnFailure
```

For detailed information here is the link to the repository:

https://github.com/Konami33/microservice