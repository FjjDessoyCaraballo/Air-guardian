from pydantic import BaseModel

class Drone(BaseModel):
	id: str
	owner_id: int
	x: int
	y: int
	z: int

class Health(BaseModel):
	status: str
