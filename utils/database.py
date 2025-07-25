import psycopg
from dotenv import load_dotenv
import os
import time
import subprocess

load_dotenv()

def create_db():
	print(50*'*')
	print("Creating postgreSQL database...")
	print(50*'*')

	docker_cmd = (
		f"docker run -d --name airguardian-db "
		f"-e POSTGRES_DB={os.getenv('DB_NAME')} "
		f"-e POSTGRES_USER={os.getenv('DB_USER')} "
		f"-e POSTGRES_PASSWORD={os.getenv('DB_PASSWORD')} "
		f"-p 5432:5432 postgres:15 || docker start airguardian-db"
	)
		
	try:
		result = subprocess.run(
			docker_cmd, 
			shell=True, 
			check=True,
			capture_output=True,
			text=True
		)
		print("Docker container created/started successfully")
		print(result.stdout)
	except subprocess.CalledProcessError as e:
		print(f"Docker command failed: {e}")
		print(f"Error output: {e.stderr}")
		return False
	
	print(50*'*')
	time.sleep(5)  # Wait for PostgreSQL to start
	# Connection string using environment variables
	connection_string = (
		f"host=localhost port=5432 "
		f"dbname={os.getenv('DB_NAME')} "
		f"user={os.getenv('DB_USER')} "
		f"password={os.getenv('DB_PASSWORD')}"
	)
	
	try:
		with psycopg.connect(connection_string) as conn:
			with conn.cursor() as cur:
				# Check if table already exists
				cur.execute("""
					SELECT EXISTS (
						SELECT FROM information_schema.tables 
						WHERE table_name = 'nfz_offender'
					);
				""")
				table_exists = cur.fetchone()[0]
				
				if not table_exists:
					cur.execute("""
						CREATE TABLE nfz_offender (
							drone_id SERIAL PRIMARY KEY,
							time TIMESTAMPTZ,
							position_x FLOAT,
							position_y FLOAT,
							position_z FLOAT,
							first_name TEXT,
							last_name TEXT,
							social_security TEXT,
							phone_number TEXT
						)
					""")
					conn.commit()
					print("Table 'nfz_offender' created successfully")
				else:
					print("Table 'nfz_offender' already exists")
					
	except psycopg.Error as e:
		print(f"Database connection/operation failed: {e}")
		return False
	except Exception as e:
		print(f"Unexpected error: {e}")
		return False
		
	print("Database setup completed successfully")
	print("end of create_db")
	return True