import requests

def download_picture(path_to_picture):
    r = requests.get(path_to_picture, stream=True)
    if (r.status_code == 200):
        with open("default.png", "wb") as f:
            for chunk in r:
                f.write(chunk)
