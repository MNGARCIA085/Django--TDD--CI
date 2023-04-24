import json

import pytest

from automotive.models import Car





@pytest.mark.django_db
def test_add_car_invalid_json(client):
    cars = Car.objects.all()
    assert len(cars) == 0

    resp = client.post(
        "/automotive/api/",
        {},
        content_type="application/json"
    )
    assert resp.status_code == 400

    movies = Car.objects.all()
    assert len(movies) == 0



@pytest.mark.django_db
def test_add_car(client):
    cars = Car.objects.all()
    assert len(cars) == 0

    resp = client.post(
        "/automotive/api/",
        {
            "marca": "Ferrari",
            "modelo": "Maranello",
        },
        content_type="application/json"
    )
    assert resp.status_code == 201
    assert resp.data["marca"] == "Ferrari"

    movies = Car.objects.all()
    assert len(movies) == 1




# fixture para testear get cars


@pytest.fixture(scope='function')
def add_car():
    def _add_car(marca, modelo):
        car = Car.objects.create(marca=marca, modelo=modelo)
        return car
    return _add_car



# get individual cars
@pytest.mark.django_db
def test_get_single_car(client, add_car):
    car = add_car(marca="Ferrari", modelo='Maranello')
    resp = client.get(f"/automotive/api/{car.id}/")
    assert resp.status_code == 200
    assert resp.data["marca"] == "Ferrari"


def test_get_single_car_incorrect_id(client):
    resp = client.get(f"/automotive/api/foo/")
    assert resp.status_code == 404



# get all cars
@pytest.mark.django_db
def test_get_all_movies(client, add_car):
    car_one = add_car(marca='Ferrari', modelo='1')
    car_two = add_car(marca='Lambo',modelo='2')
    resp = client.get(f"/automotive/api/")
    assert resp.status_code == 200
    assert resp.data[0]["marca"] == car_one.marca
    assert resp.data[1]["marca"] == car_two.marca



# edit a car
@pytest.mark.django_db
def test_get_all_cars(client, add_car):
    car = add_car(marca='Ferrari', modelo='1')
    resp = client.put(
                f"/automotive/api/{car.id}/",
                {
                    "marca": "Tesla",
                    "modelo": "Maranello",
                },
                content_type="application/json"
                )
    assert resp.status_code == 200
    car_modified = Car.objects.get(pk=car.id)
    assert car_modified.marca == 'Tesla'



# delete a car
@pytest.mark.django_db
def test_delete_car(client, add_car):
    car = add_car(marca='Ferrari', modelo='1')
    cars = Car.objects.all()
    assert len(cars) == 1
    resp = client.delete(f"/automotive/api/{car.id}/")
    assert resp.status_code == 204
    cars = Car.objects.all()
    assert len(cars) == 0