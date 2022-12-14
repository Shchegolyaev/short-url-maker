import os
import time
from multiprocessing import Process

import requests

from core.keygen import create_unique_random_key


def test_create_short_url():
    long_url = f"https://dzen.ru/{create_unique_random_key()}"
    response = requests.post(
        "http://127.0.0.1:8001/api/v1/", json={"long_url": long_url}
    )
    short_url_id = response.json()["short_url"].split("/")[-1]
    assert len(short_url_id) == 10
    response = requests.post(
        "http://127.0.0.1:8001/api/v1/", json={"long_url": long_url}
    )
    short_url_id_2 = response.json()["short_url"].split("/")[-1]
    assert short_url_id == short_url_id_2
    return short_url_id


def test_get_long_url(short_url_id):
    response = requests.get(f"http://127.0.0.1:8001/api/v1/{short_url_id}221")
    assert response.text == "Item not found"
    response = requests.get(f"http://127.0.0.1:8001/api/v1/{short_url_id}")
    assert response.status_code == 200


def test_delete_url(short_url_id):
    response = requests.delete(f"http://127.0.0.1:8001/api/v1/{short_url_id}")
    print(response.text)
    assert response.json()["Deleted"] == "True"
    response = requests.get(f"http://127.0.0.1:8001/api/v1/{short_url_id}")
    print(response.text)
    assert response.text == "Gone"
    assert response.status_code == 410


def test_ping_db():
    response = requests.get("http://127.0.0.1:8001/api/v1/ping")
    assert response.json()["Availability"] == "accepting connections"


def start_server():
    os.system("python3 main.py")
    time.sleep(5)
    return


def start_client():
    short_url_id = test_create_short_url()
    test_get_long_url(short_url_id)
    test_delete_url(short_url_id)
    test_ping_db()


if __name__ == "__main__":
    proc_server = Process(target=start_server)
    proc_client = Process(target=start_client)
    proc_server.start()
    time.sleep(2)
    proc_client.start()
    proc_client.join()
    proc_server.join()
