from requests import post
from multiprocessing import Pool


token = "Bearer <token>"
pnr = "pnr_number"


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
