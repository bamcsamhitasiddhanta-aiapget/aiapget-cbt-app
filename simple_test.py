import psycopg

conn = psycopg.connect(
    host="192.168.1.66",
    port=5432,
    dbname="myprojectdb",
    user="myappuser",
    password=input("Password: "),
    connect_timeout=5,
)

print("Connected!")
conn.close()
