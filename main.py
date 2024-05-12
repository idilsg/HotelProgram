from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv

# CURRENT URL IS FOR BELOW QUERY
# Rome
# checkin= 2024-06-03
# checkout=2024-06-16
# group_adults=2
# no_rooms=1
# group_children=0

url = ('https://www.booking.com/searchresults.html?ss=Rome&ssne=Rome&ssne_untouched=Rome&efdco=1&label=gen173nr-1FCAE'
       'oggI46AdIM1gEaOQBiAEBmAExuAEHyAEP2AEB6AEBAECiAIBqAIDuAKo8sKxBsACAdICJGZlZWVmNGJjLWI2OGEtNGM0OS05ODk0LTM2ZGQ4Y'
       'zkxYzY0MNgCBeACAQ&aid=304142&lang=en-us&sb=1&src_elem=sb&src=index&dest_id=-126693&dest_type=city&checkin=2024'
       '-06-03&checkout=2024-06-16&group_adults=2&no_rooms=1&group_children=0')
headers = {'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/51.0.'
                         '2704.64 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'
           }

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
hotels = soup.findAll('div', {'data-testid': 'property-card'})
hotels_data = []

# Loop over the hotel elements and extract the desired data
for hotel in hotels:
    # Extract the hotel name
    name_element = hotel.find('div', {'data-testid': 'title'})
    name = name_element.text.strip()
    # Append hotels_data with info about hotel
    hotels_data.append({'name': name})

hotels = pd.DataFrame(hotels_data)
hotels.head()
hotels.to_csv('test_hotels.csv', header=True, index=False)
