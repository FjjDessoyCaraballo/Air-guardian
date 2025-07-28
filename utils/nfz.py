import os
from dotenv import load_dotenv
import psycopg

def authenticate(secret: str):
    if not secret or secret != os.environ["X-SECRET"]:
        return False
    return True

def retrieve_nfz_list():
	load_dotenv()
	connection_string = (
		f"host=localhost port=5432 "
		f"dbname={os.getenv('DB_NAME')} "
		f"user={os.getenv('DB_USER')} "
		f"password={os.getenv('DB_PASSWORD')}"
		)
	try:
		with psycopg.connect(connection_string) as conn:
			with conn.cursor() as cur:
				cur.execute('''SELECT * FROM nfz_offender ORDER BY time DESC;''')
				rows = cur.fetchall()
				columns = [desc[0] for desc in cur.description]
				result = [dict(zip(columns, row)) for row in rows]
		return result
	except psycopg.Error as e:
		print(f"Database error: {e}")
		return []
	except Exception as e:
		print(f"Unknown error: {e}")
		return []