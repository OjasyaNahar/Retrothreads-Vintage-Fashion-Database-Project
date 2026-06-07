import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Riya@10550",
        database="retrothreads_group30"
    )

print("Database connected successfully!")