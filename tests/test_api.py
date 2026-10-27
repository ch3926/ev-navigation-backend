from fastapi.testclient import TestClient # TestClient lets you test without runnin server!

from app.main import app


client = TestClient(app)

# can run this with pytest which auto finds files that have test_* or *_test

# check backend exists/running
def test_health_returns_200():
    response = client.get("/health")

    assert response.status_code == 200 # pytest will mark as failed if not receive this response
    assert response.json() == {"status": "ok"}

# check response for getting all stations
def test_stations_returns_200():
    response = client.get("/stations")

    assert response.status_code == 200

# test gotten stations have expected fieds
def test_stations_returns_station_data():
    response = client.get("/stations")
    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 5
    assert {
        "id",
        "name",
        "latitude",
        "longitude",
    } <= data[0].keys()

# check getting a specific station
def test_known_station_returns_correct_station():
    response = client.get("/stations/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert (
        response.json()["name"]
        == "Downtown Vancouver Charging Station"
    )

# test error when request an inexistent station
def test_unknown_station_returns_404():
    response = client.get("/stations/999999992222255555")

    assert response.status_code == 404
    assert response.json()["detail"] == "Station not found :("

# check post works with valid data
def test_reachable_stations_returns_200():
    request_data = { # data I'm sending to the test
        "latitude": 49.2827,
        "longitude": -123.1207,
        "remaining_range_km": 15,
    }

    response = client.post(
        "/reachable-stations", # send the request to the post endpt
        json=request_data, # as json
    )

    assert response.status_code == 200 # check if successful (with is code 200)

# check post returns correct stations so for the given stats, does it return stations 1-5?
def test_reachable_stations_returns_expected_stations():
    request_data = {
        "latitude": 49.2827,
        "longitude": -123.1207,
        "remaining_range_km": 15,
    }

    response = client.post(
        "/reachable-stations",
        json=request_data,
    )

    data = response.json()

    assert {
        station["id"]
        for station in data
    } == {1, 2, 3, 4, 5} # these 5 all reach

# test reachable stations sorted in ascending distances (close to far)
def test_reachable_stations_are_sorted_by_distance():
    request_data = {
        "latitude": 49.2827,
        "longitude": -123.1207,
        "remaining_range_km": 30,
    }

    response = client.post(
        "/reachable-stations",
        json=request_data,
    )

    data = response.json()

    distances = [
        station["distance_km"]
        for station in data
    ]

    assert distances == sorted(distances)

# test those ge, gt fields etc for valid input
def test_invalid_reachable_station_input_is_rejected():
    invalid_request_datas = [
        {
            "latitude": 91,
            "longitude": -123.1207,
            "remaining_range_km": 15,
        },
        {
            "latitude": 49.2827,
            "longitude": 181,
            "remaining_range_km": 15,
        },
        {
            "latitude": 49.2827,
            "longitude": -123.1207,
            "remaining_range_km": 0,
        },
        {
            "latitude": 49.2827,
            "longitude": -123.1207,
            "remaining_range_km": -10,
        },
    ]

    for request_data in invalid_request_datas:
        response = client.post(
            "/reachable-stations",
            json=request_data,
        )

        assert response.status_code == 422