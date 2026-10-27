from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.data import STATIONS
from app.services import find_reachable_stations


app = FastAPI(
    title="EV Charging Station API",
    version="1.0.0",
)

# defines what fields and types the client must send when POSTing
class ReachableStationsRequest(BaseModel):
    latitude: float = Field( # -90 <= latitude <= 90
        ge=-90, # ge, le, gt are pydantic syntax
        le=90,
    )
    longitude: float = Field(
        ge=-180,
        le=180,
    )
    remaining_range_km: float = Field(
        gt=0,
    )

# endpoints below! ------

@app.get("/health") # check backend is up an running
def health():
    return {"status": "ok"}


@app.get("/stations") # run the function that spits out the available stations
def get_stations():
    return STATIONS


@app.get("/stations/{station_id}")
def get_station(station_id: int):
    station = None

    for s in STATIONS:
        if s["id"] == station_id:
            station = s
            break

    if station is None:
        raise HTTPException(
            status_code=404,
            detail="Station not found :(",
        )

    return station


@app.post("/reachable-stations")
def reachable_stations(
    request: ReachableStationsRequest, # the basemodel from earlier
):
    return find_reachable_stations( # function that calculates reachable stations located inside services.py
        request.latitude,
        request.longitude,
        request.remaining_range_km,
        STATIONS,
    )