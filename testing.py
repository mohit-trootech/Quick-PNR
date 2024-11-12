from requests import post
from multiprocessing import Pool


token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMxNDE2ODAyLCJpYXQiOjE3MzE0MTMyMDIsImp0aSI6Ijk0YTljYzIzY2Q4NDQ4ZGU5NjE3NmQ3ZmJkZDk4ZTM0IiwidXNlcl9pZCI6MX0.oTpWRrR1lU4Ny-jrxFZUD3P1KjbbZ-9lxhUA_QbF9iY"
pnr = 8725278554


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
    breakpoint()
    print(results)
