import psycopg
from dotenv import load_dotenv
import os
import time
import subprocess

DB_PASSWORD = load_dotenv()
print(f'password for the db: {os.getenv('DB_PASSWORD')}')


def create_db():

	print(50*'*')
	print("Creating postgreSQL database...")
	print(50*'*')
	subprocess.run(
            f"docker run -d --name airguardian-db -e POSTGRES_DB={os.getenv('DB_NAME')} -e POSTGRES_USER={os.getenv('DB_USER')} -e POSTGRES_PASSWORD={os.getenv('DB_PASSWORD')} -p 5436:5436 postgres:15 || docker start airguardian-db", 
            shell=True, 
            check=False,
            capture_output=True
        )
	print(50*'*')
	time.sleep(5)

	with psycopg.connect(f"host=localhost port=5436 dbname=nfz_list user=fdessoy- password={os.getenv('DB_PASSWORD')}") as conn:
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
	return print("end of create_db")