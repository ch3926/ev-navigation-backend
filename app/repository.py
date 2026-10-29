
# this file handles data access from sample data or DynamoDB
import logging
import os

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from app.data import STATIONS

logger = logging.getLogger(__name__)

# Custom exception for errors accessing station data
class StationRepositoryError(Exception):
    """Raised when station storage cannot be accessed."""
    pass


def _backend(): # check if should use sample for local tests or DynamoDB data, sample by default
    mode = os.getenv("STATIONS_BACKEND", "sample")

    if mode not in ("sample", "dynamodb"):
        raise StationRepositoryError("Invalid storage backend")

    return mode


# creates the stations table object that my code can interact with
def _table(): # get ref to DynamoDB table
    dynamodb = boto3.resource("dynamodb")
    table_name = os.environ["STATIONS_TABLE"]
    table = dynamodb.Table(table_name)
    return table


# Convert DynamoDB records to normal Python dicts.
def _normalize(item):
    return {
        "id": int(item["id"]),
        "name": item["name"],
        "latitude": float(item["latitude"]),
        "longitude": float(item["longitude"]),
    }


def get_station_by_id(station_id):

    # do if using sample data
    if _backend() == "sample":
        for station in STATIONS:
            if station["id"] == station_id:
                return station
        return None

    try: # now for DynamoDB
        table = _table()
        response = table.get_item(Key={"id": station_id})
        item = response.get("Item")

    except (ClientError, BotoCoreError, KeyError) as exc:
        logger.exception("DynamoDB GetItem failed")
        raise StationRepositoryError(
            "Database read failed"
        ) from exc

    if item is None:
        return None

    return _normalize(item)


def list_stations():
    if _backend() == "sample":
        return STATIONS

    try:
        table = _table()
        items = []
        last_key = None

        while True:
            if last_key is None:
                response = table.scan()
            else:
                response = table.scan(ExclusiveStartKey=last_key)

            page_items = response.get("Items", [])
            items.extend(page_items)

            last_key = response.get("LastEvaluatedKey")
            if not last_key:
                break

    except (ClientError, BotoCoreError, KeyError) as exc:
        logger.exception("DynamoDB Scan failed")
        raise StationRepositoryError(
            "Database read failed"
        ) from exc

    stations = []

    for item in items:
        station = _normalize(item)
        stations.append(station)

    return sorted(stations, key=lambda station: station["id"]) # sort by id
