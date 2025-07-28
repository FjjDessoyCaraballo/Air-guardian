from fastapi import HTTPException, APIRouter
from dotenv import load_dotenv
from utils.drones import violated_drones, append_owner_details
import requests
import psycopg
import asyncio
import os

drones_route = APIRouter()

@drones_route.get("/drones")
def drones():
	url = os.environ["DRONES_API_BASE_URL"] + "drones"
	res = requests.get(url)
	if res.status_code != 200:
		# log error
		return HTTPException(500, "Internal server error")

	try:
		body = res.json()
	except:
		# log error
		return HTTPException(500, "Internal server error")

	drones = violated_drones(body)
	if drones:
		if not append_owner_details(drones):
			return HTTPException(500, "Internal server error")
		print(50*'*')
		print('** violation detected ***')
		print(drones)
		print(50*'*')
		success = list_offender(drones)
		if success:
			print('** Offender added to list ***')
		else:
			print('** Failed to insert to list ***')
		print(50*'*')

		#update db
	return body

def list_offender(drones_list):
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
				for drone in drones_list:
					cur.execute('''
						INSERT INTO nfz_offender (
							time, drone_uuid, position_x, position_y, position_z,
							first_name, last_name, social_security, phone_number
					) VALUES (
						NOW(), %s, %s, %s, %s, %s, %s, %s
					) ON CONFLICT (social_security_number) DO UPDATE SET
						time = NOW(),
						position_x = EXCLUDED.position_x,
						position_y = EXCLUDED.position_y,
						position_z = EXCLUDED.position_z
					''', (
						drone['id'],
						drone['x'],
						drone['y'],
						drone['z'],
						drone['first_name'],
						drone['last_name'],
						drone['social_security_number'],
						drone['phone_number'],
					)) #here are the values coming from drone
				conn.commit()
	except psycopg.Error as e:
		print(f'Database insertion failed: {e}')
		return False
	except Exception as e:
		print(f'Unknown exception: {e}')
		return False
	return True



""" 

EXAMPLE OF DATA

[{'id': '0489ac58-4213-49ac-a0da-eae25a91de0e', 
'owner_id': 3, 
'x': -613, 
'y': 307, 
'z': 143, 
'first_name': 'Juha', 
'last_name': 'Korhonen', 
'social_security_number': '100119-3437', 
'phone_number': '+358409876543'}, 


{'id': '427a2d29-48ff-48b6-9ef8-2b092ceaed77', 
'owner_id': 27, 
'x': -655, 
'y': -86, 
'z': 191, 
'first_name': 'Risto', 
'last_name': 'Mäkelä', 
'social_security_number': '180619-545X', 
'phone_number': '+358404567890'}]

"""