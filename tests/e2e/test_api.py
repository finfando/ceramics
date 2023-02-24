import requests

from ceramics import config


def test_api_adds_student():
    data = {"name": "John"}
    url = config.get_api_url()
    r = requests.post(f"{url}/students/new", data=data)
    assert r.status_code == 200
