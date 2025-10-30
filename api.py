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

app = FastAPI(
	title="Realtime Transit Data API"
)

load_dotenv()

MONGO_CONNECTION_STRING = f"mongodb://{os.getenv("MONGO_USER")}:{os.getenv("MONGO_PASSWORD")}@localhost:27017/"

client = AsyncMongoClient(MONGO_CONNECTION_STRING)

db = client["position"]
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
 
