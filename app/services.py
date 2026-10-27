from math import asin, cos, radians, sin, sqrt


EARTH_RADIUS_KM = 6371.0


def haversine_distance_km(
    latitude_1,
    longitude_1,
    latitude_2,
    longitude_2,
):
    lat1 = radians(latitude_1)
    lon1 = radians(longitude_1)
    lat2 = radians(latitude_2)
    lon2 = radians(longitude_2)

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = (
        sin(delta_lat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(delta_lon / 2) ** 2
    )

    c = 2 * asin(sqrt(a))

    return EARTH_RADIUS_KM * c


def find_reachable_stations(
    latitude,
    longitude,
    remaining_range_km,
    stations,
):
    reachable = []

    for station in stations:
        distance = haversine_distance_km(
            latitude,
            longitude,
            station["latitude"],
            station["longitude"],
        )

        if distance <= remaining_range_km:
            reachable.append(
                {
                    **station,
                    "distance_km": distance,
                }
            )

    reachable.sort(
        key=lambda station: station["distance_km"]
    )

    for station in reachable:
        station["distance_km"] = round(
            station["distance_km"],
            2,
        )

    return reachable