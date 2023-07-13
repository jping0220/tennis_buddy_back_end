import requests

#COnnect with an API that returns a list of zip code 20 miles radius from the given zip_code.

path = "https://api.zip-codes.com/ZipCodesAPI.svc/1.0/FindZipCodesInRadius"

# zip_code = 98075


def create_params(zip_code):
    query_params = {
        "zipcode": zip_code,
        "minimumradius": 0,
        "maximumradius": 20,
        "country": "ALL",
        "key": "DEMOAPIKEY"
    }
    return query_params


def construct_request_for_zip_code(query_params):
    response = requests.get(path, params=query_params)
    response_body = response.json()
    return response_body


def get_list_of_zip_codes(zip_code):
    query_params = create_params(zip_code)
    response_body = construct_request_for_zip_code(query_params)
    closest_zip_codes = []
    list_of_cities = response_body['DataList']
    for item in list_of_cities:
        closest_zip_codes.append(item["Code"])
    return closest_zip_codes


# get_list_of_zip_codes(zip_code)

