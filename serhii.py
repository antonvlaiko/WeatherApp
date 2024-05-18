import os
import requests
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

BASE_URL = "http://api.weatherapi.com/v1/current.json"


# 200, 201, 203 -> Success
# 300 -> Redirect
# 400, 401, 403, 404 -> Client error
# 500 -> Server error

def main() -> None:
    params = {
        #"q": "Chernivtsi",
        "q": "48.29344381086331,25.93368057714031",
        "key": os.getenv("API")
    }
    
    response = requests.get(BASE_URL, params=params)
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        pprint(data)


if __name__ == "__main__":
    main()
