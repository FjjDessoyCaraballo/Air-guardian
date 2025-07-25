import psycopg
from dotenv import load_dotenv
import os

DB_PASSWORD = load_dotenv()
print(f'password for the db: {os.getenv('DB_PASSWORD')}')


def create_db():
	with psycopg.connect(f"dbname=nfz_list user=fdessoy- password=super_secret_password") as conn:
		with conn.cursor() as cur:
			cur.execute("""
			   CREATE TABLE nfz_offender (
			   		drone_id serial PRIMARY KEY,
			   		time timestamptz,
			   		position_x float,
   			   		position_y float,
			   		position_z float,
			   		first_name text,
			   		last_name text,
			   		social_security text,
			   		phone_number text
				)
				""")
			conn.commit()
			conn.close()
	return print("end of create_db")