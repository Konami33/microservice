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
