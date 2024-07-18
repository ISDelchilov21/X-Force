import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg.connect(f'dbname=postgres user={os.getenv("DB_USER")} password={os.getenv("DB_PASSWORD")} host={os.getenv("DB_HOST")} sslmode=require', row_factory=dict_row)
curr = conn.cursor()