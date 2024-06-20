import googlemaps
import requests
from config import API_KEY

class CustomGoogleMapsClient(googlemaps.Client):
    def _request(self, url, params, first_request_time=None, retry_counter=0, base_url=None, accepts_clientid=True, extract_body=None, requests_kwargs=None):
        if requests_kwargs is None:
            requests_kwargs = {}
        requests_kwargs['verify'] = False
        return super()._request(url, params, first_request_time, retry_counter, base_url, accepts_clientid, extract_body, requests_kwargs)

def get_directions(api_key, origin, destination):
    gmaps = CustomGoogleMapsClient(key=api_key)

    try:
        directions_result = gmaps.directions(origin, destination, mode="driving")
    except requests.exceptions.SSLError as e:
        print(f"SSL error occurred: {e}")
        return None
    except googlemaps.exceptions.TransportError as e:
        print(f"Transport error occurred: {e}")
        return None

    return directions_result

def print_directions(directions_result):
    if not directions_result:
        print("No directions found.")
        return

    steps = directions_result[0]['legs'][0]['steps']
    for step in steps:
        instructions = step['html_instructions']
        distance = step['distance']['text']
        duration = step['duration']['text']
        print(f"{instructions} ({distance}, {duration})")

def main():
    origin = '735 NW Gilman Blvd, Issaquah, WA 98027'
    destination = '600 5th Ave S, Seattle, WA 98104'
    
    directions_result = get_directions(API_KEY, origin, destination)
    
    print()

    print_directions(directions_result)

if __name__ == '__main__':
    main()
