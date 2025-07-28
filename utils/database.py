import psycopg
from dotenv import load_dotenv
import os
import time
import subprocess
import logging

load_dotenv()
logger = logging.getLogger(__name__)

def create_db():
	"""
	This function is responsible for the initial creation of the database and set up. The database 
	is created within a container that can be communicated through port 5432. The database name, user,
	and password must be provided through the environment variable `.env`. If you do not know how to
	make your own environment variable, there is an `.env.example` that you can follow.
	"""
	logger.info(50*'*')
	logger.info("Creating postgreSQL database...")
	logger.info(50*'*')

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
		logger.info("Docker container created/started successfully")
		logger.info(result.stdout)
	except subprocess.CalledProcessError as e:
		logger.error(f"Docker command failed: {e}")
		logger.error(f"Error output: {e.stderr}")
		return False
	
	logger.info(50*'*')
	time.sleep(5)
	connection_string = (
		f"host=localhost port=5432 "
		f"dbname={os.getenv('DB_NAME')} "
		f"user={os.getenv('DB_USER')} "
		f"password={os.getenv('DB_PASSWORD')}"
	)

	try:
		with psycopg.connect(connection_string) as conn:
			with conn.cursor() as cur:
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
							id SERIAL PRIMARY KEY,
							drone_uuid TEXT UNIQUE NOT NULL,
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
					logger.info("Table 'nfz_offender' created successfully")
				else:
					logger.info("Table 'nfz_offender' already exists")
					
	except psycopg.Error as e:
		logger.error(f"Database connection/operation failed: {e}")
		return False
	except Exception as e:
		logger.error(f"Unexpected error: {e}")
		return False
		
	logger.info("Database setup completed successfully")
	return True