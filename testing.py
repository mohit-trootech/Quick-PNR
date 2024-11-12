from requests import post
from multiprocessing import Pool


token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMxMzg5NDM5LCJpYXQiOjE3MzEzODU4MzksImp0aSI6ImU1MmUwOGU4ODkxMjQ4NjlhMzg1MDRhYjc0MzAxOWE1IiwidXNlcl9pZCI6MjJ9.ZVt4QHZvj8Oa6Dmd29nas2IbYARHFj2VrC4dvRUfNVc"
pnr = 8425362963


def test_api(url):
    response = post(url, data={"pnr": pnr}, headers={"Authorization": token})
    return response


if __name__ == "__main__":
    urls = [
        "http://127.0.0.1:8000/pnr/fetch/",
        "http://127.0.0.1:8000/pnr/fetch/",
        "http://127.0.0.1:8000/pnr/fetch/",
        "http://127.0.0.1:8000/pnr/fetch/",
        "http://127.0.0.1:8000/pnr/fetch/",
        "http://127.0.0.1:8000/pnr/fetch/",
        "http://127.0.0.1:8000/pnr/fetch/",
        "http://127.0.0.1:8000/pnr/fetch/",
        "http://127.0.0.1:8000/pnr/fetch/",
        "http://127.0.0.1:8000/pnr/fetch/",
        "http://127.0.0.1:8000/pnr/fetch/",
        "http://127.0.0.1:8000/pnr/fetch/",
    ]
    with Pool(processes=4) as pool:
        results = pool.map(test_api, urls)
    print(results)
