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

"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import requests
from bs4 import BeautifulSoup


# Function to scrape hotel information from Booking.com
def scrape_hotels(city, checkin_date, checkout_date):
    try:
        # Construct URL for Booking.com with the provided parameters
        url = (f'https://www.booking.com/searchresults.html?ss={city}&checkin={checkin_date}&checkout={checkout_date}&g'
               f'roup_adults=2&no_rooms=1&group_children=0')
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chr'
                                 'ome/94.0.4606.81 Safari/537.36'}

        # Send HTTP request and fetch the hotel information from Booking.com
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        hotels = soup.findAll('div', {'data-testid': 'property-card'})

        # Store hotel data
        hotel_data = []

        # Loop over the hotel elements and extract the desired data
        for hotel in hotels:
            name_element = hotel.find('div', {'data-testid': 'title'})
            address_element = hotel.find('a', {'data-testid': 'property-address'})
            distance_element = hotel.find('div', {'data-testid': 'distanceFromCenter'})
            rating_element = hotel.find('span', {'data-testid': 'guest-rating-value'})
            price_element = hotel.find('div', {'data-testid': 'price-value'})

            name = name_element.text.strip() if name_element else 'NOT GIVEN'
            address = address_element.text.strip() if address_element else 'NOT GIVEN'
            distance = distance_element.text.strip() if distance_element else 'NOT GIVEN'
            rating = rating_element.text.strip() if rating_element else 'NOT GIVEN'
            price = price_element.text.strip() if price_element else 'NOT GIVEN'

            hotel_data.append({'Name':name, 'Address': address, 'Distance': distance, 'Rating': rating, 'Price': price})

        return hotel_data[:5]  # Return top 5 hotels
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


# Function to handle search button click
def search_hotels():
    city = city_combobox.get()
    checkin_date = checkin_entry.get()
    checkout_date = checkout_entry.get()

    if city and checkin_date and checkout_date:
        hotels = scrape_hotels(city, checkin_date, checkout_date)
        if hotels:
            display_hotels(hotels)
        else:
            messagebox.showinfo("Info", "No hotels found.")
    else:
        messagebox.showinfo("Info", "Please fill all fields.")


# Function to display hotels in the GUI
def display_hotels(hotels):
    hotels_text.delete(1.0, tk.END)
    for idx, hotel in enumerate(hotels, start=1):
        hotels_text.insert(tk.END, f"Hotel {idx}:\n")
        for key, value in hotel.items():
            hotels_text.insert(tk.END, f"{key}: {value}\n")
        hotels_text.insert(tk.END, "\n")


# GUI setup
root = tk.Tk()
root.title("Hotel Program")

main_frame = ttk.Frame(root, padding="20")
main_frame.grid(row=0, column=0)

city_label = ttk.Label(main_frame, text="Select City:")
city_label.grid(row=0, column=0, sticky="w")

cities = ['Paris', 'London', 'Berlin', 'Munich', 'Barcelona', 'Los Angeles', 'Miami', 'Sydney', 'Tokyo', 'Osaka']
city_combobox = ttk.Combobox(main_frame, values=cities)
city_combobox.grid(row=0, column=1, pady=5)

checkin_label = ttk.Label(main_frame, text="Check-in Date:")
checkin_label.grid(row=1, column=0, sticky="w")
checkin_entry = ttk.Entry(main_frame)
checkin_entry.grid(row=1, column=1, pady=5)

checkout_label = ttk.Label(main_frame, text="Check-out Date:")
checkout_label.grid(row=2, column=0, sticky="w")
checkout_entry = ttk.Entry(main_frame)
checkout_entry.grid(row=2, column=1, pady=5)

search_button = ttk.Button(main_frame, text="Search Hotels", command=search_hotels)
search_button.grid(row=3, column=0, columnspan=2, pady=10)

hotels_text = tk.Text(main_frame, height=15, width=80)
hotels_text.grid(row=4, column=0, columnspan=2)

root.mainloop()
"""