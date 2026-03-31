from pymongo import AsyncMongoClient
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
import os
from dotenv import load_dotenv
from typing import Optional, List
from typing_extensions import Annotated
import datetime

from fastapi.staticfiles import StaticFiles

app = FastAPI(
	title="Realtime Transit Dashboard API"
)

load_dotenv()

MONGO_USER = os.getenv("MONGO_USER", "root")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "example")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DB = os.getenv("MONGO_DB", "position")

if os.getenv("MONGO_CONNECTION_STRING"):
	MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
else:
	MONGO_CONNECTION_STRING = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"

client = AsyncMongoClient(MONGO_CONNECTION_STRING)

db = client[MONGO_DB]
collection = db.get_collection("vehicle")

PyObjectId = Annotated[str, BeforeValidator(str)]

BASE_MODEL_CONFIG = ConfigDict(
	populate_by_name=True,
	arbitrary_types_allowed=True,
)

# Innermost vehicle object
class VehicleIdentity(BaseModel):
	id: str
	label: str
	model_config = BASE_MODEL_CONFIG

# Position object
class Position(BaseModel):
	latitude: float
	longitude: float
	model_config = BASE_MODEL_CONFIG

# Trip object
class Trip(BaseModel):
	tripId: str
	startDate: str
	scheduleRelationship: str
	routeId: str
	route_name: Optional[str] = None
	directionId: int
	model_config = BASE_MODEL_CONFIG

# Main 'vehicle' data object
class VehicleDetails(BaseModel):
	trip: Trip
	position: Position
	currentStopSequence: int
	currentStatus: str
	timestamp: str  # Timestamp is a string in the input
	stopId: str
	vehicle: VehicleIdentity
	model_config = BASE_MODEL_CONFIG

# The root model
class VehicleUpdate(BaseModel):
	id: str
	vehicle: VehicleDetails
	# Use 'alias' to handle the field name '_id' 
	# which is awkward in Python.
	mongo_id: PyObjectId = Field(alias='_id')
	timestamp: datetime
	model_config = BASE_MODEL_CONFIG

@app.get(
    "/api/vehicles/",
    response_model=List[VehicleUpdate],
    summary="Get All Vehicle Positions",
    description="Retrieves a list of all current vehicle position documents from the database."
)
async def get_all_vehicles():
	"""
	Fetches all documents from the 'vehicle' collection.
	
	The route uses an async cursor to iterate over all documents
	and returns them as a list. FastAPI automatically serializes
	the MongoDB documents into the `VehicleUpdate` response model.
	"""
	vehicles = []
	try:
		cursor = collection.find({})
		async for document in cursor:
			vehicles.append(document)
   
		print('{vehicles=}')
		
		if not vehicles:
			raise HTTPException(status_code=404, detail="No vehicles found")
			
		return vehicles
	except Exception as e:
		# Log the error for debugging
		print(f"Error fetching vehicles: {e}")
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail=f"An error occurred while fetching vehicle data: {e}"
		)

# Mount the static files from the built frontend
# In production, this will serve the React app
#if os.path.exists("frontend/dist"):
# 	app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")
 
